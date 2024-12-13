from typing import Optional
from typing import Sequence

from pydantic import conint

from superwise_api.client.api_client import ApiClient
from superwise_api.client.models.page import Page
from superwise_api.entities.base import BaseApi
from superwise_api.models.application.application import Application
from superwise_api.models.application.application import ModelLLM
from superwise_api.models.application.application import ToolDef
from superwise_api.models.application.playground import AskResponsePayload
from superwise_api.models.context.context import Context


class ApplicationApi(BaseApi):
    """
    This class provides methods to interact with the Application API.

    Attributes:
        api_client (ApiClient): An instance of the ApiClient to make requests.
        _model_name (str): The name of the model.
        _resource_path (str): The path of the resource.
    """

    _model_name = "application"
    _resource_path = "/v1/applications"
    _model_class = Application

    def __init__(self, api_client: ApiClient) -> None:
        """
        Initializes the DatasetApi class.

        Args:
            api_client (ApiClient): An instance of the SuperwiseApiClient to make requests.
        """
        super().__init__(api_client)
        self._playground_resource_path = "/v1/application-playground"

    def create(
        self,
        name: str,
        tools: Sequence[ToolDef],
        llm_model: Optional[ModelLLM],
        contexts: Optional[Sequence[Context]] = None,
        prompt: Optional[str] = None,
        show_cites: bool = False,
        **kwargs
    ) -> Application:
        """
        Creates a new application.

        Args:
            name (str): The name of the application.
            tools (Sequence[ToolDef]): The tools connected to the application.
            contexts (Optional[Sequence[Context]]): The contexts connected to the application.
            llm_model (ModelLLM, optional): The model of the application.
            prompt (str, optional): The prompt of the application.
            show_cites (bool, optional): Whether to show cites or not.

        Returns:
            Application: The created application.
        """

        payload = {
            "name": name,
            "tools": [tool.dict() for tool in tools],
            "contexts": [context.dict() for context in contexts] if contexts else [],
            "model": llm_model.dict() if llm_model else None,
            "prompt": prompt,
            "show_cites": show_cites,
        }
        return self.api_client.create(
            resource_path=self._resource_path,
            model_name=self._model_name,
            model_class=Application,
            data=payload,
            **kwargs,
        )

    def put(
        self,
        application_id: str,
        *,
        name: str,
        tools: Optional[Sequence[ToolDef]] = None,
        contexts: Optional[Sequence[Context]] = None,
        llm_model: Optional[ModelLLM] = None,
        prompt: Optional[str] = None,
        show_cites: bool = False,
        **kwargs
    ) -> Application:
        """
        Updates an application.

        Args:
            application_id (str): The id of the application.
            name (str): The name of the application.
            tools (Optional[Sequence[ToolDef]]): The tools connected to the application.
            contexts (Optional[Sequence[Context]]): The contexts connected to the application.
            llm_model (ModelLLM, optional): The model of the application.
            prompt (str, optional): The prompt of the application.
            show_cites (bool, optional): Whether to show cites or not.

        Returns:
            Application: The updated application.
        """
        if not any([name, tools, contexts, llm_model, prompt, show_cites]):
            raise ValueError("At least one of the parameters must be provided to update an application.")

        data = dict(
            name=name,
            tools=[tool.dict() for tool in tools] if tools else [],
            contexts=[context.dict() for context in contexts] if contexts else [],
            model=llm_model.dict() if llm_model else None,
            prompt=prompt,
            show_cites=show_cites,
        )
        return self.api_client.replace(
            resource_path=self._resource_path,
            model_name=self._model_name,
            entity_id=application_id,
            model_class=Application,
            data=data,
            **kwargs,
        )

    def get(
        self,
        name: Optional[str] = None,
        created_by: Optional[str] = None,
        prompt: Optional[str] = None,
        dataset_id: Optional[str] = None,
        page: Optional[conint(strict=True, ge=1)] = None,
        size: Optional[conint(strict=True, le=500, ge=1)] = None,
        **kwargs
    ) -> Page:
        """
        Gets applications. Filter if any of the parameters are provided.

        Args:
            name (str, optional): The name of the application.
            created_by (str, optional): The creator of the application.
            prompt (str, optional): The prompt of the application.
            dataset_id (str, optional): The id of the dataset.
            page (int, optional): The page number.
            size (int, optional): The size of the page.

        Returns:
            Page: A page of applications.
        """

        query_params = {
            k: v
            for k, v in dict(
                name=name,
                created_by=created_by,
                prompt=prompt,
                dataset_id=dataset_id,
                page=page,
                size=size,
            ).items()
            if v is not None
        }
        return self.api_client.get(
            resource_path=self._resource_path,
            model_name=self._model_name,
            model_class=Application,
            query_params=query_params,
            **kwargs,
        )

    @BaseApi.raise_exception
    def test_model_connection(self, llm_model: ModelLLM, **kwargs):
        """
        Tests the connection to the model. Raises exception on fail.

        Args:
            llm_model (ModelLLM): The model to test.
        """
        response_types_map = {"204": None, "422": "HTTPValidationError"}
        return self.api_client.post(
            resource_path=self._resource_path + "/test-model-connection",
            data=llm_model.dict(),
            response_types_map=response_types_map,
            **kwargs,
        )

    @BaseApi.raise_exception
    def test_tool_connection(self, tool: ToolDef, **kwargs):
        """
        Tests the connection to the tool. Raises exception on fail.

        Args:
            tool (ToolDef): The tool to test.
        """
        response_types_map = {"204": None, "422": "HTTPValidationError"}
        return self.api_client.post(
            resource_path=self._resource_path + "/test-tool-connection",
            data=tool.dict(),
            response_types_map=response_types_map,
            **kwargs,
        )

    @BaseApi.raise_exception
    def ask_playground(
        self,
        input: str,
        llm_model: ModelLLM,
        tools: Sequence[ToolDef],
        contexts: Optional[Sequence[Context]] = None,
        chat_history: Optional[Sequence[dict]] = None,
        prompt: Optional[str] = None,
        show_cites: bool = False,
        **kwargs
    ) -> AskResponsePayload:
        """
        Performs ask request in playground mode.

        Args:
            input (str): The input to the model.
            llm_model (ModelLLM): The model of the application.
            tools (Sequence[ToolDef]): The tools connected to the application.
            contexts (Optional[Sequence[Context]]): The contexts connected to the application.
            chat_history (Sequence[dict], optional): The chat history.
            prompt (str, optional): The prompt of the application.
            show_cites (bool, optional): Whether to show cites or not.

        Returns:
            AskResponsePayload: The response payload.
        """
        payload = {
            "config": {
                "model": llm_model.dict(),
                "prompt": prompt,
                "tools": [tool.dict() for tool in tools],
                "contexts": [context.dict() for context in contexts] if contexts else [],
                "show_cites": show_cites,
            },
            "input": input,
            "chat_history": chat_history or [],
        }
        response_types_map = {"200": AskResponsePayload, "422": "HTTPValidationError"}
        return self.api_client.post(
            resource_path=self._playground_resource_path + "/ask",
            data=payload,
            response_types_map=response_types_map,
            **kwargs,
        )
