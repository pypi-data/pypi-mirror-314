import uuid
from typing import Optional

from pydantic import conint

from superwise_api.client.models.page import Page
from superwise_api.entities.base import BaseApi
from superwise_api.models.dataset.dataset import Dataset
from superwise_api.models.dataset_source.dataset_source import DatasetSource
from superwise_api.models.dataset_source.dataset_source import IngestType
from superwise_api.models.model import Model


class DatasetApi(BaseApi):
    """
    This class provides methods to interact with the Dataset API.

    Attributes:
        api_client (ApiClient): An instance of the ApiClient to make requests.
        _model_name (str): The name of the model.
        _resource_path (str): The path of the resource.
        _dataset_source_model_name (str): The name of the dataset source model.
        _dataset_source_path (str): The path of the dataset source resource.
    """

    _model_name = "dataset"
    _dataset_source_model_name = "dataset_source"
    _resource_path = "/v1/datasets"
    _dataset_source_path = "/v1/dataset-sources"
    _model_class = Dataset

    def delete(self, dataset_id: str, **kwargs):
        """
        Deletes a dataset.

        Args:
            dataset_id (str): The id of the dataset to delete.
            **kwargs: Arbitrary keyword arguments.
        """
        return super().delete(_id=dataset_id, **kwargs)

    def get_by_id(self, dataset_id: str, **kwargs) -> Dataset:
        """
        Retrieves a dataset by its id.

        Args:
            dataset_id (str): The id of the dataset to retrieve.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Dataset: The retrieved dataset.
        """
        return super().get_by_id(_id=dataset_id, **kwargs)

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        id: Optional[str] = None,
        schema: Optional[dict] = None,
        **kwargs,
    ) -> Dataset:
        """
        Creates a new dataset.

        Args:
            name (str): The name of the dataset.
            description (str, optional): The description of the dataset.
            id (str, optional): The id of the dataset.
            schema (dict, optional): The schema of the dataset.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Dataset: The created dataset.
        """
        if not id:
            id = str(uuid.uuid4())
        data = {
            k: v for k, v in dict(name=name, description=description, id=id, schema=schema).items() if v is not None
        }
        return self.api_client.create(
            resource_path=self._resource_path, model_name=self._model_name, model_class=Dataset, data=data, **kwargs
        )

    def get(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        id: Optional[str] = None,
        model_version_id: Optional[str] = None,
        created_by: Optional[str] = None,
        page: Optional[conint(strict=True, ge=1)] = None,
        size: Optional[conint(strict=True, le=500, ge=1)] = None,
        **kwargs,
    ) -> Page:
        """
        Retrieves datasets based on the provided filters.

        Args:
            name (Optional[str], optional): The name of the dataset to retrieve.
            description (Optional[str], optional): The description of the dataset to retrieve.
            id (Optional[str], optional): The id of the dataset to retrieve.
            model_version_id (Optional[str], optional): The model version id of the dataset to retrieve.
            created_by (Optional[str], optional): The creator of the dataset to retrieve.
            page (Optional[conint(strict=True, ge=1)], optional): The page number to retrieve.
            size (Optional[conint(strict=True, le=500, ge=1)], optional): The number of datasets to retrieve per page.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Page: A page of datasets.
        """
        query_params = {
            k: v
            for k, v in dict(
                name=name,
                description=description,
                id=id,
                model_version_id=model_version_id,
                created_by=created_by,
                page=page,
                size=size,
            ).items()
            if v is not None
        }
        return self.api_client.get(
            resource_path=self._resource_path,
            model_name=self._model_name,
            model_class=Dataset,
            query_params=query_params,
            **kwargs,
        )

    @BaseApi.raise_exception
    def search(
        self,
        prefix: str,
        page: Optional[conint(strict=True, ge=1)] = None,
        size: Optional[conint(strict=True, le=500, ge=1)] = None,
        **kwargs,
    ) -> Page:
        """
        Searches for datasets based on a prefix.

        Args:
            prefix (str): The prefix to search for.
            page (Optional[conint(strict=True, ge=1)], optional): The page number to retrieve.
            size (Optional[conint(strict=True, le=500, ge=1)], optional): The number of datasets to retrieve per page.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Page: A page of datasets.
        """
        kwargs.update({k: v for k, v in dict(prefix=prefix, page=page, size=size).items() if v is not None})
        return self.api_client.get(resource_path=f"{self._resource_path}/search", **kwargs)

    def update(
        self,
        dataset_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        id: Optional[str] = None,
        schema: Optional[dict] = None,
        **kwargs,
    ) -> Dataset:
        """
        Updates a dataset.

        Args:
            dataset_id (str): The id of the dataset to update.
            name (str, optional): The new name of the dataset.
            description (str, optional): The new description of the dataset.
            id (str, optional): The new id of the dataset.
            schema (dict, optional): The new schema of the dataset.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Dataset: The updated dataset.
        """
        if not any([name, description, id, schema]):
            raise ValueError("At least one parameter must be provided to update the dataset.")

        data = {
            k: v for k, v in dict(name=name, description=description, id=id, schema=schema).items() if v is not None
        }
        return self.api_client.update(
            resource_path=self._resource_path,
            entity_id=dataset_id,
            model_name=self._model_name,
            model_class=Dataset,
            data=data,
            **kwargs,
        )

    @BaseApi.raise_exception
    def connect_to_source(self, dataset_id: str, source_id: str, ingest_type: IngestType, folder: str, **kwargs):
        """
        Connects a dataset to a source.

        Args:
            dataset_id (str): The id of the dataset to connect.
            source_id (str): The id of the source to connect to.
            ingest_type (IngestType): The ingestion type.
            folder (str): The folder path to connect to inside the bucket. e.g. "folder1/folder2".
            **kwargs: Arbitrary keyword arguments.
        """
        data = dict(dataset_id=dataset_id, source_id=source_id, ingest_type=ingest_type, folder=folder)
        return self.api_client.create(
            resource_path=self._dataset_source_path,
            model_name=self._dataset_source_model_name,
            model_class=DatasetSource,
            data=data,
            **kwargs,
        )

    @BaseApi.raise_exception
    def get_connected_sources(self, dataset_id: str, **kwargs) -> Page:
        """
        Retrieves the sources connected to a dataset.

        Args:
            dataset_id (str): The id of the dataset to retrieve the connected sources for.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Page: A page of connected sources.
        """
        return self.api_client.get(
            resource_path=f"{self._dataset_source_path}",
            model_name=self._dataset_source_model_name,
            model_class=DatasetSource,
            query_params={"dataset_id": dataset_id},
            **kwargs,
        )

    @BaseApi.raise_exception
    def get_models_for_dataset(
        self,
        dataset_id: str,
        **kwargs,
    ) -> Page:
        """
        Retrieves all models for a dataset.

        Args:
            dataset_id (str): The id of the dataset.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Page: A page of models.
        """
        return self.api_client.get(
            resource_path=f"{self._resource_path}/{dataset_id}/models",
            model_name=self._model_name,
            model_class=Dataset,
            **kwargs,
        )
