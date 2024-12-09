from typing import Optional

from pydantic import Field

from superwise_api.models import SuperwiseEntity
from superwise_api.models.knowledge.knowledge import Knowledge
from superwise_api.models.knowledge.knowledge import UrlKnowledgeMetadata
from superwise_api.models.tool.tool import EmbeddingModel


class Context(SuperwiseEntity):
    knowledge_id: str  # should be UUID4 in pydentic v2
    name: str = Field(..., min_length=1, max_length=50)
    knowledge_metadata: UrlKnowledgeMetadata
    embedding_model: EmbeddingModel = Field(..., discriminator="provider")
    description: str

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[Context]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Context.parse_obj(obj)

        _obj = Context.parse_obj(
            {
                "knowledge_id": obj.get("knowledge_id"),
                "name": obj.get("name"),
                "knowledge_metadata": UrlKnowledgeMetadata.parse_obj(obj.get("knowledge_metadata")),
                "embedding_model": obj.get("embedding_model"),
                "description": obj.get("description"),
            }
        )
        return _obj

    @classmethod
    def from_knowledge(cls, knowledge: Knowledge, description: str) -> "Context":
        return Context(
            knowledge_id=str(knowledge.id),
            name=knowledge.name,
            knowledge_metadata=knowledge.knowledge_metadata,
            embedding_model=knowledge.embedding_model,
            description=description,
        )
