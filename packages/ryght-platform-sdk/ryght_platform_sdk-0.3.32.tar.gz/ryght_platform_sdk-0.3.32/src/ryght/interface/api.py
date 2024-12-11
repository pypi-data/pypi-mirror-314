# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import os
import time
import json
import logging

from result import as_result
from urllib.parse import urljoin
from urllib.parse import urlencode
from pydantic import ValidationError

from ryght.models import Token
from ryght.utils import QnARating
from ryght.utils import FlowTypes
from ryght.configs import Credentials
from ryght.utils import ModelOperation
from ryght.utils import RequestMethods
from ryght.configs import ApiEndpoints
from ryght.managers import TokenManager
from ryght.requests import HttpxRequestExecutor

from ryght.models import Prompts
from ryght.models import AIModels
from ryght.models import Documents
from ryght.models import Collection
from ryght.models import TraceStatus
from ryght.models import JsonDocument
from ryght.models import ConversationInfo
from ryght.models import CompletionsResponse
from ryght.models import ConversationResponse
from ryght.models import ChunkedDocumentCollection
from ryght.models import OrganizationSearchResponse
from ryght.models import LoincOrder
from ryght.models import LoincCoding

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class ApiInterface:
    api_endpoints: ApiEndpoints
    token_manager: TokenManager
    http_request_exec: HttpxRequestExecutor

    def __init__(self, env: str = 'production'):
        self.api_endpoints = ApiEndpoints.load_api_endpoints(env=env)
        self.http_request_exec = HttpxRequestExecutor()
        self.token_manager: TokenManager = TokenManager(
            token=Token.init_as_none(),
            credentials=Credentials.init_none(),
            requestor=self.http_request_exec,
            auth_url=self.api_endpoints.auth_token_url
        )

    def get_auth_headers(self):
        return {'Authorization': self.token_manager.token.authorization_param}

    @TokenManager.authenticate
    def execute_request(
            self,
            method: RequestMethods,
            url,
            **kwargs
    ) -> dict | str:

        try:
            match method:
                case RequestMethods.GET:
                    request_fn = self.http_request_exec.get
                case RequestMethods.PUT:
                    request_fn = self.http_request_exec.put
                case RequestMethods.POST:
                    request_fn = self.http_request_exec.post
                case RequestMethods.PATCH:
                    request_fn = self.http_request_exec.patch
                case RequestMethods.DELETE:
                    request_fn = self.http_request_exec.delete
                case _:
                    raise ValueError(f'Unknown method {method}')

            auth_headers = self.get_auth_headers()
            if 'headers' in kwargs and isinstance(kwargs['headers'], dict):
                kwargs["headers"].update(auth_headers)
            else:
                kwargs["headers"] = auth_headers

            response = request_fn(url=url, **kwargs)
            
            match response.status_code:
                case 200 | 201 | 202 | 203 | 204:
                    if response.headers.get('Content-Type') == 'application/json':
                        return response.json()
                    elif response.text is not None and response.text != '':
                        value = response.text
                        return f'Success! response text: {value}'
                    else:
                        return f'Success! response code: {response.status_code}'

                case 400 | 402 | 403 | 404:
                    logger.error(
                        f'Got client error: {response.status_code}, '
                        f'Please check your credential & api endpoint variables'
                    )
                    response.raise_for_status()

                case 500 | 502 | 503 | 504:
                    logger.error('Got client error: 500, attempting new token request after 5 seconds')
                    time.sleep(5)
                    # try this outside this func
                    response = request_fn(url=url, **kwargs)
                    response.raise_for_status()

                case _:
                    logger.error(f'Unknown response status code: {response.status_code}')
        except ValueError as value_error:
            logger.error(f'ValueError occurred: {value_error}')
        except Exception as exception:
            logger.error('Exception occurred: {}'.format(exception))


