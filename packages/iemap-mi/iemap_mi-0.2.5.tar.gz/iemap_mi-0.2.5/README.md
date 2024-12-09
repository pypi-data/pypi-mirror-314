![Project Logo](https://github.com/SergioEanX/iemap_mi_module/blob/master/images/logo_iemap.png?raw=True)
# Iemap-MI Python Module

[![PyPI version](https://badge.fury.io/py/iemap-mi.svg)](https://badge.fury.io/py/iemap-mi)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Iemap-MI is a Python module that provides easy access to the IEMAP REST API.   
It includes functionality for user authentication, fetching paginated project data, and more.    
The module is designed to be used asynchronously and leverages `httpx` for making HTTP requests   
and `pydantic` for data validation.

## Documentation

For full documentation, visit [iemap-mi documentation](https://iemap-mi-module.readthedocs.io/en/latest/index.html).   
For a full working example, see `examples.py` (create metadata for a new project, add project to IEMAP platform, add
files to project, query data) inside iemap_mi folder.
Full documentation for REST API endpoint is available at   
[IEMAP-MI REST API Swagger generated documentation](https://iemap.enea.it/rest/docs).

## Features

- **JWT Authentication**: Authenticate users and manage sessions with JSON Web Tokens.
- **Project Data**: Fetch paginated project data from the API. Add new projects metadata, add file, and more.
- **Asynchronous Requests**: Utilize `httpx` for efficient, asynchronous HTTP requests.
- **Data Validation**: Ensure data integrity with `pydantic` models.
- **AI functionalities based on a Graph neural networks (GNNs)**: aiding in the discovery and design of new battery
  materials
- **Semantic search**: Not yet implemented. Stay tuned!

## AI Model

The geoCGNN model is inspired by the research paper published in Nature Communications:   
"Crystal Graph Convolutional Neural Networks for Analyzing Materials Properties"   
(https://www.nature.com/articles/s43246-021-00194-3).

**This model has been further trained and optimized by ENEA on the High-Performance Computing (HPC)   
infrastructure CRESCO (https://ict.enea.it/cresco/) to predict formation energy and redox potential,   
aiding in the discovery and design of new battery materials.**

In addition to the foundational concepts,    
the approach to redox potential prediction incorporates methodologies discussed in the paper       
**"Data-Driven Discovery of Redox Active Battery Materials Using Crystal Graph Neural Networks"**         
(Batteries, 2024, 10(12), 431; https://www.mdpi.com/2313-0105/10/12/431),    
which provided insights into the application of CGNNs for redox-active materials.

The training for formation energy prediction was conducted on a dataset of over 150,000 materials,       
while the training for redox potential prediction utilized data from more than 4,000 batteries.        
These datasets were sourced from the Materials Project database (Materials Project),    
with materials containing noble gas elements excluded from the training process.

**Note**: The predicted redox potential represents the voltage change from the completely discharged    
to the fully charged state of the battery material. Consequently, only the CIF file corresponding to    
the completely discharged battery material was used during the training and validation phases.       
This same format must be provided as input during the inference phase.

## Installation

To install the module, use `poetry`:

```sh
poetry add iemap-mi
```

Alternatively, you can install it using pip:

```sh

pip install iemap-mi

```

## Note on IEMAP Projects metadata

Projects on IEMAP platform are stored as:

- **General project metadata** with a predefined schema
- **Files related to project** (allowed extensions are: csv, pdf, doc, docx, cls, xlsx, dat, in, cif)

Project metadata are stored onto MongoDB (and are searchable) while files are stored onto Ceph FS.   
The metadata schema is the following:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "project": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "label": {
          "type": "string"
        },
        "description": {
          "type": "string"
        }
      },
      "required": [
        "name",
        "label"
      ]
    },
    "material": {
      "type": "object",
      "properties": {
        "formula": {
          "type": "string"
        }
      },
      "required": [
        "formula"
      ]
    },
    "process": {
      "type": "object",
      "properties": {
        "method": {
          "type": "string"
        },
        "agent": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "version": {
              "type": [
                "string",
                "null"
              ]
            }
          },
          "required": [
            "name"
          ]
        },
        "isExperiment": {
          "type": "boolean"
        }
      },
      "required": [
        "method",
        "agent",
        "isExperiment"
      ]
    },
    "parameters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "value": {
            "type": "number"
          },
          "unit": {
            "type": "string"
          }
        },
        "required": [
          "name",
          "value",
          "unit"
        ]
      }
    },
    "properties": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "value": {
            "type": "string"
          },
          "unit": {
            "type": "string"
          }
        },
        "required": [
          "name",
          "value",
          "unit"
        ]
      }
    }
  },
  "required": [
    "project",
    "material",
    "process",
    "parameters",
    "properties"
  ]
}

