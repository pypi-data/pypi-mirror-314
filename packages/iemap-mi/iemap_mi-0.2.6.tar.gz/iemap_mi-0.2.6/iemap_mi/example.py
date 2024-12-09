# This is an example script that demonstrates how to use the iemap-mi Python module.
# If not yet install then you can install the module by running the following command:
# pip install iemap-mi

# Import the required modules
# asyncio is used to run the main function asynchronously
import asyncio
# stdiomask is used to hide the password input
import stdiomask
# TypeAdapter is used to validate the project data
from pydantic import TypeAdapter
# Import the IemapMI class from the iemap_mi module
from iemap_mi import IemapMI
# typing is used to define the type hints
from typing import List
# Import the required models from the iemap_mi module
from iemap_mi.models import (IEMAPProject, Project, Material, Process, Agent,
                             Parameter, Property, FlattenedProjectBase, FlattenedProjectHashEmail, FileInfo)

# Import the ProjectHandler class from the iemap_mi module to handle project data tasks as:
# - Create a new project
# - Add a file to a project
from iemap_mi.project_handler import ProjectHandler

# Import the flatten_project_data function from the iemap_mi.utils module to easily flatten project data for display
from iemap_mi.utils import flatten_project_data

# Import the PredictionType enumeration to use it in the get_prediction function
from iemap_mi.ai_handler import PredictionType

# to pretty print the output of JSON responses
from pprint import pprint

# Check if pandas and tqdm are available,
# and set the corresponding flags
# pandas is used to display the project data in a DataFrame (if pandas is available)
# tqdm is used to display a progress bar while fetching projects (if tqdm is available)
try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from tqdm import tqdm

    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


# Define the iterate_projects function
# this function shows how to fetch projects in pages and display them in a pandas DataFrame
# similar functions can be created to fetch other data, this is just an example
# executed later in the main function
async def iterate_projects(client: IemapMI, page_size: int = 40) -> None:
    """
        Iterates over projects in the Iemap Management Interface (IEMI) and prints them,
        or converts to a pandas DataFrame if pandas is available.

        This function fetches projects in pages, with each page containing up to `page_size` projects.
        It can optionally include email addresses in the output if `show_email` is True and the user has
        the necessary permissions.

        Parameters:
        - client (IemapMI): An authenticated instance of IemapMI used to fetch project data.
        - page_size (int): The number of projects to fetch per page. Defaults to 40.

        Returns:
        None. The function directly prints project information to the console or displays it in a pandas DataFrame.

        Usage Example:
        ```python
        import asyncio
        from iemap_mi import IemapMI

        async def main():
            client = IemapMI()
            await client.authenticate(username="your_username", password="your_password")
            await iterate_projects(client, page_size=50)

        if __name__ == "__main__":
            asyncio.run(main())
        ```
        """
    page_number = 1
    all_projects: List[FlattenedProjectBase] = []
    total_projects = None  # Initialize total_projects to None

    while True:
        projects_response = await client.project_handler.get_projects(page_size=page_size, page_number=page_number)
        if not projects_response.data:
            break

        adapter = TypeAdapter(FlattenedProjectHashEmail)

        projects = [adapter.validate_python(project) for project in projects_response.data]

        all_projects.extend(projects)
        page_number += 1

        if total_projects is None:
            total_projects = projects_response.number_docs

        if TQDM_AVAILABLE:
            tqdm.write(f"Page {page_number - 1} fetched. Total projects so far: {len(all_projects)}/{total_projects}")

    if PANDAS_AVAILABLE:
        # Set the option to display all columns
        pd.set_option('display.max_columns', None)
        # Convert the projects to a pandas DataFrame
        # df = pd.DataFrame([project.model_dump() for project in all_projects])
        flat_projects = [flatten_project_data(project) for project in all_projects]
        df = pd.DataFrame(flat_projects)
        print(df)
    else:
        # Print the projects as a list of dictionaries
        for project in all_projects:
            print(project.model_dump())