# -------------------------------------------------------------------------------------------------------------------- #
class DocumentCollectionAPI(ApiInterface):
    @as_result(NotImplementedError)
    def get_collection_page_by_page(self, query_params: dict = None):
        raise NotImplementedError(f'Get collections page by page not implemented !')

    def create_new_collection(
            self,
            collection_name: str,
            metadata: dict | None,
            tag_ids: list | None,
            is_externally_chunked: bool
    ) -> str:
        logger.debug(f'Create a new/empty collection')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document_collection.base)
        headers = {'Content-Type': 'application/json'}
        result = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            data=json.dumps({
                'name': collection_name,
                'metadata': metadata,
                'tagIds': tag_ids if tag_ids else [],
                'isExternalChunked': is_externally_chunked
            }),
            timeout=20.0
        )
        return result.get('id')

    def get_all_available_collections(self) -> list[Collection]:
        return self.search_collections(
            query_params={
                'size': 100
            }
        )

    def search_collections(self, query_params: dict = None) -> list[Collection]:
        logger.debug(f'Getting available collections ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document_collection.search)
        if isinstance(query_params, dict):
            url = urljoin(url, '?' + urlencode(query_params))
            print(url)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        collections = []
        if 'content' in result:
            for collection_details in result['content']:
                collections.append(Collection(**collection_details))
        return collections

    def get_collection_details(self, collection_id: str) -> Collection:
        logger.debug(f"Getting a collection's details ...")
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document_collection.by_id)
        url = url.format(id=collection_id)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        return Collection(**result)

    @as_result(Exception)
    def delete_collection_by_id(self, collection_id: str) -> str:
        logger.debug(f"Request a collection deletion by collection id ...")
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document_collection.by_id)
        url = url.format(id=collection_id)
        result: str = self.execute_request(
            method=RequestMethods.DELETE,
            url=url,
            timeout=20.0
        )

        return result

    @as_result(Exception)
    def upload_chunked_document_collection(self, document_collection: ChunkedDocumentCollection | dict) -> str:
        logger.debug(f'Create/update chunked document collection')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document.pre_chunked)
        headers = {'Content-Type': 'application/json'}
        if isinstance(document_collection, ChunkedDocumentCollection):
            data = document_collection.model_dump_json(by_alias=True)
        else:
            data = json.dumps(document_collection)
        result: str = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            data=data,
            timeout=20.0
        )
        return result

    def track_status(self, trace_id: str) -> TraceStatus:
        logger.debug(f'Tract status of a call using trace ID')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.file_store.status)
        url = url.format(traceId=trace_id)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        return TraceStatus(**result)

    @as_result(Exception)
    def upload_doc_as_json_to_a_document_collection(
            self,
            collection_id: str,
            document_path: str
    ) -> dict:
        logger.debug(f'Upload a json file doc to the document collection')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.file_store.base_url)
        url = url.format(collectionId=collection_id)

        if os.path.isfile(document_path):
            with open(document_path, 'r') as f:
                document = JsonDocument(
                    **json.load(f)
                )
            print(document)

            document.metadata.extra_fields['collectionId'] = collection_id

            with open(document_path, 'rb') as file:
                file_data = {
                    'file': (document.name, file),
                    'fileName': document.name,
                    'isPublished': (None, 'true', 'application/json'),
                    'metadata': (None, document.metadata.model_dump_json(by_alias=True), 'application/json')
                }

                result = self.execute_request(
                    method=RequestMethods.POST,
                    url=url,
                    files=file_data,
                    timeout=20.0
                )

                assert isinstance(
                    result,
                    dict
                ), f'Expected response was a type dict, but got a object of type {type(result)}'
                return result
        else:
            raise FileNotFoundError(document_path)

    @as_result(Exception)
    def get_file_by_id(
            self,
            file_id: str,
    ) -> dict:
        logger.debug(f'Get file by id')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.file_store.file_by_id)
        url = url.format(id=file_id)

        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )

        assert isinstance(
            result,
            dict
        ), f'Expected response was a type dict, but got a object of type {type(result)}'
        return result


    def upload_pdf_doc_to_a_document_collection(
            self,
            collection_id: str,
            document_path: str,
            file_name: str
    ):
        logger.debug(f'Upload a PDF doc to the document collection')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.file_store.pdf_file)
        metadata = {'extraFields': {'collectionId': collection_id}}
        if os.path.isfile(document_path):
            with open(document_path, 'rb') as file:
                files = {
                    'file': (file_name, file),
                    'fileName': file_name,
                    'isPublished': (None, 'true', 'application/json'),
                    'metadata': (None, json.dumps(metadata), 'application/json')
                }

                result = self.execute_request(
                    method=RequestMethods.POST,
                    url=url,
                    files=files,
                    timeout=20.0
                )

                assert isinstance(
                    result,
                    dict
                ), f'Expected response was a type dict, but got a object of type {type(result)}'
                return result
            
        else:
            raise FileNotFoundError(document_path)


