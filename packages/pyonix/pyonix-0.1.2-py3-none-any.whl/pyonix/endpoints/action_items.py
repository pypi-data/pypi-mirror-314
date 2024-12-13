# ionix_api/endpoints/action_items.py
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from pyonix.client import IonixClient

@dataclass
class ActionItem:
    id: str
    title: str
    type: str
    asset: str
    summary: str
    urgency: str
    cves: List[str]
    first_opened_at: datetime
    last_opened_at: datetime
    description: Optional[str] = None

@dataclass
class PaginatedResponse:
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Dict[str, Any]]

class ActionItems:
    """
    Handles interaction with the Ionix Action Items API endpoints.
    """
    def __init__(self, client: IonixClient):
        self.client = client

    def get(self, 
            asset: Optional[str] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            **kwargs) -> PaginatedResponse:
        """
        Get open action items synchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            PaginatedResponse containing action items
            
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
        response = self.client.get("metadata/remediation/action_items/open/", params=params)
        return PaginatedResponse(**response)

    async def get_async(self,
                       asset: Optional[str] = None,
                       limit: Optional[int] = None,
                       offset: Optional[int] = None,
                       **kwargs) -> PaginatedResponse:
        """
        Get open action items asynchronously.
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            PaginatedResponse containing action items
            
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
        response = await self.client.get_async("metadata/remediation/action_items/open/", params=params)
        return PaginatedResponse(**response)

    def get_all(self, 
                asset: Optional[str] = None,
                limit: Optional[int] = None,
                offset: Optional[int] = None,
                **kwargs) -> List[Dict[str, Any]]:
        """
        Get all open action items synchronously (handles pagination automatically).
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            List of all action items across pages
            
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
        return self.client.paginate("metadata/remediation/action_items/open/", params=params)

    async def get_all_async(self,
                          asset: Optional[str] = None,
                          limit: Optional[int] = None,
                          offset: Optional[int] = None,
                          **kwargs) -> List[Dict[str, Any]]:
        """
        Get all open action items asynchronously (handles pagination automatically).
        
        Args:
            asset: Filter by asset name
            limit: Number of results per page
            offset: Pagination offset
            **kwargs: Additional filter parameters
            
        Returns:
            List of all action items across pages
            
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
        return await self.client.paginate_async("metadata/remediation/action_items/open/", params=params)

    def acknowledge(self, 
                   ids: List[str],
                   is_acknowledged: bool,
                   reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Acknowledge or unacknowledge action items synchronously.
        
        Args:
            ids: List of action item IDs
            is_acknowledged: True to acknowledge, False to unacknowledge
            reason: Optional acknowledgement reason
            
        Returns:
            API response
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        data = {
            "ids": ids,
            "is_acknowledged": is_acknowledged
        }
        if reason:
            data["acknowledgement_reason"] = reason
            
        return self.client.post("remediation/action-items/acknowledge/", data=data)

    async def acknowledge_async(self,
                             ids: List[str],
                             is_acknowledged: bool,
                             reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Acknowledge or unacknowledge action items asynchronously.
        
        Args:
            ids: List of action item IDs
            is_acknowledged: True to acknowledge, False to unacknowledge
            reason: Optional acknowledgement reason
            
        Returns:
            API response
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        data = {
            "ids": ids,
            "is_acknowledged": is_acknowledged
        }
        if reason:
            data["acknowledgement_reason"] = reason
            
        return await self.client.post_async("remediation/action-items/acknowledge/", data=data)
