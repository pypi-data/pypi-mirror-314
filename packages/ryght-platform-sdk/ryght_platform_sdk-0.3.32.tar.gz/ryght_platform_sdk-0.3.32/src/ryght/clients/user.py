# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import logging

from result import Ok
from result import Err
from result import OkErr
from result import as_result

from ryght.models import Prompts
from ryght.configs import Credentials
from ryght.configs import ApiEndpoints
from ryght.interface import BaseClient
from ryght.clients.api import ApiProxyClient
from ryght.models import ChunkedDocumentCollection

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class RyghtClient(BaseClient):
    """
        A client for user to access the Ryght features using the Ryght backend APIs

        You can access the following features using this class,
            - Get a list of all document collections
            - Create a new empty document collection
            - Get a document collection by its ID
            - Perform Completions
            - Get a list of all AI models
            - Get a list of AI models by its operation nature
            - Get an AI model by its ID
            - Get a list of all the documents from default collections
            - Upload a new document to the default collection
            - Get a document from default collections by its ID
            - Delete a document from default collections by its ID
            - Rename a document in default collections by its ID
    """
    pass


# -------------------------------------------------------------------------------------------------------------------- #

class DevClient(BaseClient):
    """
        A client for user to access the Ryght features using the Ryght backend APIs, but with some specialized functions
    for developers and development purposes.

        You can access all the features of RyghtClient and get the following features in addition,
            - Upload a new document to the document collection
            - Upload a new pdf document to the document collection
            - Get status using trace ID
            - Create/Upload a pre-chunked documentCollection
    """

    def __repr__(self):
        return f"Client is Configured to the Environment: {self.environment} for the Organization: {self.organization}"

    def get_client_config(self):
        return {
            "environment": self.environment,
            "organization": self.organization
        }

    def switch_environment(self, env: str, credentials: dict | Credentials | str):
        try:
            self.api_client.api_endpoints = ApiEndpoints.load_api_endpoints(env=env)
            self.api_client.token_manager.auth_url = self.api_client.api_endpoints.auth_token_url
            self.set_credentials(credentials)
            self.api_client.token_manager.get_new_token(organization=self.organization)
        except Exception as e:
            logger.error(e)
        else:
            self.api_client.environment = env
            self.environment = env

    @as_result(Exception, ValueError)
    def switch_organization(self, organization_name: str):
        """

        :param organization_name:
        :return:
        """
        match self.api_client.list_all_organization_names():
            case Ok(organization_names):
                logger.info(f"Available {organization_names}")
                if organization_name in organization_names:
                    logger.info(f"Valid organization name! {organization_name}")
                    self.api_client.token_manager.get_new_token(organization=organization_name)
                    self.api_client.token_manager.credentials.organization = organization_name
                    self.organization = organization_name
                else:
                    raise ValueError(
                        f'Organization "{organization_name}" does not exist or User doesnt belong to the organization.'
                        f'Current organization is set to: {self.organization}'
                    )
            case Err(error_message):
                logger.error(error_message)
                raise Exception(error_message)
        return f'Switched to organization: {self.organization}'

    def create_a_chunked_collection(
            self,
            chunked_document_collection: ChunkedDocumentCollection | dict
    ) -> OkErr:
        return self.api_client.upload_chunked_document_collection(chunked_document_collection)

    def list_all_organizations(self) -> OkErr:
        return self.api_client.list_all_organizations()

    def list_all_organization_names(self) -> OkErr:
        return self.api_client.list_all_organization_names()

    def get_organization_by_name(self, organization_name: str) -> OkErr:
        return self.api_client.get_organization_by_name(organization_name)

    def get_organization_by_id(self, organization_id: str) -> OkErr:
        return self.api_client.get_organization_by_id(organization_id)

    def list_all_resources(self) -> OkErr:
        return self.api_client.list_all_resources()

    def list_permission_by_resource(self, resource: str) -> OkErr:
        return self.api_client.list_resource_permissions(resource)

# -------------------------------------------------------------------------------------------------------------------- #
class ProxyClient(DevClient):
    """
        ProxyClient will have access to all the methods apiclient used by DevClient. Instead of authenticating
    using credentials, you can directly enter env and user token to call the apis on proxy, using the
    ProxyClient in place of RyghtClient or DevClient. This will eliminate token validation check since we
    won't be taking advantage of the TokenManager's Authenticate function, since the token is assumed to be valid at
    the time of client creation.
    """
    def __init__(
            self,
            /,
            token_str: str,
            *,
            env: str,
            token_type: str = 'Bearer',

    ):
        self.api_client: ApiProxyClient = ApiProxyClient(
            token_str=token_str,
            env=env,
            token_type=token_type,
        )

# -------------------------------------------------------------------------------------------------------------------- #
