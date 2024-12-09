from typing import Optional

from pydantic import BaseModel

from superwise_api.client.models.page import Page
from superwise_api.entities.base import BaseApi
from superwise_api.models.knowledge.knowledge import Knowledge
from superwise_api.models.knowledge.knowledge import UrlKnowledgeMetadata
from superwise_api.models.tool.tool import EmbeddingModel


class KnowledgeApi(BaseApi):
    """
    This class provides methods to interact with the KnowledgeApi API.

    Attributes:
        api_client (ApiClient): An instance of the ApiClient to make requests.
        _model_name (str): The name of the model.
        _resource_path (str): The path of the resource.
        _model_class (KnowledgeApi): The model class.
    """

    _model_name = "knowledgeApi"
    _resource_path = "/v1/knowledge"
    _model_class = Knowledge

    def get_by_id(self, knowledge_id: str, **kwargs) -> dict:
        """
        Gets knowledge by id.

        Args:
            knowledge_id (str): The id of the knowledge.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Knowledge: The knowledge.
        """
        return super().get_by_id(_id=knowledge_id, **kwargs)

    def delete(self, knowledge_id: str, **kwargs) -> None:
        """
        Deletes knowledge.

        Args:
            knowledge_id (str): The id of the knowledge.
            **kwargs: Arbitrary keyword arguments.
        """
        return super().delete(_id=knowledge_id, **kwargs)

    def create(
        self, name: str, knowledge_metadata: UrlKnowledgeMetadata, embedding_model: EmbeddingModel, **kwargs
    ) -> BaseModel:
        """
        Creates new knowledge.

        Args:
            name (str): The name of the knowledge.
            knowledge_metadata (UrlKnowledgeMetadata): URL knowledge params.
            embedding_model (EmbeddingModel): The parameters of the embedding model.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Knowledge: The created knowledge.
        """
        data = dict(name=name, knowledge_metadata=knowledge_metadata.dict(), embedding_model=embedding_model.dict())
        return self.api_client.create(
            resource_path=self._resource_path, model_class=Knowledge, model_name=self._model_name, data=data, **kwargs
        )

    def get(self, page: Optional[int] = None, size: Optional[int] = None, **kwargs) -> Page:
        """
        Retrieves knowledge. Filter if any of the parameters are provided.

        Args:
            page (int, optional): The page number.
            size (int, optional): The size of the page.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Page: A page of knowledge.
        """
        query_params = {
            k: v
            for k, v in dict(
                page=page,
                size=size,
            ).items()
            if v is not None
        }
        return self.api_client.get(
            resource_path=self._resource_path,
            model_class=Knowledge,
            model_name=self._model_name,
            query_params=query_params,
            **kwargs
        )

    def update(self, knowledge_id: str, name: Optional[str] = None, **kwargs) -> BaseModel:
        """
        Updates knowledge.

        Args:
            knowledge_id (str): The id of the knowledge.
            name (str, optional): The new name of the knowledge.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Knowledge: The updated knowledge.
        """
        if not any([name]):
            raise ValueError("At least one parameter must be provided to update the knowledge.")

        data = {k: v for k, v in dict(name=name).items() if v is not None}
        return self.api_client.update(
            resource_path=self._resource_path,
            model_name=self._model_name,
            model_class=Knowledge,
            entity_id=knowledge_id,
            data=data,
            **kwargs
        )
