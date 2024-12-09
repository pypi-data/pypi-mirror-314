from typing import Optional, Dict, Any
import httpx
from iemap_mi.models import StatsResponse
from iemap_mi.utils import get_headers
from iemap_mi.settings import settings


class IemapStat:
    def __init__(self, token: Optional[str] = None) -> None:
        """
        Initialize IemapStat with base URL and JWT token.

        Args:

            token (Optional[str]): JWT token for authentication. Defaults to None.
        """

        self.token = token

    async def get_stats(self) -> StatsResponse:
        """
        Get statistics from the API.

        Returns:
            StatsResponse: Response containing statistics data.
        """
        endpoint = settings.STATS
        headers = get_headers(self.token)

        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, headers=headers)
            response.raise_for_status()
            return StatsResponse(**response.json())
