from datetime import datetime
from enum import Enum
from typing import Annotated
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Union

from pydantic import BaseModel
from pydantic import confloat
from pydantic import conint
from pydantic import Field
from pydantic import HttpUrl
from pydantic import UUID4

from superwise_api.models import SuperwiseEntity
from superwise_api.models.context.context import Context
from superwise_api.models.tool.tool import ToolDef


class ModelProvider(str, Enum):
    OPENAI = "OpenAI"
    GOOGLE = "GoogleAI"
    VERTEX_AI_MODEL_GARDEN = "VertexAIModelGarden"


class OpenAIModelVersion(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"


class GoogleModelVersion(str, Enum):
    GEMINI_1_5_FLASH = "models/gemini-1.5-flash"
    GEMINI_1_5_FLASH_8B = "models/gemini-1.5-flash-8b"
    GEMINI_1_5 = "models/gemini-1.5-pro"
    GEMINI_PRO = "models/gemini-1.0-pro"


class VertexAIModelGardenVersion(str, Enum):
    PLACEHOLDER = "placeholder"


class ApplicationStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
    DEGRADED = "degraded"


class OpenAIParameters(BaseModel):
    temperature: confloat(ge=0, le=2) = 0
    top_p: confloat(ge=0, le=1) = 1


class GoogleParameters(BaseModel):
    temperature: confloat(ge=0, le=1) = 0
    top_p: confloat(ge=0, le=1) = 1
    top_k: conint(ge=1, le=40) = 40


class VertexAIModelGardenParameters(BaseModel):
    pass


class BaseModelLLM(BaseModel):
    api_token: str

    @classmethod
    def from_dict(cls, obj: dict):
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ModelLLM.parse_obj(obj)

        _obj = ModelLLM.parse_obj(
            {"provider": obj.get("provider"), "version": obj.get("version"), "api_token": obj.get("api_token")}
        )
        return _obj


class OpenAIModel(BaseModelLLM):
    provider: Literal[ModelProvider.OPENAI] = ModelProvider.OPENAI.value
    version: OpenAIModelVersion
    parameters: OpenAIParameters = Field(default_factory=OpenAIParameters)


class GoogleModel(BaseModelLLM):
    provider: Literal[ModelProvider.GOOGLE] = ModelProvider.GOOGLE.value
    version: GoogleModelVersion
    parameters: GoogleParameters = Field(default_factory=GoogleParameters)


class VertexAIModelGardenModel(BaseModelLLM):
    provider: Literal[ModelProvider.VERTEX_AI_MODEL_GARDEN] = ModelProvider.VERTEX_AI_MODEL_GARDEN.value
    version: VertexAIModelGardenVersion
    parameters: VertexAIModelGardenParameters = Field(default_factory=VertexAIModelGardenParameters)


ModelLLM = Annotated[Union[OpenAIModel, GoogleModel, VertexAIModelGardenModel], Field(..., discriminator="provider")]


class Application(SuperwiseEntity):
    id: UUID4
    created_by: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: str
    llm_model: Optional[ModelLLM] = Field(None, alias="model")
    prompt: Optional[str]
    dataset_id: str
    tools: Sequence[ToolDef]
    contexts: Sequence[Context]
    url: HttpUrl
    show_cites: bool = Field(default=False)
    status: ApplicationStatus = ApplicationStatus.UNKNOWN

    @classmethod
    def from_dict(cls, obj: dict):
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Application.parse_obj(obj)

        _obj = Application.parse_obj(
            {
                "id": obj.get("id"),
                "created_by": obj.get("created_by"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "name": obj.get("name"),
                "model": obj.get("model"),
                "prompt": obj.get("prompt"),
                "dataset_id": obj.get("dataset_id"),
                "tools": [ToolDef.parse_obj(tool) for tool in obj.get("tools")],
                "contexts": [Context.parse_obj(context) for context in obj.get("contexts")]
                if obj.get("contexts")
                else [],
                "url": obj.get("url"),
                "show_cites": obj.get("show_cites"),
                "status": obj.get("status"),
            }
        )
        return _obj
