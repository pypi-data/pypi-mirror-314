# ionix_api/endpoints/connections.py
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pyonix.client import IonixClient

@dataclass
class RiskRank:
    risk_score: int
    type: str

@dataclass
class Connection:
    id: int
    risk: RiskRank
    source: str
    target: str
    connected_asset_type: str
    type: str
    is_redirected: bool = False
    remarks: Optional[str] = None
    source_groups: Optional[List[str]] = None
    details: Optional[Dict[str, Any]] = None

class Connections:
    """
    Handles interaction with the Ionix Connections API endpoints.
    """
    def __init__(self, client: IonixClient):
        self.client = client

    def get_all(self,
                asset: Optional[str] = None,
                limit: Optional[int] = None,
                offset: Optional[int] = None,
                **kwargs) -> List[Dict[str, Any]]:
        """
        Get all connections synchronously (handles pagination automatically).
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            List of all connections across pages
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        params = {
            "asset": asset,
            "limit": limit,
            "offset": offset
        }
        params.update(kwargs)
        return self.client.paginate("discovery/connections/", params=params)

    async def get_all_async(self,
                          asset: Optional[str] = None,
                          limit: Optional[int] = None,
                          offset: Optional[int] = None,
                          **kwargs) -> List[Dict[str, Any]]:
        """
        Get all connections asynchronously (handles pagination automatically).
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            List of all connections across pages
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        params = {
            "asset": asset,
            "limit": limit,
            "offset": offset
        }
        params.update(kwargs)
        return await self.client.paginate_async("discovery/connections/", params=params)

    def get(self,
            asset: Optional[str] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            **kwargs) -> Dict[str, Any]:
        """
        Get paginated connections synchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            Paginated response containing connections
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        params = {
            "asset": asset,
            "limit": limit,
            "offset": offset
        }
        params.update(kwargs)
        return self.client.get("discovery/connections/", params=params)

    async def get_async(self,
                       asset: Optional[str] = None,
                       limit: Optional[int] = None,
                       offset: Optional[int] = None,
                       **kwargs) -> Dict[str, Any]:
        """
        Get paginated connections asynchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            Paginated response containing connections
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        params = {
            "asset": asset,
            "limit": limit,
            "offset": offset
        }
        params.update(kwargs)
        return await self.client.get_async("discovery/connections/", params=params)
