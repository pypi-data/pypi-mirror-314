import logging
import httpx
from pydantic import TypeAdapter, ValidationError
from typing import Optional, Dict, Any, Union, List
from iemap_mi.models import (ProjectResponse, IEMAPProject, CreateProjectResponse,
                             ProjectQueryModel)
from iemap_mi.settings import settings
from iemap_mi.utils import get_headers


class ProjectHandler:
    def __init__(self, token: Optional[str] = None) -> None:
        """
        Initialize ProjectHandler with base URL and JWT token.

        Args:
            token (Optional[str]): JWT token for authentication. Defaults to None.
        """

        self.token = token

    async def get_projects(self, page_size: int = 10, page_number: int = 1) -> ProjectResponse:
        """
        Get paginated list of projects.

        Args:
            page_size (int): Number of results to return in a single page. Defaults to 10.
            page_number (int): Actual page number returned. Defaults to 1.

        Returns:
            ProjectResponse: Paginated list of projects.
        """
        endpoint = settings.PROJECT_LIST
        params = {'page_size': page_size, 'page_number': page_number}
        headers = get_headers(self.token)

        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return ProjectResponse(**response.json())

    async def create_project(self, project_data: IEMAPProject) -> CreateProjectResponse:
        """
        Create a new project.

        Args:
            project_data (IEMAPProject): Data for the new project.

        Returns:
            CreateProjectResponse: Response containing the inserted ID of the new project.
        """
        endpoint = settings.PROJECT_ADD
        headers = get_headers(self.token)

        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, json=project_data.dict(), headers=headers)
            response.raise_for_status()
            return CreateProjectResponse(**response.json())

    async def add_file_to_project(self, project_id: str, file_path: str, file_name: Optional[str] = None) -> Dict[
        str, Any]:
        """
        Add a file to a project.

        Args:
            project_id (str): The ID of the project to add the file to.
            file_path (str): The path to the file to be uploaded.
            file_name (Optional[str]): The name of the file. Defaults to None.

        Returns:
            Dict[str, Any]: Response from the API.
        """
        endpoint = settings.ADD_FILE_TO_PROJECT
        headers = get_headers(self.token)
        params = {"project_id": project_id}
        if file_name:
            params["file_name"] = file_name

        allowed_extensions = {"pdf", "doc", "docs", "xls", "xlsx", "rt", "cif", "dat", "csv", "png", "jpg", "tif"}
        if not any(file_path.lower().endswith(ext) for ext in allowed_extensions):
            raise ValueError(f"File extension not allowed. Allowed extensions are: {', '.join(allowed_extensions)}")

        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as file:
                files = {"file": (file_name or file_path, file)}
                response = await client.post(endpoint, params=params, headers=headers, files=files)
                response.raise_for_status()
                return response.json()

    @staticmethod
    async def query_projects(
            response_model: Optional[str] = None,
            id: Optional[str] = None,
            fields_output: Optional[str] = 'all',
            affiliation: Optional[str] = None,
            project_name: Optional[str] = None,
            provenance_email: Optional[str] = None,
            material_formula: Optional[str] = None,
            material_all_elements: Optional[str] = None,
            material_any_element: Optional[str] = None,
            iemap_id: Optional[str] = None,
            isExperiment: Optional[bool] = None,
            simulationCode: Optional[str] = None,
            experimentInstrument: Optional[str] = None,
            simulationMethod: Optional[str] = None,
            experimentMethod: Optional[str] = None,
            parameterName: Optional[str] = None,
            parameterValue: Optional[str] = None,
            propertyName: Optional[str] = None,
            propertyValue: Optional[str] = None,
            fields: Optional[str] = None,
            limit: int = 100,
            skip: int = 0,
            sort: Optional[str] = None,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None
    ) -> List[ProjectQueryModel]:
        """
        Query projects with specified parameters.
        This method is a static method and does not require an instance of the class to be called.
        No authentication is required to call this method.

        Args:
            response_model (Optional[str]): Response model.
            id (Optional[str]): Project ID.
            fields_output (Optional[str]): Fields to output. Defaults to 'all'.
            affiliation (Optional[str]): Affiliation.
            project_name (Optional[str]): Project name.
            provenance_email (Optional[str]): Provenance email.
            material_formula (Optional[str]): Material formula.
            material_all_elements (Optional[str]): All elements in material.
            material_any_element (Optional[str]): Any element in material.
            iemap_id (Optional[str]): IEMAP ID.
            isExperiment (Optional[bool]): Is experiment.
            simulationCode (Optional[str]): Simulation code.
            experimentInstrument (Optional[str]): Experiment instrument.
            simulationMethod (Optional[str]): Simulation method.
            experimentMethod (Optional[str]): Experiment method.
            parameterName (Optional[str]): Parameter name.
            parameterValue (Optional[str]): Parameter value.
            propertyName (Optional[str]): Property name.
            propertyValue (Optional[str]): Property value.
            fields (Optional[str]): Fields.
            limit (int): Limit. Defaults to 100.
            skip (int): Skip. Defaults to 0.
            sort (Optional[str]): Sort.
            start_date (Optional[str]): Start date.
            end_date (Optional[str]): End date.

        Returns:
            ProjectQueryResponse: Query response.
        """
        endpoint = settings.PROJECT_QUERY
        params = {
            key: value for key, value in {
                "response_model": response_model,
                "id": id,
                "fields_output": fields_output,
                "affiliation": affiliation,
                "project_name": project_name,
                "provenance_email": provenance_email,
                "material_formula": material_formula,
                "material_all_elements": material_all_elements,
                "material_any_element": material_any_element,
                "iemap_id": iemap_id,
                "isExperiment": isExperiment,
                "simulationCode": simulationCode,
                "experimentInstrument": experimentInstrument,
                "simulationMethod": simulationMethod,
                "experimentMethod": experimentMethod,
                "parameterName": parameterName,
                "parameterValue": parameterValue,
                "propertyName": propertyName,
                "propertyValue": propertyValue,
                "fields": fields,
                "limit": limit,
                "skip": skip,
                "sort": sort,
                "start_date": start_date,
                "end_date": end_date,
            }.items() if value is not None
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()

        try:
            adapter = TypeAdapter(ProjectQueryModel)
            results: List[ProjectQueryModel] = [adapter.validate_python(single_result) for single_result in
                                                response.json()]
            return results
        except ValidationError as e:
            print("Validation error occurred:")
            print(e.json(indent=4))

    @staticmethod
    def build_project_payload(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build and validate a JSON payload for the "/api/v1/project/add" endpoint.

        This method constructs a JSON payload for creating a new project, applies
        Pydantic validation, and provides easy-to-read error messages in case of validation failures.

        Args:
            data (Dict[str, Any]): A dictionary containing the project details.

        Returns:
            Dict[str, Any]: A validated dictionary representation of the project payload.
                            Returns an empty dictionary if validation fails.

        Raises:
            ValidationError: If the provided data is not valid according to the Pydantic model.

        Example:
            >>> data = {
            ...     "project": {
            ...         "name": "Materials for Batteries",
            ...         "label": "MB",
            ...         "description": "IEMAP - eco-sustainable synthesis of ionic liquids as innovative solvents for lithium/sodium batteries"
            ...     },
            ...     "material": {
            ...         "formula": "C11H20N2F6S2O4"
            ...     },
            ...     "process": {
            ...         "method": "Karl-Fischer titration",
            ...         "agent": {
            ...             "name": "Karl-Fischer titrator Mettler Toledo",
            ...             "version": None
            ...         },
            ...         "isExperiment": True
            ...     },
            ...     "parameters": [
            ...         {
            ...             "name": "time",
            ...             "value": 20,
            ...             "unit": "s"
            ...         },
            ...         {
            ...             "name": "weight",
            ...             "value": 0.5,
            ...             "unit": "gr"
            ...         }
            ...     ],
            ...     "properties": [
            ...         {
            ...             "name": "Moisture content",
            ...             "value": "<2",
            ...             "unit": "ppm"
            ...         }
            ...     ]
            ... }
            >>> valid_payload = ProjectHandler.build_project_payload(data)
            >>> if valid_payload:
            ...     print("Payload is valid and ready to be submitted.")
            ... else:
            ...     print("Payload is invalid.")
        """
        try:
            project_request = IEMAPProject(**data)
            return project_request.dict()
        except ValidationError as e:
            print("Validation Error: The provided data is not valid.")
            for error in e.errors():
                print(f"Error in field '{'.'.join(map(str, error['loc']))}': {error['msg']} (type: {error['type']})")
            return {}