# Define the main function
# This function demonstrates how to use the IemapMI module to interact with the IEMAP API
# It includes examples of:
# - Authenticating a user
# - Creating a new project
# - Adding a file to a project
# - Fetching statistical data from the API
async def main():
    # Initialize the client
    client = IemapMI()

    # Print the module version
    IemapMI.print_version()

    # Get the prediction using AI functionalities from IEMAP Platform using a geoCGNN model
    # The geoCGNN model is inspired by the research paper published in Nature Communications:
    # "Crystal Graph Convolutional Neural Networks for Analyzing Materials Properties"
    # (https://www.nature.com/articles/s43246-021-00194-3).
    # This model has been further trained and optimized by ENEA on the High-Performance Computing (HPC)
    # infrastructure CRESCO (https://ict.enea.it/cresco/) to predict formation energy and redox potential,
    # The prediction type can be either "formation-energy" or "redox-potential"
    # The prediction is based on the crystal structure provided in .cif format
    # The prediction is returned as a JSON response
    # example CIFs can be found in the "example_cif" folder

    cif_file_for_energy_prediction = "./example_cif/mp-2064.cif"
    cif_file_for_redox_potential = "./example_cif/mp-1003402.cif"

    prediction_fe = await client.ai_handler.get_prediction(cif_file_path=cif_file_for_energy_prediction,
                                                           prediction_type=PredictionType.FORMATION_ENERGY)

    print(f"Formation energy for file {cif_file_for_energy_prediction} predicted by AI model")
    pprint(prediction_fe, indent=2)

    prediction_rp = await client.ai_handler.get_prediction(cif_file_path=cif_file_for_redox_potential,
                                                           prediction_type=PredictionType.REDOX_POTENTIAL)

    print(f"Redox potential for file {cif_file_for_redox_potential} predicted by AI model")
    pprint(prediction_rp, indent=2)


    # Iterate over projects and print them or convert to pandas DataFrame if available
    await iterate_projects(client, page_size=60)

    # Fetch statistics data
    stats = await client.stat_handler.get_stats()
    print(stats.model_dump())

    query_response = await client.project_handler.query_projects(
        # project_name="Materials for Batteries",
        material_formula="C11H20N2F6S2O4",
        # isExperiment=True,
        limit=10
    )

    print([doc.model_dump() for doc in query_response])

    # Prompt for username and password
    username = input("Enter your username (email address): ")
    password = stdiomask.getpass(prompt="Enter your password: ")

    # Authenticate to get the JWT token to be used to invoke REST API endpoints
    # !! ATTENTION: you should register to the IEMAP platform to get your credentials !!
    # This credential that has to be validated by email sent to the user email address
    # To do so, please visit: https://iemap.enea.it/auth/signup

    # This sets a JWT token in the client instance
    await client.authenticate(username=username, password=password)

    # To create a new project, you need to provide the project metadata as a dictionary (JSON-like format)
    # The project metadata should include the project name, label, description, material, process, parameters,
    # and properties.
    # Parameters and properties are arrays of dictionaries containing the
    # name, value, and unit of each parameter/property.
    # Below an example of a valid project metadata dictionary is provided
    #
    data = {
        "project": {
            "name": "Materials for Batteries",
            "label": "MB",
            "description": "IEMAP - eco-sustainable synthesis of ionic liquids as innovative solvents for lithium/sodium batteries"
        },
        "material": {
            "formula": "C11H20N2F6S2O4"
        },
        "process": {
            "method": "Karl-Fischer titration",
            "agent": {
                "name": "Karl-Fischer titrator Mettler Toledo",
                "version": None
            },
            "isExperiment": True
        },
        "parameters": [
            {
                "name": "time",
                "value": 20,
                "unit": "s"
            },
            {
                "name": "weight",
                "value": 0.5,
                "unit": "gr"
            }
        ],
        "properties": [
            {
                "name": "Moisture content",
                "value": "<2",
                "unit": "ppm"
            }
        ]
    }

    # Build and validate the project payload
    valid_payload_example_1 = ProjectHandler.build_project_payload(data)

    if valid_payload_example_1:
        print("Payload is valid and ready to be submitted.")
    else:
        print("Payload is invalid.")

    # Example of invalid payload
    data_invalid = {"project": {
        "name": "Materials for Batteries",
        "label": "MB",
        # "description": Description is missing, this is  a required field !!!
    },
        # material is missing and this is a required field !!!!
        # "material": {
        #     "formula": "C11H20N2F6S2O4"
        # },
        "process": {
            "method": "Karl-Fischer titration",
            "agent": {
                "name": "Karl-Fischer titrator Mettler Toledo",
                "version": None
            },
            "isExperiment": True
        }}
    # Also missing are parameters and properties, which are required fields

    # Build and validate the project payload
    # as the payload is invalid, the function will return None and will
    # print the error message that caused the payload to be invalid.
    # In this case, the error message is:
    #
    # Validation Error: The provided data is not valid.
    # Error in field 'project.description': Field required (type: missing)
    # Error in field 'material': Field required (type: missing)
    # Error in field 'parameters': Field required (type: missing)
    # Error in field 'properties': Field required (type: missing)

    valid_payload_example_2 = ProjectHandler.build_project_payload(data_invalid)

    if valid_payload_example_2:
        print("Payload from 'data_invalid' is valid and ready to be submitted.")
    else:
        print("Payload from 'data_invalid' is invalid.")

    for p in [valid_payload_example_1, valid_payload_example_2]:
        if p:
            # Create a new project
            current_proj = IEMAPProject(**p)
            print(f"Adding project: {current_proj.project.name}")
            new_project = await client.project_handler.create_project(current_proj)
            print(new_project)

    # Alternatively metadate can be defined using the Pydantic class CreateProjectRequest as below

    project_data = IEMAPProject(
        project=Project(
            name="Materials for Batteries",
            label="MB",
            description="IEMAP - eco-sustainable synthesis of ionic liquids as innovative solvents for lithium/sodium batteries"
        ),
        material=Material(
            formula="C11H20N2F6S2O4"
        ),
        process=Process(
            method="Karl-Fischer titration",
            agent=Agent(
                name="Karl-Fischer titrator Mettler Toledo",
                version=None
            ),
            isExperiment=True
        ),
        parameters=[
            Parameter(
                name="time",
                value=20,
                unit="s"
            ),
            Parameter(
                name="weight",
                value=0.5,
                unit="gr"
            )
        ],
        properties=[
            Property(
                name="Moisture content",
                value="<2",
                unit="ppm"
            )
        ]
    )

    # as previously add a new project
    new_project = await client.project_handler.create_project(project_data)
    print(new_project)

    # Now add a file to the newly created project
    # to do this:
    # 1. input file name path
    # 2. get the file name from full path
    # 3. use method "add_file_to_project" from "project_handler" providing the id of the newly created project (metadata only)
    # and the file to read
    file_to_add_to_project = input(
        f"Please type in the full path of file to upload and associate to current project {project_data.project.name}: ")
    file_name = file_to_add_to_project.split("/")[-1]
    print("Adding file to project...")

    # Add a file to the project.
    # To add a file to a project,
    # you need to provide the project ID (inserted_id) and the file path.
    # If you already have the project ID, you can use it directly (as string).
    file_response = await client.project_handler.add_file_to_project(
        project_id=new_project.inserted_id,
        file_path=file_to_add_to_project,
        file_name=file_name
    )
    # Check if the file was uploaded successfully
    # If the file was uploaded successfully, the 'uploaded' key in the response will be True
    if file_response['uploaded']:
        file_info = FileInfo(**file_response)
        # Print the file information
        # The file is save onto the IEMAP FileSystem with a unique hash
        print(f"File {file_info.file_name} uploaded successfully to project (saved as {file_info.file_hash})")
    else:
        print("File upload failed.")

    # Finally an example of how to fetch statistics data from IEMAP DB
    client.stat_handler.get_stats()

    # to view all functionalities consult documentation at
    # https://iemap-mi-module.readthedocs.io/en/latest/iemap_mi.html
    # Note that current module is in development and not a stable release.


# Run the main function asynchronously
if __name__ == "__main__":
    asyncio.run(main())