```

Pydantic class `IEMAPProject` is provided to easily build and validate project metadata.   
For more information and usage example view `examples.py`.   
Alternatively, you can use `ProjectHandler.build_project_payload()` method to build a project payload from a Python
dictionary.   
**[IEMAP website](https://iemap.enea.it)** provides a user-friendly interface to interact with IEMAP platform,      
including the ability to add new projects, search for existing projects, and more.   
**In IEMAP website, projects metadata are defined compiling an Excel file (a template ready to use is provided) with the
required fields**,       
this data are converted into a JSON object that is used to store the project metadata on the platform,   
similarly to the schema above.    
In a second step, files related to the project can be uploaded, always using the UI provided by IEMAP website.

## Usage

This module allows you to interact integrate into your workflow the IEMAP platform.
Data to store on IEMAP platform are stored as projects metadata and files,    
this means that you can store metadata and files related to your projects.
Steps required to use the module are:

1. Initialize the client
2. Authenticate (to get the JWT token used for subsequent requests). To register an account
   visit [IEMAP](https://iemap.enea.it).
3. Store metadata for your project
4. Store files related to your project
5. Retrieve/Query project data

**Note**: The module is designed to be used asynchronously,    
so you should use `async` functions and `await` for making requests.
A quick introduction to asynchronous programming in Python can be found [here](https://realpython.com/async-io-python/).

**Note**:    
IEMAP platform is a service provided by **ENEA**,    
the Italian National Agency for New Technologies,   
Energy and Sustainable Economic Development within the Project IEMAP (see [details](https://iemap.enea.it/)).

Here are some brief examples of how to use the iemap-mi module.

### Initialize the Client and Authenticate


### Fetch Paginated Project Data

```python
# import necessary modules
import asyncio
from iemap_mi.iemap_mi import IemapMI


# define an async main function
async def main():


# Initialize IEMAP client
client = IemapMI()

# Authenticate to get the JWT token
await client.authenticate(username='your_username', password='your_password')

# Fetch paginated project data
projects = await client.project_handler.get_projects(page_size=10, page_number=1)
print(projects)

# Run the main function asynchronously
if __name__ == "__main__":
    asyncio.run(main())
```

### Running Tests

To run the tests, use pytest. Make sure to set the TEST_USERNAME and TEST_PASSWORD environment variables with your test
credentials.

```sh

export TEST_USERNAME="your_username"
export TEST_PASSWORD="your_password"
pytest
```

Using pytest with poetry

```sh

poetry run pytest
```

Contributing

Contributions are welcome! Please follow these steps to contribute:

    Fork the repository.
    Create a new branch for your feature or bugfix.
    Make your changes.
    Ensure tests pass.
    Submit a pull request.

License

This project is licensed under the MIT License.   
See the LICENSE file for more information.   
Acknowledgements

    httpx
    pydantic

Contact

For any questions or inquiries, please contact **iemap.support@enea.it**.

```plaintext
This`README.md` includes an overview of the project, installation instructions,
usage examples, testing guidelines, contribution guidelines, license information,
acknowledgements, and contact information.
```