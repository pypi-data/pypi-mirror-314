# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import os
import uuid
import logging

from result import OkErr

from ryght.models import AIModels
from ryght.models import Documents
from ryght.models import Collection
from ryght.models import JsonDocument
from ryght.models import Prompts
from ryght.models import LoincOrder
from ryght.models import LoincCoding

from ryght.configs import Credentials
from ryght.clients.api import ApiClient

from ryght.utils import FlowTypes
from ryght.utils import ModelOperation

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class BaseClient:
    id: uuid.UUID = uuid.uuid4()
    api_client: ApiClient
    organization: str
    environment: str

    def __init__(
            self,
            user_credentials: dict | Credentials = None,
            env='preview',
            env_path: str = None
    ):
        logger.debug(f'Client ID: {self.id}\n\n')
        self.environment = env
        self.api_client = ApiClient(env=env)
        if isinstance(user_credentials, dict):
            self.api_client.token_manager.credentials = Credentials(**user_credentials)
        elif isinstance(user_credentials, Credentials):
            self.api_client.token_manager.credentials = user_credentials
        elif env_path and os.path.isfile(env_path):
            credentials = Credentials(_env_file=env_path)
            self.api_client.token_manager.credentials = credentials

        self.organization = self.api_client.token_manager.credentials.organization
        self.api_client.token_manager.get_new_token()

    def set_credentials(self, user_credentials: dict | Credentials | str = None):
        if isinstance(user_credentials, dict):
            self.api_client.token_manager.credentials = Credentials(**user_credentials)
        elif isinstance(user_credentials, Credentials):
            self.api_client.token_manager.credentials = user_credentials
        elif isinstance(user_credentials, str) and os.path.isfile(user_credentials):
            credentials = Credentials(_env_file=user_credentials)
            self.api_client.token_manager.credentials = credentials

        # Document Collection  ------->

    def list_collections(self, query_params: dict | None = None) -> list[Collection]:
        return self.api_client.search_collections(query_params)

    def create_new_collection(
            self,
            collection_name: str,
            metadata: dict | None = None,
            tag_ids: list[str] | None = None,
            is_externally_chunked: bool = False,
    ) -> str:
        return self.api_client.create_new_collection(
            collection_name,
            metadata,
            tag_ids,
            is_externally_chunked
        )

    def get_collection_by_id(self, collection_id: str) -> Collection:
        return self.api_client.get_collection_details(collection_id)

    def delete_collection_by_id(self, collection_id: str) -> OkErr:
        return self.api_client.delete_collection_by_id(collection_id)

    # Document import to a collection ----->
    def upload_a_new_doc_to_collection(
            self,
            collection_id: str,
            document_path: str,
    ) -> OkErr:
        return self.api_client.upload_doc_as_json_to_a_document_collection(
            collection_id,
            document_path
        )

    def get_file_by_id(self, file_id: str) -> OkErr:
        return self.api_client.get_file_by_id(file_id)

    def upload_a_new_pdf_to_collection(
            self,
            collection_id: str,
            document_path: str,
            file_name: str
    ):
        return self.api_client.upload_pdf_doc_to_a_document_collection(
            collection_id,
            document_path,
            file_name
        )
    
    def get_status_using_trace_id(self, trace_id: str):
        return self.api_client.track_status(
            trace_id=trace_id
        )

    # Completions ------->
    def completions(
            self,
            input_str: str,
            collection_ids: str | list[str],
            flow: FlowTypes = FlowTypes.SEARCH,
            search_limit: int = 5,
            completion_model_id: str = None,
            document_ids=None,
            ai_tags: list[str] = None
    ):
        if document_ids is None:
            document_ids = []
        return self.api_client.perform_completions(
            input_str,
            collection_ids,
            flow,
            search_limit,
            completion_model_id,
            document_ids=document_ids,
            ai_tags=ai_tags
        )

    def conversations(
            self,
            prompt: Prompts,
            conversation_id: str | None = None,
            collection_ids: str | list[str] | None = None,
            ai_tag_ids: str | list[str] | None = None,
            default_collection: bool = False,
            document_ids: list[str] | None = None,
            copilot_id: str | None = None,
        ) -> OkErr:
        return self.api_client.converse(
            prompt,
            conversation_id,
            collection_ids,
            ai_tag_ids,
            default_collection,
            document_ids,
            copilot_id,
        )

    # Ai Models ------->
    def list_models(self) -> list[AIModels]:
        return self.api_client.get_ai_models()

    def get_model(self, model_id: str = None) -> AIModels:
        return self.api_client.get_ai_model_by_id(model_id)

    def get_model_by_operation(self, operation: ModelOperation = ModelOperation.EMBEDDING) -> list[AIModels]:
        return self.api_client.get_ai_models_by_operation(operation)

    # Documents ------->
    def upload_new_document(self, documents_path: str, file_name: str, tag_ids: list = None) -> str:
        return self.api_client.upload_documents(
            documents_path,
            file_name,
            tag_ids=tag_ids
        )

    def get_default_collections(self) -> list[Documents]:
        return self.api_client.get_document_collection()

    def get_document_by_id(self, document_id: str) -> Documents:
        return self.api_client.get_document_by_id(document_id)

    def delete_document_by_id(self, document_id: str) -> Documents:
        return self.api_client.delete_document_by_id(document_id)

    def rename_document(self, document_id: str, new_name: str) -> str:
        return self.api_client.rename_document(document_id, new_name)

    def search_loinc_codes(
            self,
            panel: LoincOrder = None,
            analytes: list[LoincOrder] = None,
            range_num: int = 100,
            analyte_only: bool = False,
            do_count_match: bool = False
        ) -> OkErr:
        return self.api_client.get_loinc_coding(panel, analytes, range_num, analyte_only, do_count_match)
    
# -------------------------------------------------------------------------------------------------------------------- #
