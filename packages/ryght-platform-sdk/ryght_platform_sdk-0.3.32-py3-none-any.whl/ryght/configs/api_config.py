"""
    :param FileName     :   api_config.py
    :param Author       :   Sudo
    :param Date         :   03/07/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   # TODO
    :param Description  :   # TODO
"""
# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import yaml
import logging
import importlib.util

from pydantic import BaseModel, ConfigDict, Field

# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class SummaryEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class CompletionsEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class MetadataTemplatesEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class TagEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")
    by_id: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class PromptTemplatesEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")
    search: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class VariantEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    search: str = Field(..., description="")
    abstract: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class NotesEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")
    by_id: str = Field(..., description="")
    search: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class DocumentEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    by_id: str = Field(..., description="")
    search: str = Field(..., description="")
    upload: str = Field(..., description="")
    pre_chunked: str = Field(..., description="API for pre chunked document upload")


# -------------------------------------------------------------------------------------------------------------------- #
class ModelSpecificationEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")
    by_id: str = Field(..., description="")
    operation: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class ConversationsEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")
    by_id: str = Field(..., description="")
    feedback: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class ChunkEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    embed: str = Field(..., description="")
    chunk: str = Field(..., description="")
    chunk_and_embed: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class ChunkSpecificationEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")
    by_id: str = Field(..., description="")
    strategies: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class AiTagEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")
    by_id: str = Field(..., description="")
    search: str = Field(..., description="")
    associate: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class DocumentCollectionEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base: str = Field(..., description="")
    by_id: str = Field(..., description="")
    search: str = Field(..., description="")
    re_process: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class FileStoreEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    base_url: str = Field(..., description="")
    file_by_id: str = Field(..., description="")
    file_search: str = Field(..., description="")
    pdf_file: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class PermissionManagementEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    for_users: str = Field(..., description="")
    resources: str = Field(..., description="")
    for_members: str = Field(..., description="")
    permissions: str = Field(..., description="")
    permissions_users_in_org: str = Field(..., description="")
    permissions_members_of_org: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class OrganizationEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    search: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class MedicalCodingEndpoint(BaseModel):
    model_config = ConfigDict(extra='ignore')

    loinc_coding: str = Field(..., description="")


# -------------------------------------------------------------------------------------------------------------------- #
class ApiEndpoints(BaseModel):
    model_config = ConfigDict(
        extra='ignore',
        protected_namespaces=()
    )

    base_url: str = Field(..., description="")
    auth_token_url: str = Field(..., description="")

    notes: NotesEndpoint
    chunk: ChunkEndpoint
    ai_tag: AiTagEndpoint
    tag_apis: TagEndpoint
    variant: VariantEndpoint
    summary: SummaryEndpoint
    document: DocumentEndpoint
    file_store: FileStoreEndpoint
    completions: CompletionsEndpoint
    organization: OrganizationEndpoint
    conversations: ConversationsEndpoint
    prompt_templates: PromptTemplatesEndpoint
    metadata_templates: MetadataTemplatesEndpoint
    model_specification: ModelSpecificationEndpoint
    chunk_specification: ChunkSpecificationEndpoint
    document_collection: DocumentCollectionEndpoint
    permission_management: PermissionManagementEndpoint
    medical_coding: MedicalCodingEndpoint

    @staticmethod
    def load_api_endpoints(
            path_to_api_configs_yaml: str = None,
            env: str = 'production'
    ):
        if path_to_api_configs_yaml is None:
            package_name = 'ryght.configs'
            spec = importlib.util.find_spec(package_name)

            # Add dev / prod switch options
            if spec is not None:
                path_to_api_configs_yaml = spec.submodule_search_locations[0] + '/api_endpoints.yaml'
                logger.debug(f"api_endpoints.yaml file found @ {path_to_api_configs_yaml}")
            else:
                logger.error(f"api_endpoints.yaml file not found")

        with open(path_to_api_configs_yaml, 'r') as file:
            config = yaml.safe_load(file)['api_configs']
            env_var = config['env'][env]
            endpoints = config['endpoints']
            return ApiEndpoints(**{
                **env_var,
                **endpoints
            })
# -------------------------------------------------------------------------------------------------------------------- #
