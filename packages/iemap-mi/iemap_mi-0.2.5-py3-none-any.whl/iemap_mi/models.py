# iemap_mi/models.py

from pydantic import BaseModel, constr, EmailStr, field_validator, RootModel
from typing import List, Optional, Any, Dict, Union
from datetime import datetime

from iemap_mi._utils_hash import hash_email


class AffiliationCount(BaseModel):
    """
    Represents the count of affiliations.

    Attributes:
        affiliation (str): The name of the affiliation.
        n (int): The number of projects/files for the affiliation.
    """
    affiliation: str
    n: int


class StatsData(BaseModel):
    """
    Represents the statistics data.

    Attributes:
        totalProj (int): Total number of projects.
        totalUsers (int): Total number of users.
        countProj (List[AffiliationCount]): List of project counts by affiliation.
        countFiles (List[AffiliationCount]): List of file counts by affiliation.
        totalUsersRegistered (int): Total number of registered users.
    """
    totalProj: int
    totalUsers: int
    countProj: List[AffiliationCount]
    countFiles: List[AffiliationCount]
    totalUsersRegistered: int


class StatsResponse(BaseModel):
    """
    Represents the response from the statistics endpoint.

    Attributes:
        data (StatsData): The statistics data.
    """
    data: StatsData


class AuthData(BaseModel):
    """
    Represents the authentication data.

    Attributes:
        username (str): The username for authentication.
        password (str): The password for authentication.
    """
    username: constr(min_length=1)
    password: constr(min_length=1)


class ProjectResponse(BaseModel):
    """
    Represents the response from the project list endpoint.

    Attributes:
        skip (int): Number of documents to skip.
        page_size (int): Number of results to return in a single page.
        page_number (int): Actual page number returned.
        page_tot (int): Total number of pages available.
        number_docs (int): Total number of documents in collection.
        data (List[Any]): List of all projects saved in the database.
    """
    skip: int
    page_size: int
    page_number: int
    page_tot: int
    number_docs: int
    data: List[Any]


class Agent(BaseModel):
    """
    Represents the agent used in the process.

    Attributes:
        name (str): The name of the agent.
        version (Optional[str]): The version of the agent.
    """
    name: str
    version: Optional[str]


class Process(BaseModel):
    """
    Represents the process used in the project.

    Attributes:
        method (str): The method used in the process.
        agent (Agent): The agent used in the process.
        isExperiment (bool): Indicates if the process is an experiment.
    """
    method: str
    agent: Agent
    isExperiment: bool


class Parameter(BaseModel):
    """
    Represents a parameter used in the project.

    Attributes:
        name (str): The name of the parameter.
        value (float): The value of the parameter.
        unit (str): The unit of the parameter.
    """
    name: str
    value: float
    unit: str


class Property(BaseModel):
    """
    Represents a property of the project.

    Attributes:
        name (str): The name of the property.
        value (str): The value of the property.
        unit (str): The unit of the property.
    """
    name: str
    value: str
    unit: str


class Project(BaseModel):
    """
    Represents a project.

    Attributes:
        name (str): The name of the project.
        label (str): The label of the project.
        description (str): The description of the project.
    """
    name: str
    label: str
    description: str


class Material(BaseModel):
    """
    Represents the material used in the project.

    Attributes:
        formula (str): The chemical formula of the material.
    """
    formula: str


class IEMAPProject(BaseModel):
    """
    Represents the request data to create a new project.

    Attributes:
        project (Project): The project details.
        material (Material): The material details.
        process (Process): The process details.
        parameters (List[Parameter]): List of parameters used in the project.
        properties (List[Property]): List of properties of the project.
    """
    project: Project
    material: Material
    process: Process
    parameters: List[Parameter]
    properties: List[Property]


class CreateProjectResponse(BaseModel):
    """
    Represents the response after creating a new project.

    Attributes:
        inserted_id (str): The ID of the newly inserted project document.
    """
    inserted_id: str


class Provenance(BaseModel):
    affiliation: str
    email: EmailStr
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


class ProvenanceHashEmail(BaseModel):
    affiliation: str
    email: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

    @field_validator('email', mode='before')
    def hash_email_field(cls, value):
        """Automatically hash the email field."""
        return hash_email(value)


class ProjectBase(BaseModel):
    name: str
    label: str
    description: Optional[str]


class Lattice(BaseModel):
    a: str
    b: str
    c: str
    alpha: str
    beta: str
    gamma: str


class Input(BaseModel):
    lattice: Lattice
    sites: List[List[float]]
    species: List[str]
    cell: List[List[float]]


class Output(BaseModel):
    lattice: Lattice
    sites: List[List[float]]
    species: List[str]
    cell: List[List[float]]


class MaterialModel(BaseModel):
    formula: str
    elements: List[str]
    input: Optional[Input] = None
    output: Optional[Output] = None


class FlattenedProjectBase(BaseModel):
    identifier: Optional[str]
    iemap_id: str
    provenance: Provenance
    project: ProjectBase
    process: Process
    material: MaterialModel
    parameters: List[Dict[str, Any]]
    properties: List[Dict[str, Any]]


class FlattenedProjectHashEmail(FlattenedProjectBase):
    provenance: ProvenanceHashEmail


# Model to use in free the queries
class FileModel(BaseModel):
    hash: str
    name: str
    extention: str
    size: Union[str, float]
    createdAt: datetime
    updatedAt: datetime


class FileInfo(BaseModel):
    file_hash: str
    file_name: str
    file_size: str
    uploaded: bool



class PropertyModel(BaseModel):
    name: str
    value: Any
    unit: Optional[str] = None


class ParameterModel(BaseModel):
    name: str
    value: Any
    unit: Optional[str] = None


class AgentModel(BaseModel):
    name: str
    version: Optional[str] = None


class ProcessModel(BaseModel):
    isExperiment: bool
    method: str
    agent: AgentModel


class ProjectModel(BaseModel):
    name: str
    label: str
    description: str


class ProvenanceQueryModel(BaseModel):
    email: str  # emails are returned as ****
    affiliation: str
    createdAt: datetime
    updatedAt: datetime


class ProjectQueryModel(BaseModel):
    iemap_id: str
    provenance: ProvenanceQueryModel
    project: ProjectModel
    process: ProcessModel
    material: MaterialModel
    parameters: List[ParameterModel]
    properties: List[PropertyModel]
    files: List[FileModel] = None
