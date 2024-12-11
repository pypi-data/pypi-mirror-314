"""
    :param FileName     :   test_data_models.py
    :param Author       :   Sudo
    :param Date         :   02/1/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   # TODO
    :param Description  :   # TODO
"""
import importlib.util
# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import yaml
import logging

from typing import Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, ConfigDict, model_validator, Field

# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class Token(BaseModel):
    """
    A data class that holds authorization token information
    """
    model_config = ConfigDict(extra='ignore')

    token_type: str | None
    expires_in: int | None
    access_token: str | None
    refresh_token: str | None
    refresh_expires_in: int | None
    token_expiry: datetime
    refresh_expiry: datetime

    @property
    def authorization_param(self) -> str:
        if self.access_token:
            return (lambda: self.token_type + ' ' + self.access_token)()
        else:
            return None

    @staticmethod
    def init_as_none():
        return Token(
            **{
                'token_type': None,
                'expires_in': 5,
                'access_token': None,
                'refresh_token': None,
                'refresh_expires_in': 5
            }
        )

    @model_validator(mode='before')
    @classmethod
    def compute_expiration(cls, params: Any) -> Any:
        """

        :param params:
        :return:
        """
        assert 'expires_in' and 'refresh_expires_in' in params
        params['token_expiry'], params['refresh_expiry'] = Token.set_expiration(
            expires_in=params['expires_in'],
            refresh_expires_in=params['refresh_expires_in']
        )
        return params

    @staticmethod
    def set_expiration(expires_in: int, refresh_expires_in: int) -> tuple:
        """

        :param expires_in:
        :param refresh_expires_in:
        :return:
        """
        now = datetime.utcnow()
        return now + timedelta(seconds=expires_in), now + timedelta(seconds=refresh_expires_in)


# -------------------------------------------------------------------------------------------------------------------- #

