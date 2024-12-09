from datetime import datetime
from enum import Enum
from typing import Annotated
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import UUID4

from superwise_api.models import SuperwiseEntity
from superwise_api.models.tool.tool import EmbeddingModel


class KnowledgeType(str, Enum):
    URL = "url"


class UrlKnowledgeMetadata(BaseModel):
    type: Literal[KnowledgeType.URL] = KnowledgeType.URL.value
    url: str
    max_depth: int = Field(..., ge=1, le=5)


class Knowledge(SuperwiseEntity):
    id: UUID4
    name: str = Field(..., min_length=1, max_length=50)
    knowledge_metadata: UrlKnowledgeMetadata
    embedding_model: EmbeddingModel = Field(..., discriminator="provider")
    created_by: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[Knowledge]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Knowledge.parse_obj(obj)

        _obj = Knowledge.parse_obj(
            {
                "id": obj.get("id"),
                "name": obj.get("name"),
                "knowledge_metadata": UrlKnowledgeMetadata.parse_obj(obj.get("knowledge_metadata")),
                "embedding_model": obj.get("embedding_model"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "created_by": obj.get("created_by"),
            }
        )
        return _obj
