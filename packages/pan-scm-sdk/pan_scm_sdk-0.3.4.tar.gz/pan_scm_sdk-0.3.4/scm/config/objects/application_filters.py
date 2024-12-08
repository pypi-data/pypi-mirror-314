# scm/config/objects/application_filters.py

# Standard library imports
import logging
from typing import List, Dict, Any, Optional

# Local SDK imports
from scm.config import BaseObject
from scm.exceptions import (
    InvalidObjectError,
    MissingQueryParameterError,
)
from scm.models.objects import (
    ApplicationFiltersCreateModel,
    ApplicationFiltersResponseModel,
    ApplicationFiltersUpdateModel,
)


class ApplicationFilters(BaseObject):
    """
    Manages Application filters in Palo Alto Networks' Strata Cloud Manager.
    """

    ENDPOINT = "/config/objects/v1/application-filters"
    DEFAULT_LIMIT = 10000

    def __init__(
        self,
        api_client,
    ):
        super().__init__(api_client)
        self.logger = logging.getLogger(__name__)

    def create(
        self,
        data: Dict[str, Any],
    ) -> ApplicationFiltersResponseModel:
        """
        Creates a new application filter object.

        Returns:
            ApplicationFiltersResponseModel
        """
        # Use the dictionary "data" to pass into Pydantic and return a modeled object
        application_filter = ApplicationFiltersCreateModel(**data)

        # Convert back to a Python dictionary, removing any unset fields
        payload = application_filter.model_dump(exclude_unset=True)

        # Send the updated object to the remote API as JSON
        response: Dict[str, Any] = self.api_client.post(
            self.ENDPOINT,
            json=payload,
        )

        # Return the SCM API response as a new Pydantic object
        return ApplicationFiltersResponseModel(**response)

    def get(
        self,
        object_id: str,
    ) -> ApplicationFiltersResponseModel:
        """
        Gets an application filter object by ID.

        Returns:
            ApplicationFiltersResponseModel
        """
        # Send the request to the remote API
        endpoint = f"{self.ENDPOINT}/{object_id}"
        response: Dict[str, Any] = self.api_client.get(endpoint)

        # Return the SCM API response as a new Pydantic object
        return ApplicationFiltersResponseModel(**response)

    def update(
        self,
        application: ApplicationFiltersUpdateModel,
    ) -> ApplicationFiltersResponseModel:
        """
        Updates an existing application filter object.

        Args:
            application: ApplicationFiltersUpdateModel instance containing the update data

        Returns:
            ApplicationFiltersResponseModel
        """
        # Convert to dict for API request, excluding unset fields
        payload = application.model_dump(exclude_unset=True)

        # Extract ID and remove from payload since it's in the URL
        object_id = str(application.id)
        payload.pop("id", None)

        # Send the updated object to the remote API as JSON
        endpoint = f"{self.ENDPOINT}/{object_id}"
        response: Dict[str, Any] = self.api_client.put(
            endpoint,
            json=payload,
        )

        # Return the SCM API response as a new Pydantic model
        return ApplicationFiltersResponseModel(**response)

    @staticmethod
    def _apply_filters(
        application_filters: List[ApplicationFiltersResponseModel],
        filters: Dict[str, Any],
    ) -> List[ApplicationFiltersResponseModel]:
        """
        Apply client-side filtering to the list of application filters.

        Args:
            application_filters: List of ApplicationFilterResponseModel objects
            filters: Dictionary of filter criteria

        Returns:
            List[ApplicationFiltersResponseModel]: Filtered list of application filters
        """
        filter_criteria = application_filters

        # Filter by category
        if "category" in filters:
            if not isinstance(filters["category"], list):
                raise InvalidObjectError(
                    message="'category' filter must be a list",
                    error_code="E003",
                    http_status_code=400,
                    details={"errorType": "Invalid Object"},
                )
            categories = filters["category"]
            filter_criteria = [
                app
                for app in filter_criteria
                if app.category is not None
                and any(cat in app.category for cat in categories)
            ]

        # Filter by subcategory
        if "subcategory" in filters:
            if not isinstance(filters["subcategory"], list):
                raise InvalidObjectError(
                    message="'subcategory' filter must be a list",
                    error_code="E003",
                    http_status_code=400,
                    details={"errorType": "Invalid Object"},
                )
            subcategories = filters["subcategory"]
            filter_criteria = [
                app
                for app in filter_criteria
                if app.sub_category is not None
                and any(sub in app.sub_category for sub in subcategories)
            ]

        # Filter by technology
        if "technology" in filters:
            if not isinstance(filters["technology"], list):
                raise InvalidObjectError(
                    message="'technology' filter must be a list",
                    error_code="E003",
                    http_status_code=400,
                    details={"errorType": "Invalid Object"},
                )
            technologies = filters["technology"]
            filter_criteria = [
                app
                for app in filter_criteria
                if app.technology is not None
                and any(tech in app.technology for tech in technologies)
            ]

        # Filter by risk
        if "risk" in filters:
            if not isinstance(filters["risk"], list):
                raise InvalidObjectError(
                    message="'risk' filter must be a list",
                    error_code="E003",
                    http_status_code=400,
                    details={"errorType": "Invalid Object"},
                )
            risks = filters["risk"]
            filter_criteria = [
                app
                for app in filter_criteria
                if app.risk is not None and any(risk in app.risk for risk in risks)
            ]

        return filter_criteria

    @staticmethod
    def _build_container_params(
        folder: Optional[str],
        snippet: Optional[str],
        device: Optional[str],
    ) -> dict:
        """Builds container parameters dictionary."""
        return {
            k: v
            for k, v in {"folder": folder, "snippet": snippet, "device": device}.items()
            if v is not None
        }

    def list(
        self,
        folder: Optional[str] = None,
        snippet: Optional[str] = None,
        device: Optional[str] = None,
        **filters,
    ) -> List[ApplicationFiltersResponseModel]:
        """
        Lists application objects with optional filtering.

        Args:
            folder: Optional folder name
            snippet: Optional snippet name
            device: Optional device name
            **filters: Additional filters including:
                - category: List[str] - Filter by category
                - subcategory: List[str] - Filter by subcategory
                - technology: List[str] - Filter by technology
                - risk: List[int] - Filter by risk level
        """
        if folder == "":
            raise MissingQueryParameterError(
                message="Field 'folder' cannot be empty",
                error_code="E003",
                http_status_code=400,
                details={
                    "field": "folder",
                    "error": '"folder" is not allowed to be empty',
                },
            )

        params = {"limit": self.DEFAULT_LIMIT}

        container_parameters = self._build_container_params(
            folder,
            snippet,
            device,
        )

        if len(container_parameters) != 1:
            raise InvalidObjectError(
                message="Exactly one of 'folder', 'snippet', or 'device' must be provided.",
                error_code="E003",
                http_status_code=400,
                details={"error": "Invalid container parameters"},
            )

        params.update(container_parameters)

        response = self.api_client.get(
            self.ENDPOINT,
            params=params,
        )

        if not isinstance(response, dict):
            raise InvalidObjectError(
                message="Invalid response format: expected dictionary",
                error_code="E003",
                http_status_code=500,
                details={"error": "Response is not a dictionary"},
            )

        if "data" not in response:
            raise InvalidObjectError(
                message="Invalid response format: missing 'data' field",
                error_code="E003",
                http_status_code=500,
                details={
                    "field": "data",
                    "error": '"data" field missing in the response',
                },
            )

        if not isinstance(response["data"], list):
            raise InvalidObjectError(
                message="Invalid response format: 'data' field must be a list",
                error_code="E003",
                http_status_code=500,
                details={
                    "field": "data",
                    "error": '"data" field must be a list',
                },
            )

        application_filters = [
            ApplicationFiltersResponseModel(**item) for item in response["data"]
        ]
        return self._apply_filters(application_filters, filters)

    def fetch(
        self,
        name: str,
        folder: Optional[str] = None,
        snippet: Optional[str] = None,
        device: Optional[str] = None,
    ) -> ApplicationFiltersResponseModel:
        """
        Fetches a single application filter by name.

        Args:
            name (str): The name of the application filter to fetch.
            folder (str, optional): The folder in which the resource is defined.
            snippet (str, optional): The snippet in which the resource is defined.
            device (str, optional): The device in which the resource is defined.

        Returns:
            ApplicationFiltersResponseModel: The fetched application filter object as a Pydantic model.
        """
        if not name:
            raise MissingQueryParameterError(
                message="Field 'name' cannot be empty",
                error_code="E003",
                http_status_code=400,
                details={
                    "field": "name",
                    "error": '"name" is not allowed to be empty',
                },
            )

        if folder == "":
            raise MissingQueryParameterError(
                message="Field 'folder' cannot be empty",
                error_code="E003",
                http_status_code=400,
                details={
                    "field": "folder",
                    "error": '"folder" is not allowed to be empty',
                },
            )

        params = {}

        container_parameters = self._build_container_params(
            folder,
            snippet,
            device,
        )

        if len(container_parameters) != 1:
            raise InvalidObjectError(
                message="Exactly one of 'folder', 'snippet', or 'device' must be provided.",
                error_code="E003",
                http_status_code=400,
                details={
                    "error": "Exactly one of 'folder', 'snippet', or 'device' must be provided."
                },
            )

        params.update(container_parameters)
        params["name"] = name

        response = self.api_client.get(
            self.ENDPOINT,
            params=params,
        )

        if not isinstance(response, dict):
            raise InvalidObjectError(
                message="Invalid response format: expected dictionary",
                error_code="E003",
                http_status_code=500,
                details={"error": "Response is not a dictionary"},
            )

        if "id" in response:
            return ApplicationFiltersResponseModel(**response)
        else:
            raise InvalidObjectError(
                message="Invalid response format: missing 'id' field",
                error_code="E003",
                http_status_code=500,
                details={"error": "Response missing 'id' field"},
            )

    def delete(
        self,
        object_id: str,
    ) -> None:
        """
        Deletes an application filter object.

        Args:
            object_id (str): The ID of the object to delete.
        """
        endpoint = f"{self.ENDPOINT}/{object_id}"
        self.api_client.delete(endpoint)
