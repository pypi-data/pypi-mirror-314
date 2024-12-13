from typing import Dict
from typing import Optional

from pydantic import conint

from superwise_api.client.models.page import Page
from superwise_api.entities.base import BaseApi
from superwise_api.models.dashboard.dashboard import Dashboard
from superwise_api.models.dashboard.dashboard import WidgetMeta


class DashboardApi(BaseApi):
    """
    This class provides methods to interact with the Dashboard API.

    Args:
        api_client (SuperwiseClient): An instance of the ApiClient to make requests.
    """

    _model_name = "dashboard"
    _resource_path = "/v1/dashboards"
    _model_class = Dashboard

    def create(self, name: str, **kwargs) -> Dashboard:
        """
        Creates a new dashboard.

        Args:
            name (str): The name of the dashboard.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Dashboard: The created dashboard.
        """
        data = {
            "name": name,
        }
        return self.api_client.create(
            resource_path=self._resource_path,
            model_name=self._model_name,
            model_class=self._model_class,
            data=data,
            **kwargs,
        )

    def get(
        self,
        name: Optional[str] = None,
        page: Optional[conint(strict=True, ge=1)] = None,
        size: Optional[conint(strict=True, le=500, ge=1)] = None,
        **kwargs
    ) -> Page:
        """
        Gets all dashboards.

        Args:
            name (str, optional): The name of the dashboard.
            page (int, optional): The page number.
            size (int, optional): The size of the page.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Page: A page of sources.
        """
        query_params = {k: v for k, v in dict(name=name, page=page, size=size).items() if v is not None}
        return self.api_client.get(
            resource_path=self._resource_path,
            model_name=self._model_name,
            model_class=self._model_class,
            query_params=query_params,
            **kwargs,
        )

    def update(
        self,
        dashboard_id: str,
        *,
        name: Optional[str] = None,
        positions: Optional[Dict[str, WidgetMeta]] = None,
        **kwargs
    ):
        """
        Updates a dashboard.

        Args:
            dashboard_id (str): The id of the dashboard.
            name (str, optional): The new name of the dashboard.
            positions (dict, optional): The new positions of the widgets.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Dashboard: The updated dashboard.
        """
        if not any([name, positions]):
            raise ValueError("At least one parameter must be provided to update the dashboard.")

        data = {k: v for k, v in dict(name=name, positions=positions).items() if v is not None}
        return self.api_client.update(
            resource_path=self._resource_path,
            entity_id=dashboard_id,
            model_name=self._model_name,
            model_class=self._model_class,
            data=data,
            **kwargs,
        )