# -------------------------------------------------------------------------------------------------------------------- #
class CompletionsAPI(ApiInterface):
    def perform_completions(
            self,
            input_str: str,
            collection_ids: str | list[str],
            flow: FlowTypes = FlowTypes.SEARCH,
            search_limit: int = 5,
            completion_model_id: str = None,
            embedding_model_id: str = None,
            document_ids: list[str] | None = None,
            ai_tags: list[str] | None = None
    ) -> CompletionsResponse:
        logger.debug(f'Performing completions ... ')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.completions.base)
        payload = {
            "prompt": {
                "question": input_str
            },
            "flow": flow.value if isinstance(flow, FlowTypes) else None,
            "collectionIds": collection_ids if isinstance(collection_ids, list) else [collection_ids],
            "completionModelId": completion_model_id,
            "limit": search_limit,
            "documentIds": document_ids,
            "aiTagIds": ai_tags
        }
        headers = {'Content-Type': 'application/json'}
        result = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=90.0
        )
        if result:
            return CompletionsResponse(**result)
        else:
            return CompletionsResponse().init_with_none()


# -------------------------------------------------------------------------------------------------------------------- #
class ModelsAPI(ApiInterface):
    # Models
    def get_ai_models(self) -> list[AIModels]:
        logger.debug(f'Getting all AI models ... ')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.model_specification.base)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        models = []
        for model in result:
            models.append(AIModels(**model))
        return models

    def get_ai_model_by_id(self, model_id: str) -> AIModels:
        logger.debug(f'Getting AI model by id: {model_id} ... ')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.model_specification.by_id)
        url = url.format(id=model_id)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        return AIModels(**result)

    def get_ai_models_by_operation(self,
                                   operation: ModelOperation = ModelOperation.EMBEDDING
                                   ) -> list[AIModels]:
        logger.debug(f'Getting AI models by operation: {operation} ... ')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.model_specification.operation)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            params={
                "operation": operation.value
            },
            timeout=20.0
        )
        models = []
        for model in result:
            models.append(AIModels(**model))
        return models


# -------------------------------------------------------------------------------------------------------------------- #
class DocumentsAPI(ApiInterface):
    # Documents
    def upload_documents(self, document_path: str, file_name: str, tag_ids: list):
        logger.debug(f'Uploading file: {file_name} ... ')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document.upload)
        data = {
            "fileName": file_name,
            "tagIds": tag_ids
        }
        result = None
        if os.path.isfile(document_path):
            with open(document_path, 'rb') as file:
                files = {
                    'file': (file_name, file)
                }
                result = self.execute_request(
                    method=RequestMethods.POST,
                    url=url,
                    files=files,
                    data=data,
                    timeout=20.0
                )
        else:
            logger.info(f'Provided file path: "{document_path}" is not valid')

        return Documents(**result)

    def get_document_collection(self) -> list[Documents]:
        logger.debug(f'Getting default document collections')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document.search)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        documents = []
        if 'content' in result:
            for collection_details in result['content']:
                documents.append(Documents(**collection_details))
        return documents

    def rename_document(self, document_id: str, new_name: str) -> str:
        logger.debug(f'Rename document by ID')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document.by_id)
        url = url.format(id=document_id)
        headers = {'Content-Type': 'application/json'}
        result = self.execute_request(
            method=RequestMethods.PATCH,
            url=url,
            headers=headers,
            data=json.dumps({'name': new_name}),
            timeout=20.0
        )
        return result

    def get_document_by_id(self, document_id: str) -> Documents:
        logger.debug(f'Getting document by ID')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document.by_id)
        url = url.format(id=document_id)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        if result:
            return Documents(**result)
        else:
            return None

    def delete_document_by_id(self, document_id: str):
        logger.debug(f'Delete document by ID')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.document.by_id)
        url = url.format(id=document_id)
        result = self.execute_request(
            method=RequestMethods.DELETE,
            url=url,
            timeout=20.0
        )
        return result