class Collection(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str = Field(
        ...,
        description='A unique identifier for the collection'
    )
    name: str = Field(
        ...,
        description='The name of the collection'
    )
    documents_count: Optional[int] = Field(
        None,
        alias='documentsCount',
        description='The number of documents in the collection'
    )
    empty_document_count: Optional[int] = Field(
        None,
        alias='emptyDocumentCount',
        description='The number of documents in the collection that are empty'
    )
    parsing_failed_document_count: Optional[int] = Field(
        None,
        alias='parsingFailedDocumentCount',
        description='The number of documents in the collection that failed to parse'
    )
    un_chunked_document_count: Optional[int] = Field(
        None,
        alias='unChunkedDocumentCount',
        description='The number of documents in the collection that are unchunked'
    )
    in_chunking_process_document_count: Optional[int] = Field(
        None,
        alias='inChunkingProcessDocumentCount',
        description='The number of documents in the collection that are in chunking process document count'
    )
    chunk_failed_document_count: Optional[int] = Field(
        None,
        alias='chunkFailedDocumentCount',
        description='The number of documents in the collection that are failed to chunk'
    )
    unembedded_document_count: Optional[int] = Field(
        None,
        alias='unEmbeddedDocumentCount',
        description='The number of documents in the collection that are not embedded'
    )
    in_embedding_process_document_count: Optional[int] = Field(
        None,
        alias='inEmbeddingProcessDocumentCount',
        description='The number of documents in the collection in embedded process'
    )
    embedding_failed_document_count: Optional[int] = Field(
        None,
        alias='embeddingFailedDocumentCount',
        description='The number of documents in the collection failed to embed'
    )
    states: Optional[list[str]] = Field(
        None,
        description='The collection states'
    )
    tags: list = Field(
        ...,
        description='A list of collection tags'
    )
    created_at: Optional[datetime] = Field(
        None,
        alias='createdAt',
        description='The date when the collection was created on'
    )
    default: bool = False
    embedding_models: list["AIModels"] = Field(
        ...,
        alias='embeddingModels',
        description='A list of embedding models'
    )


# -------------------------------------------------------------------------------------------------------------------- #

class CompletionsResponse(BaseModel):
    model_config = ConfigDict(extra='ignore')

    answer: str | None
    embeddings: list | None
    citations: dict | None

    @model_validator(mode='before')
    @classmethod
    def transform_data(cls, params: Any) -> Any:
        """

        :param params:
        :return:
        """
        if 'embeddings' not in params:
            params['embeddings'] = None
        if 'answer' not in params:
            params['answer'] = None
        if 'citations' not in params:
            params['citations'] = None

        return params

    @staticmethod
    def init_with_none():
        return CompletionsResponse(**{'answer': None, 'embeddings': None, 'citations': None})


# -------------------------------------------------------------------------------------------------------------------- #

class TraceStatus(BaseModel):
    model_config = ConfigDict(extra='ignore')

    status: str
    message: str


# -------------------------------------------------------------------------------------------------------------------- #

class AIModels(BaseModel):
    model_config = ConfigDict(extra='allow')
    id: str = Field(
        ...,
        description='A unique identifier for the model'
    )
    name: str = Field(
        ...,
        description='The name of the model'
    )


# -------------------------------------------------------------------------------------------------------------------- #

class Documents(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str
    name: str
    states: Optional[list[str]] = None
    content: Optional[str] = None


# -------------------------------------------------------------------------------------------------------------------- #
class ChunkedDocumentsMetadata(BaseModel):
    model_config = ConfigDict(extra='allow')

    doi: str = Field(
        ...,
        description='URL or path to view the document online'
    )
    source_path: str = Field(
        ...,
        alias='source',
        description='The url or link to the location where the document can be retrieved'
    )
    extra_fields: dict = Field(
        ...,
        alias='extraFields',
        description='Store extra information relevant to chunked document in here'
    )


# -------------------------------------------------------------------------------------------------------------------- #
class ChunkedDocumentsCollectionsMetadata(BaseModel):
    model_config = ConfigDict(extra='ignore')

    source: str = Field(
        ...,
        description='From whom/where the collection is sourced from'
    )
    extra_fields: dict = Field(
        ...,
        alias='extraFields',
        description='Store extra information relevant to collection in here'
    )


# -------------------------------------------------------------------------------------------------------------------- #
class ChunksOfDocumentContent(BaseModel):
    model_config = ConfigDict(extra='ignore')

    content: str = Field(
        ...,
        description='chunk of a given document'
    ),
    order: int = Field(
        ...,
        ge=-1,
        description='order of the chunk within a document',
    ),
    extra_fields: dict = Field(
        ...,
        alias='extraFields',
        description='Other extra information relevant to the chunk and its specification goes here'
    )


# -------------------------------------------------------------------------------------------------------------------- #

class JsonDocument(BaseModel):
    model_config = ConfigDict(extra='ignore')

    name: str = Field(
        ...,
        description='Name of the document'
    ),
    content: str = Field(
        ...,
        description="Whole content of the document that's been chunked"
    ),
    metadata: ChunkedDocumentsMetadata = Field(
        ...,
        description='Metadata about the document'
    )


# -------------------------------------------------------------------------------------------------------------------- #
class ChunkedDocument(JsonDocument):
    name: str = Field(
        ...,
        description='Name of the document'
    )
    chunks: list[ChunksOfDocumentContent] = Field(
        ...,
        description='List of chunks of a given document'
    )
    metadata: ChunkedDocumentsMetadata = Field(
        ...,
        description='Metadata about the chunks in the document'
    )


# -------------------------------------------------------------------------------------------------------------------- #

class ChunkedDocumentCollection(BaseModel):
    model_config = ConfigDict(extra='ignore')

    collectionId: str = Field(
        ...,
        description='Name of the collection the docs belongs to',
        alias='collectionName'
    )
    chunk_specification: dict = Field(
        default={
            "name": "EXTERNAL_SPECIFICATION",
            "description": "Custom chunk description"
        },
        description='Chunk specification for the chunked documents, by default its set to External Specification',
        alias='chunkSpecification')
    metadata: ChunkedDocumentsCollectionsMetadata = Field(
        ...,
        description='Metadata about the collection'
    )

    documents: list[ChunkedDocument] = Field(
        ...,
        description='List of chunked Documents'
    )


# -------------------------------------------------------------------------------------------------------------------- #
class ConversationResponseCollection(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str = Field(
        ...,
        description='collection id'
    )
    name: str = Field(
        ...,
        description='collection name'
    )


# -------------------------------------------------------------------------------------------------------------------- #
class ConversationResponseDocuments(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str = Field(
        ...,
        description='collection id'
    )
    name: str = Field(
        ...,
        description='collection name'
    )


# -------------------------------------------------------------------------------------------------------------------- #
class ConversationResponseEmbeddings(BaseModel):
    model_config = ConfigDict(extra='ignore')

    content: str = Field(
        ...,
        description='Content of the embeddings that matched'
    )
    cosine_distance: str = Field(
        ...,
        description='distance score of the embeddings',
        alias='cosineDistance'
    )
    document: dict = Field(
        ...,
        description='document of the embeddings'
    )


# -------------------------------------------------------------------------------------------------------------------- #
class ConversationResponse(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str = Field(
        ...,
        description='Chat ID'
    )
    conversation_id: str = Field(
        ...,
        alias='conversationId',
        description='Conversation ID'
    )
    question: str = Field(
        ...,
        description='Question Asked.'
    )
    answer: str = Field(
        ...,
        description='Answer we got from the conversation service'
    )
    created_at: str = Field(
        ...,
        description='time the conversation was created',
        alias='createdAt'
    )


    collections: list[ConversationResponseCollection] = Field(
        [],
        description='List of collections the conversation is based on'
    )

    documents: list[ConversationResponseDocuments] = Field(
        [],
        description='List of documents the conversation is based on'
    )
    embeddings: list[ConversationResponseEmbeddings] = Field(
        [],
        description='List of embeddings the conversation depends on '
    )

    @model_validator(mode='before')
    @classmethod
    def parse_input_data(cls, params: Any) -> Any:
        if 'collections' in params:
            params['collections'] = ConversationResponse.parse_collections(params['collections'])

        if 'documents' in params:
            params['documents'] = ConversationResponse.parse_documents(params['documents'])

        if 'embeddings' in params:
            params['embeddings'] = ConversationResponse.parse_embeddings(params['embeddings'])

        return params

    @staticmethod
    def parse_collections(collections_list: list[dict]) -> list[ConversationResponseCollection]:
        collections = []
        for collection_info in collections_list:
            collections.append(ConversationResponseCollection(**collection_info))
        return collections

    @staticmethod
    def parse_documents(documents_list: list[dict]) -> list[ConversationResponseDocuments]:
        documents = []
        for document_info in documents_list:
            documents.append(ConversationResponseDocuments(**document_info))
        return documents

    @staticmethod
    def parse_embeddings(embeddings_list: list[dict]) -> list[ConversationResponseEmbeddings]:
        embeddings = []
        for embedding_info in embeddings_list:
            embeddings.append(ConversationResponseEmbeddings(**embedding_info))
        return embeddings


# -------------------------------------------------------------------------------------------------------------------- #
class ConversationInfo(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str = Field(
        ...,
        description='Conversation ID'
    )
    name: str = Field(
        ...,
        description='Conversation Name'
    )
    updated_at: str = Field(
        ...,
        description='last update time of the conversation',
        alias='updatedAt'
    )


# -------------------------------------------------------------------------------------------------------------------- #
class Prompts(BaseModel):
    model_config = ConfigDict(extra='ignore')

    question: str = Field(
        ...,
        description='Question Asked.'
    )
    template: Optional[str | None] = Field(
        None,
        description='Prompt templates'
    )
    keywords: Optional[dict | None] = Field(
        None,
        description='Conversation Name'
    )


# -------------------------------------------------------------------------------------------------------------------- #
class OrganizationSearchResponse(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: str = Field(
        ...,
        description='ID of the organization'
    )
    name: str = Field(
        ...,
        description='Name of the Organization'
    )

# -------------------------------------------------------------------------------------------------------------------- #
class LoincOrder(BaseModel):
    model_config = ConfigDict(extra='ignore')

    name: str = Field(
        ...,
        description='Name of loinc order',
    )
    units: Optional[str | None] = Field(
        None,
        description='Units of loinc order'
    )

# -------------------------------------------------------------------------------------------------------------------- #
class LoincCoding(BaseModel):
    model_config = ConfigDict(extra='ignore')

    loinc_id: Optional[str | None] = Field(
        ...,
        description='Loinc id',
        alias='loincId'
    )
    short_name: Optional[str | None] = Field(
        ...,
        description='Short Name',
        alias='shortName'
    )
    long_common_name: Optional[str | None] = Field(
        ...,
        description='Long Common Name',
        alias='longCommonName'
    )
    display_name: Optional[str | None] = Field(
        ...,
        description='Display Name',
        alias='displayName'
    )
    example_units: Optional[str | None] = Field(
        ...,
        description='Example Units',
        alias='exampleUnits'
    )
    example_ucum_units: Optional[str | None] = Field(
        ...,
        description='Example Ucum Units',
        alias='exampleUcumUnits'
    )
    definition_description: Optional[str | None] = Field(
        ...,
        description='Definition Description',
        alias='definitionDescription'
    )
    panel_type: Optional[str | None] = Field(
        ...,
        description='Panel Type',
        alias='panelType'
    )
    analyte_score: Optional[float | None] = Field(
        ...,
        description='Analyte Score',
        alias='analyteScore'
    )
    panel_score: Optional[float | None] = Field(
        ...,
        description='Panel Score',
        alias='panelScore'
    )
    overlap_score: Optional[float | None] = Field(
        ...,
        description='Overlap Score',
        alias='overlapScore'
    )
