from enum import Enum
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator


class ToolType(str, Enum):
    PINECONE = "Pinecone"
    PG_VECTOR = "PGVector"
    SQL_DATABASE_POSTGRES = "PostgreSQL"
    SQL_DATABASE_BIGQUERY = "BigQuery"
    SQL_DATABASE_MYSQL = "MySQL"
    SQL_DATABASE_MSSQL = "MSSQL"
    SQL_DATABASE_ORACLE = "Oracle"
    OPENAPI = "OpenAPI"


class EmbeddingModelProvider(str, Enum):
    VERTEX_AI_MODEL_GARDEN = "VertexAIModelGarden"
    OPEN_AI = "OpenAI"
    GOOGLE_AI = "GoogleAI"


class OpenAIEmbeddingModelVersion(str, Enum):
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"


class GoogleAIEmbeddingModelVersion(str, Enum):
    EMBEDDING_V1 = "models/embedding-001"
    TEXT_EMBEDDING_004 = "models/text-embedding-004"


class ToolConfigSQLMetadata(BaseModel):
    include_tables: Optional[list[str]]
    exclude_tables: Optional[list[str]]

    @root_validator
    def validate_include_or_exclude_tables(cls, values) -> "ToolConfigSQLMetadata":
        include_tables, exclude_tables = values.get("include_tables"), values.get("exclude_tables")
        if all([include_tables, exclude_tables]):
            raise ValueError("Both include_tables and exclude_tables cannot be provided")
        if not any([include_tables, exclude_tables]):
            raise ValueError("Either include_tables or exclude_tables should be provided")
        return values


class ToolConfigBase(BaseModel):
    type: ToolType


class ToolConfigSQLBase(ToolConfigBase):
    type: Literal[
        ToolType.SQL_DATABASE_POSTGRES,
        ToolType.SQL_DATABASE_BIGQUERY,
        ToolType.SQL_DATABASE_MYSQL,
        ToolType.SQL_DATABASE_MSSQL,
        ToolType.SQL_DATABASE_ORACLE,
    ]
    config_metadata: Optional[ToolConfigSQLMetadata] = Field(default=None)


class EmbeddingModelBase(BaseModel):
    provider: EmbeddingModelProvider


class VertexAIModelGardenEmbeddingModel(EmbeddingModelBase):
    provider: Literal[
        EmbeddingModelProvider.VERTEX_AI_MODEL_GARDEN
    ] = EmbeddingModelProvider.VERTEX_AI_MODEL_GARDEN.value
    project_id: str
    endpoint_id: str
    location: str
    service_account: dict[str, str]


class OpenAIEmbeddingModel(EmbeddingModelBase):
    provider: Literal[EmbeddingModelProvider.OPEN_AI] = EmbeddingModelProvider.OPEN_AI.value
    version: OpenAIEmbeddingModelVersion
    api_key: str


class GoogleAIEmbeddingModel(EmbeddingModelBase):
    provider: Literal[EmbeddingModelProvider.GOOGLE_AI] = EmbeddingModelProvider.GOOGLE_AI.value
    version: GoogleAIEmbeddingModelVersion
    api_key: str


EmbeddingModel = Union[OpenAIEmbeddingModel, GoogleAIEmbeddingModel, VertexAIModelGardenEmbeddingModel]


class ToolConfigSQLDatabasePostgres(ToolConfigSQLBase):
    type: Literal[ToolType.SQL_DATABASE_POSTGRES] = ToolType.SQL_DATABASE_POSTGRES.value
    connection_string: str = Field(pattern=r"^postgresql://")


class ToolConfigSQLDatabaseMySQL(ToolConfigSQLBase):
    type: Literal[ToolType.SQL_DATABASE_MYSQL] = ToolType.SQL_DATABASE_MYSQL.value
    connection_string: str = Field(pattern=r"^mysql://")


class ToolConfigSQLDatabaseMSSQL(ToolConfigSQLBase):
    type: Literal[ToolType.SQL_DATABASE_MSSQL] = ToolType.SQL_DATABASE_MSSQL.value
    connection_string: str = Field(pattern=r"^mssql://")


class ToolConfigSQLDatabaseOracle(ToolConfigSQLBase):
    type: Literal[ToolType.SQL_DATABASE_ORACLE] = ToolType.SQL_DATABASE_ORACLE.value
    connection_string: str = Field(pattern=r"^oracle://")


class ToolConfigBigQuery(ToolConfigSQLBase):
    type: Literal[ToolType.SQL_DATABASE_BIGQUERY] = ToolType.SQL_DATABASE_BIGQUERY.value
    project_id: str
    dataset_id: str
    service_account: dict[str, str]


class ToolConfigPGVector(ToolConfigBase):
    type: Literal[ToolType.PG_VECTOR] = ToolType.PG_VECTOR.value
    connection_string: str
    table_name: str
    db_schema: Optional[str] = None
    embedding_model: EmbeddingModel = Field(..., discriminator="provider")


class ToolConfigPineconeVectorDB(ToolConfigBase):
    type: Literal[ToolType.PINECONE] = ToolType.PINECONE.value
    api_key: str
    index_name: str
    embedding_model: EmbeddingModel = Field(..., discriminator="provider")


class BearerAuthenticationConfig(BaseModel):
    type: Literal["Bearer"]
    token: str


AuthenticationConfig = BearerAuthenticationConfig


class ToolConfigOpenAPI(ToolConfigBase):
    type: Literal[ToolType.OPENAPI] = ToolType.OPENAPI.value
    openapi_schema: dict
    authentication: Optional[AuthenticationConfig] = Field(default=None)


ToolConfig = Union[
    ToolConfigPGVector,
    ToolConfigPineconeVectorDB,
    ToolConfigSQLDatabasePostgres,
    ToolConfigSQLDatabaseMySQL,
    ToolConfigSQLDatabaseMSSQL,
    ToolConfigSQLDatabaseOracle,
    ToolConfigBigQuery,
    ToolConfigOpenAPI,
]

SQL_TOOLS = Union[
    ToolConfigSQLDatabasePostgres,
    ToolConfigSQLDatabaseMySQL,
    ToolConfigSQLDatabaseMSSQL,
    ToolConfigSQLDatabaseOracle,
    ToolConfigBigQuery,
]


class ToolDef(BaseModel):
    name: str
    description: str
    config: ToolConfig


class TableMetadata(BaseModel):
    table_name: str