# -------------------------------------------------------------------------------------------------------------------- #
class ConversationsAPI(ApiInterface):
    @as_result(Exception, ValueError, ValidationError, TypeError)
    def find_user_conversations(self, query_params: dict = None) -> list[ConversationInfo]:
        logger.debug(f'Find the Conversations of the current user ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.conversations.base)
        if isinstance(query_params, dict):
            url = urljoin(url, '?' + urlencode(query_params))
            print(url)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        conversations_list = []
        if 'content' in result:
            for collection_details in result['content']:
                conversations_list.append(ConversationInfo(**collection_details))
            return conversations_list
        else:
            raise Exception('Content is not found in the response, Parsing Error.')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def update_conversation_name(
            self,
            conversation_id: str,
            new_name: str
    ) -> str:
        logger.debug(f'update a given conversation by its ID')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.conversations.base)
        headers = {'Content-Type': 'application/json'}

        payload = {
            'id': conversation_id,
            'name': new_name
        }

        result = self.execute_request(
            method=RequestMethods.PUT,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=20.0
        )
        if result is None:
            raise Exception(f'Got None as response, response: {result}')
        else:
            return result

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def converse(
            self,
            prompt: Prompts,
            conversation_id: str | None = None,
            collection_ids: str | list[str] | None = None,
            ai_tag_ids: str | list[str] | None = None,
            default_collection: bool = False,
            document_ids: list[str] | None = None,
            copilot_id: str | None = None,
    ) -> ConversationResponse:
        """

        :param prompt:
        :param conversation_id:
        :param collection_ids:
        :param ai_tag_ids:
        :param default_collection:
        :param document_ids:
        :param copilot_id:
        :return:
        """

        logger.debug(f'update a given conversation by its ID')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.conversations.base)

        headers = {'Content-Type': 'application/json'}

        payload = {
            "defaultCollection": default_collection,
        }
        if conversation_id:
            payload['conversationId'] = conversation_id

        if collection_ids:
            payload['collectionIds'] = collection_ids if isinstance(collection_ids, list) else [collection_ids]

        if document_ids:
            payload['documentIds'] = document_ids if isinstance(document_ids, list) else [document_ids]

        if ai_tag_ids:
            payload["aiTagIds"] = ai_tag_ids if isinstance(ai_tag_ids, list) else [ai_tag_ids]

        if copilot_id:
            payload['copilotId'] = copilot_id

        prompt_payload = {}
        prompt_data: dict = prompt.model_dump()
        for key, data in prompt_data.items():
            if data:
                prompt_payload[key] = data

        payload['prompt'] = prompt_payload

        result = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=25.0
        )
        if result is None:
            raise Exception(f'Got None as response, response: {result}')
        else:
            return ConversationResponse(**result)

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def send_feedback(
            self,
            feedback_message: str,
            question_answer_id: str,
            rating: QnARating
    ) -> str:
        logger.debug(f'Feedback for QnA ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.conversations.feedback)

        headers = {'Content-Type': 'application/json'}
        payload = {
            "content": feedback_message,
            "questionAnswerId": question_answer_id,
            "rate": rating.value if isinstance(rating, QnARating) else None
        }

        result = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=20.0
        )
        if result is None:
            raise Exception(f'Got None as response, response: {result}')
        else:
            return result

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def delete_conversation_by_id(self, conversation_id: str):
        logger.debug(f'Deleting a conversation by its ID ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.conversations.by_id)
        url = url.format(id=conversation_id)
        result = self.execute_request(
            method=RequestMethods.PATCH,
            url=url,
            timeout=20.0
        )
        if result is None:
            raise Exception(f'Got None as response, response: {result}')
        else:
            return result

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def get_all_question_and_answers(self, conversation_id: str) -> list[ConversationResponse]:
        logger.debug(f'Loading all question and answers for conversation ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.conversations.by_id)
        url = url.format(id=conversation_id)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        question_and_answers = []
        if 'content' in result:
            for collection_details in result['content']:
                question_and_answers.append(ConversationResponse(**collection_details))
            return question_and_answers
        else:
            raise Exception('Content is not found in the response, Parsing Error.')


# -------------------------------------------------------------------------------------------------------------------- #
class OrganizationAPI(ApiInterface):

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def list_all_organizations(self) -> list[OrganizationSearchResponse]:
        """
        List all organizations that are visible to the user
        :return: list[OrganizationSearchResponse]
        """
        logger.debug(f'Requesting all organizations names and ids ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.organization.search)
        result = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        organizations = []
        if isinstance(result, list):
            for organization in result:
                organizations.append(OrganizationSearchResponse(**organization))
        else:
            raise Exception(f'Expected list of organizations, got {result}')

        return organizations

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def list_all_organization_names(self) -> list[str]:
        """
        List all organizations that are visible to the user
        :return: list[OrganizationSearchResponse]
        """
        result = self.list_all_organizations()
        org_names = []
        for organization in result.ok_value:
            org_names.append(organization.name)
        return org_names

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def get_organization_by_id(self, organization_id: str) -> OrganizationSearchResponse:
        """

        :param organization_id:
        :return:
        """
        result = self.list_all_organizations()
        for organization in result.ok_value:
            if organization.id == organization_id:
                return organization
        raise Exception(f'Organization with ID {organization_id} is not found')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def get_organization_by_name(self, organization_name: str) -> OrganizationSearchResponse:
        """

        :param organization_name:
        :return:
        """
        result = self.list_all_organizations()

        for organization in result.ok_value:
            if organization.name == organization_name:
                return organization
        raise Exception(f'Organization with Name {organization_name} is not found')


# -------------------------------------------------------------------------------------------------------------------- #
class PermissionManagementAPI(ApiInterface):

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def list_all_resources(self) -> list[str]:
        """
        List all the Resources
        :return: list[str]
        """
        logger.debug(f'Listing all resources ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.resources)
        response = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        if isinstance(response, list):
            return response
        else:
            raise Exception(f'Expected list of resources, got {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def list_resource_permissions(
            self,
            resource_type: str
    ) -> list[str]:
        """
        List the permissions available by the Resources
        :param resource_type: str
            type of resource
        :return: str
        """
        logger.debug(f'Listing permission by available resources ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.permissions)
        url = urljoin(url, '?' + urlencode({'resource': resource_type}))
        response = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        if isinstance(response, list):
            return response
        else:
            raise Exception(f'Expected list of permissions available by the resources, got {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def revoke_all_resource_permissions(
            self,
            resource_ids: list[str],
            resource_type: str
    ) -> list[str]:
        """
        Revoke all permissions available for the Resources
        :param resource_ids: list[str]
            list of resource IDs
        :param resource_type: str
            type of resource
        :return: str
        """
        logger.debug(f'Listing permission by available resources ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.permissions)
        url = urljoin(url, '?' + urlencode({
            'resourceIds': resource_ids,
            'resource': resource_type
        }))
        response = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        if isinstance(response, list):
            return response
        else:
            raise Exception(f'Expected list of permissions available by the resources, got {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def check_user_permission_for_resource(
            self,
            resource_id: str,
            permissions: str,
            resource_type: str
    ) -> str:
        """

        Check if the user has particular permission for a given resources

        :param resource_id: str
            Target Resource ID
        :param permissions: str
            Resource permissions
        :param resource_type: str
            Resource type
        :return: str
        """
        logger.debug(f'Performing check_user_permission_for_resource() ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.for_users)
        url = urljoin(url, '?' + urlencode({
            'resourceId': resource_id,
            'permissions': permissions,
            'resource': resource_type
        }))
        response = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        if response:
            return response
        else:
            raise Exception(f'Got None as response, response: {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def check_resource_permission_for_members_of_organizations(
            self,
            resource_id: str,
            organization_ids: list[str],
            permissions: str,
            resource_type: str
    ) -> str:
        """

        Check if the members of organization has particular permission for a given resource

        :param organization_ids: list[str] -> UUID
            List of organization IDs
        :param resource_id: str
            Target Resource ID
        :param permissions: str
            Resource permissions
        :param resource_type: str
            Resource type
        :return: str
        """
        logger.debug(f'Performing check_resource_permission_for_members_of_organizations() ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.for_members)
        url = urljoin(url, '?' + urlencode({
            'resourceId': resource_id,
            'organizationIds': organization_ids,
            'permissions': permissions,
            'resource': resource_type
        }))
        response = self.execute_request(
            method=RequestMethods.GET,
            url=url,
            timeout=20.0
        )
        if response:
            return response
        else:
            raise Exception(f'Got None as response, response: {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def grant_current_organization_users_resources_permission(
            self,
            organization_id: str,
            user_ids: list[str],
            resource_ids: list[str],
            resource_type: str,
            permission: str
    ) -> str:
        """
        Grant the users of current organization permission to list of resources
        :param organization_id: str -> UUID
            Target Organization ID
        :param user_ids: list[str] -> UUID
            list of User IDs
        :param resource_ids: list[str] -> UUID
            list of Resource IDs
        :param resource_type: str
            Type of Resource
        :param permission: str
            Permission to grant the users in an organization permission
        :return: str
            If status request status is 2XX then we get a str as response if not None or other error filled str
        """

        logger.debug(f'Performing grant_current_organization_users_resources_permission() ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.for_users)
        url = url.format(organizationId=organization_id)

        headers = {'Content-Type': 'application/json'}
        payload = {
            "userIds": user_ids,
            "resourceIds": resource_ids,
            "resource": resource_type,
            "permission": permission
        }
        response = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=20.0
        )
        if response:
            return response
        else:
            raise Exception(f'Got None as response, response: {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def grant_target_organization_users_resources_permission(
            self,
            organization_id: str,
            user_ids: list[str],
            resource_ids: list[str],
            resource_type: str,
            permission: str
    ) -> str:
        """
        Grant the users in an organization permission to list of resources
        :param organization_id: str -> UUID
            Target Organization ID
        :param user_ids: list[str] -> UUID
            list of User IDs
        :param resource_ids: list[str] -> UUID
            list of Resource IDs
        :param resource_type: str
            Type of Resource
        :param permission: str
            Permission to grant the users in an organization permission
        :return: str
            If status request status is 2XX then we get a str as response if not None or other error filled str
        """

        logger.debug(f'Performing grant_target_organization_users_resources_permission() ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.permissions_users_in_org)
        url = url.format(organizationId=organization_id)

        headers = {'Content-Type': 'application/json'}
        payload = {
            "userIds": user_ids,
            "resourceIds": resource_ids,
            "resource": resource_type,
            "permission": permission
        }
        response = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=20.0
        )
        if response:
            return response
        else:
            raise Exception(f'Got None as response, response: {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def grant_current_organization_members_resources_permission(
            self,
            organization_id: str,
            resource_ids: list[str],
            resource_type: str,
            permission: str
    ) -> str:
        """
        Grant all the members of current organization permission to list of resources
        :param organization_id: str -> UUID
            Target Organization ID
        :param resource_ids: list[str] -> UUID
            list of Resource IDs
        :param resource_type: str
            Type of Resource
        :param permission: str
            Permission to grant the users in an organization permission
        :return: str
            If status request status is 2XX then we get a str as response if not None or other error filled str
        """

        logger.debug(f'Performing grant_current_organization_members_resources_permission() ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.for_members)
        url = url.format(organizationId=organization_id)

        headers = {'Content-Type': 'application/json'}
        payload = {
            "resourceIds": resource_ids,
            "resource": resource_type,
            "permission": permission
        }
        response = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=20.0
        )
        if response:
            return response
        else:
            raise Exception(f'Got None as response, response: {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def grant_target_organization_members_resources_permission(
            self,
            organization_id: str,
            resource_ids: list[str],
            resource_type: str,
            permission: str
    ) -> str:
        """
        Grant all the members in an organization permission to list of resources
        :param organization_id: str -> UUID
            Target Organization ID
        :param resource_ids: list[str] -> UUID
            list of Resource IDs
        :param resource_type: str
            Type of Resource
        :param permission: str
            Permission to grant the users in an organization permission
        :return: str
            If status request status is 2XX then we get a str as response if not None or other error filled str
        """

        logger.debug(f'Performing grant_target_organization_members_resources_permission() ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.permissions_members_of_org)
        url = url.format(organizationId=organization_id)

        headers = {'Content-Type': 'application/json'}
        payload = {
            "resourceIds": resource_ids,
            "resource": resource_type,
            "permission": permission
        }
        response = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=20.0
        )
        if response:
            return response
        else:
            raise Exception(f'Got None as response, response: {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def revoke_target_organization_members_resources_permission(
            self,
            organization_id: str,
            resource_ids: list[str],
            resource_type: str,
            permission: str
    ) -> str:
        """
        Revoke all the members in an organization permission to list of resources

        :param organization_id: str -> UUID
            Target Organization ID
        :param resource_ids: list[str] -> UUID
            list of Resource IDs
        :param resource_type: str
            Type of Resource
        :param permission: str
            Permission to grant the users in an organization permission
        :return: str
            If status request status is 2XX then we get a str as response if not None or other error filled str
        """

        logger.debug(f'Performing revoke_target_organization_members_resources_permission() ...')
        url = urljoin(
            self.api_endpoints.base_url,
            self.api_endpoints.permission_management.permissions_members_of_org
        )
        url = url.format(organizationId=organization_id)

        headers = {'Content-Type': 'application/json'}
        payload = {
            "resourceIds": resource_ids,
            "resource": resource_type,
            "permission": permission
        }
        response = self.execute_request(
            method=RequestMethods.DELETE,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=20.0
        )
        if response:
            return response
        else:
            raise Exception(f'Got None as response, response: {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def revoke_current_organization_users_resources_permission(
            self,
            organization_id: str,
            user_ids: list[str],
            resource_ids: list[str],
            resource_type: str,
            permission: str
    ) -> str:
        """
        Revoke the users of current organization permission to list of resources
        :param organization_id: str -> UUID
            Target Organization ID
        :param user_ids: list[str] -> UUID
            list of User IDs
        :param resource_ids: list[str] -> UUID
            list of Resource IDs
        :param resource_type: str
            Type of Resource
        :param permission: str
            Permission to grant the users in an organization permission
        :return: str
            If status request status is 2XX then we get a str as response if not None or other error filled str
        """

        logger.debug(f'Performing revoke_current_organization_users_resources_permission() ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.for_users)
        url = url.format(organizationId=organization_id)

        headers = {'Content-Type': 'application/json'}
        payload = {
            "userIds": user_ids,
            "resourceIds": resource_ids,
            "resource": resource_type,
            "permission": permission
        }
        response = self.execute_request(
            method=RequestMethods.DELETE,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=20.0
        )
        if response:
            return response
        else:
            raise Exception(f'Got None as response, response: {response}')

    @as_result(Exception, ValueError, ValidationError, TypeError)
    def revoke_current_organization_members_resources_permission(
            self,
            organization_id: str,
            resource_ids: list[str],
            resource_type: str,
            permission: str
    ) -> str:
        """
        Revoke all the members of current organization permission to list of resources
        :param organization_id: str -> UUID
            Target Organization ID
        :param resource_ids: list[str] -> UUID
            list of Resource IDs
        :param resource_type: str
            Type of Resource
        :param permission: str
            Permission to grant the users in an organization permission
        :return: str
            If status request status is 2XX then we get a str as response if not None or other error filled str
        """

        logger.debug(f'Performing revoke_current_organization_members_resources_permission() ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.permission_management.for_members)
        url = url.format(organizationId=organization_id)

        headers = {'Content-Type': 'application/json'}
        payload = {
            "resourceIds": resource_ids,
            "resource": resource_type,
            "permission": permission
        }
        response = self.execute_request(
            method=RequestMethods.DELETE,
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=20.0
        )
        if response:
            return response
        else:
            raise Exception(f'Got None as response, response: {response}')


# -------------------------------------------------------------------------------------------------------------------- #
class NotesAPI(ApiInterface):
    pass

# -------------------------------------------------------------------------------------------------------------------- #
class MedicalCodingAPI(ApiInterface):
    @as_result(Exception, ValueError, ValidationError, TypeError)
    def get_loinc_coding(
            self,
            panel: LoincOrder = None,
            analytes: list[LoincOrder] = None,
            range_num: int = 100,
            analyte_only: bool = False,
            do_count_match: bool = False
    ) -> list[LoincCoding]:
        """
        Revoke all the members of current organization permission to list of resources
        :param panel: LoincOrder
            Panel
        :param analyte_names: list[LoincOrder]
            List of analytes
        :param range_num: int
            Integer range
        :param analyte_only: bool
            Return analyte if true, return panel if false
        :param do_count_match: bool
            Return result only if no. of analytes match
        :return: 
            If status request status is 2XX then we get a list[LoincCoding] as response if not None or other error filled str
        """

        logger.debug(f'Performing get_loinc_coding() ...')
        url = urljoin(self.api_endpoints.base_url, self.api_endpoints.medical_coding.loinc_coding)

        request_body = {
            "panelRange": range_num,
            "analyteRange": range_num,
            "doCountMatch": do_count_match,
            "returnItem": "analyte" if analyte_only else "panel"
        }
        
        if analytes:
            request_body['analytes'] = [analyte.model_dump(exclude_none=True) for analyte in analytes if analyte]
        if panel:
            request_body['panel'] = panel.model_dump(exclude_none=True)
        
        headers = {'Content-Type': 'application/json'}

        response = self.execute_request(
            method=RequestMethods.POST,
            url=url,
            headers=headers,
            data=json.dumps(request_body),
            timeout=40.0
        )
        if response:
            loinc_coding_responses = []
            if 'results' in response:
                for result in response['results']:
                    loinc_coding_responses.append(LoincCoding(**result))
                return loinc_coding_responses
        else:
            raise Exception(f'Got None as response, response: {response}')
