from typing import Dict, Any
from enum import Enum
import httpx
from iemap_mi.settings import settings


class PredictionType(Enum):
    """
    Enumeration for prediction types supported by the geoCGNN model.
    """
    FORMATION_ENERGY = "formation-energy"
    REDOX_POTENTIAL = "redox-potential"


class AIHandler:
    """
    Handles AI-related operations, such as interacting with the geoCGNN REST API.

    The geoCGNN model is inspired by the research paper published in Nature Communications:
    "Crystal Graph Convolutional Neural Networks for Analyzing Materials Properties"
    (https://www.nature.com/articles/s43246-021-00194-3).

    This model has been further trained and optimized by ENEA on the High-Performance Computing (HPC)
    infrastructure CRESCO (https://ict.enea.it/cresco/) to predict formation energy and redox potential,
    aiding in the discovery and design of new battery materials.

    Attributes:
        None
    """

    @staticmethod
    async def get_prediction(cif_file_path: str, prediction_type: PredictionType) -> Dict[str, Any]:
        """
        The geoCGNN model predicts material properties, such as formation energy and redox potential,
        based on crystal structures provided in .cif format. It has been inspired by the research
        paper published in Nature Communications (https://www.nature.com/articles/s43246-021-00194-3)
        and further optimized by ENEA using the CRESCO HPC infrastructure.

        Args:
            cif_file_path (str): Path to the .cif file to upload.
            prediction_type (PredictionType): Type of prediction to request.

        Returns:
            Dict[str, Any]: JSON response from the geoCGNN model.

        Raises:
            Exception: If the API request fails or the response status is not 200.
        """
        # Base endpoint from settings
        base_endpoint = settings.AI_GEOCGNN

        # Construct the full URL
        url = f"{base_endpoint}ai_materials:predict_what"

        # Use a file handle to read the .cif file
        try:
            with open(cif_file_path, "rb") as cif_file:
                files = {"file": (cif_file_path, cif_file, "application/octet-stream")}
                data = {"predict_what": prediction_type.value}

                # Print a waiting message
                print("Waiting for inference result from geoCGNN model...")

                # Send the request
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, files=files, data=data)

                # Raise HTTP errors if any
                response.raise_for_status()

                # Return the parsed JSON response
                print("Inference result received.")
                return response.json()

        except FileNotFoundError:
            raise ValueError(f"The file at {cif_file_path} was not found.")
        except httpx.RequestError as e:
            raise RuntimeError(f"An error occurred while making the request: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Error response {e.response.status_code}: {e.response.text}")
