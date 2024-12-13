# ionix_api/client.py
import asyncio
import aiohttp
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from typing import Optional, Dict, Any, List, Tuple
from aiohttp import ClientTimeout
from aiohttp.client_exceptions import ClientError

from pyonix.endpoints.action_items import ActionItems
from pyonix.endpoints.assessments import Assessments
from pyonix.endpoints.connections import Connections
from pyonix.endpoints.dashboards import Dashboards
from pyonix.endpoints.tags import Tags

class IonixApiError(Exception):
    """Base exception for Ionix API errors"""
    pass

class IonixClientError(IonixApiError):
    """4xx client errors"""
    pass

class IonixServerError(IonixApiError):
    """5xx server errors"""
    pass

class IonixClient:
    def __init__(self,
                 base_url: str,
                 api_token: str,
                 account_name: str,
                 timeout: int = 30,
                 max_retries: int = 3,
                 batch_size: int = 5):
        """
        Initialize Ionix API client.
        
        Args:
            base_url: API base URL
            api_token: API authentication token
            account_name: Account name for X-Account-Name header
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            batch_size: Number of concurrent requests for pagination
        """
        self.base_url = base_url
        self.timeout = timeout
        self.batch_size = batch_size
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
            'X-Account-Name': account_name
        }
        
        # Setup sync session
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Add retry adapter for sync requests
        retry = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retry))
        
        # Async session will be created when needed
        self._async_session = None

        # Initialize endpoints
        self._action_items = None
        self._assessments = None
        self._connections = None
        self._dashboards = None
        self._tags = None

    @property
    def action_items(self) -> ActionItems:
        """Access the Action Items endpoint"""
        if self._action_items is None:
            self._action_items = ActionItems(self)
        return self._action_items

    @property
    def assessments(self) -> Assessments:
        """Access the Assessments endpoint"""
        if self._assessments is None:
            self._assessments = Assessments(self)
        return self._assessments

    @property
    def connections(self) -> Connections:
        """Access the Connections endpoint"""
        if self._connections is None:
            self._connections = Connections(self)
        return self._connections

    @property
    def dashboards(self) -> Dashboards:
        """Access the Dashboards endpoint"""
        if self._dashboards is None:
            self._dashboards = Dashboards(self)
        return self._dashboards

    @property
    def tags(self) -> Tags:
        """Access the Tags endpoint"""
        if self._tags is None:
            self._tags = Tags(self)
        return self._tags

    def _clean_params(self, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Clean None values from params dict"""
        if params is None:
            return None
        return {k: v for k, v in params.items() if v is not None}

    async def _get_async_session(self) -> aiohttp.ClientSession:
        """Get or create async session"""
        if self._async_session is None:
            timeout = ClientTimeout(total=self.timeout)
            self._async_session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=timeout
            )
        return self._async_session

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and errors.
        
        Args:
            response: Response from API request
            
        Returns:
            Response JSON data
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if 400 <= e.response.status_code < 500:
                raise IonixClientError(f"Client error: {e.response.text}")
            elif 500 <= e.response.status_code < 600:
                raise IonixServerError(f"Server error: {e.response.text}")
            raise
        return response.json()

    async def _handle_async_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """
        Handle async API response and errors.
        
        Args:
            response: Async response from API request
            
        Returns:
            Response JSON data
            
        Raises:
            IonixClientError: For 4xx errors
            IonixServerError: For 5xx errors
        """
        try:
            if 400 <= response.status < 500:
                text = await response.text()
                raise IonixClientError(f"Client error: {text}")
            elif 500 <= response.status < 600:
                text = await response.text()
                raise IonixServerError(f"Server error: {text}")
            response.raise_for_status()
            return await response.json()
        except ClientError as e:
            raise IonixApiError(f"Request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make synchronous GET request to API endpoint.
        
        Args:
            endpoint: API endpoint path or full URL
            params: Optional query parameters
            
        Returns:
            Response JSON data
        """
        if "https" in endpoint:
            url = endpoint
        else:
            url = f"{self.base_url}/{endpoint}"
        
        clean_params = self._clean_params(params)
        response = self.session.get(url, params=clean_params, timeout=self.timeout)
        return self._handle_response(response)

    async def get_async(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make asynchronous GET request to API endpoint.
        
        Args:
            endpoint: API endpoint path or full URL
            params: Optional query parameters
            
        Returns:
            Response JSON data
        """
        if "https" in endpoint:
            url = endpoint
        else:
            url = f"{self.base_url}/{endpoint}"
        
        clean_params = self._clean_params(params)
        session = await self._get_async_session()
        async with session.get(url, params=clean_params) as response:
            return await self._handle_async_response(response)

    async def _fetch_page(self, url: str, params: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Fetch a single page of results.
        
        Returns:
            Tuple of (results, next_url)
        """
        response = await self.get_async(url, params)
        return response.get('results', []), response.get('next')

    async def paginate_async(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Handle paginated results from API asynchronously with concurrent page fetching.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            List of all results across pages
        """
        all_results = []
        params = params or {}
        clean_params = self._clean_params(params)
        
        # Get first page to determine total pages
        first_page, next_url = await self._fetch_page(endpoint, clean_params)
        all_results.extend(first_page)
        
        # Collect all page URLs
        urls = []
        while next_url:
            urls.append(next_url)
            # Pre-fetch next URL to build complete URL list
            page_results, next_url = await self._fetch_page(next_url)
            all_results.extend(page_results)
        
        if urls:
            print(f"Fetching {len(urls)} additional pages in batches of {self.batch_size}...")
            
            # Process remaining URLs in batches
            for i in range(0, len(urls), self.batch_size):
                batch_urls = urls[i:i + self.batch_size]
                # Create tasks for each URL in the batch
                tasks = [self._fetch_page(url) for url in batch_urls]
                # Fetch batch concurrently
                batch_results = await asyncio.gather(*tasks)
                # Extract results from each page
                for results, _ in batch_results:
                    all_results.extend(results)
                
                print(f"Processed batch {i//self.batch_size + 1}/{(len(urls) + self.batch_size - 1)//self.batch_size}")
        
        return all_results

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make synchronous POST request to API endpoint.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Response JSON data
        """
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(response)

    async def post_async(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make asynchronous POST request to API endpoint.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Response JSON data
        """
        url = f"{self.base_url}/{endpoint}"
        session = await self._get_async_session()
        async with session.post(url, json=data) as response:
            return await self._handle_async_response(response)

    def paginate(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Handle paginated results from API synchronously.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            List of all results across pages
        """
        all_results = []
        params = params or {}
        clean_params = self._clean_params(params)
        
        while endpoint:
            response = self.get(endpoint, params=clean_params)
            all_results.extend(response.get('results', []))
            endpoint = response.get('next')  # Update endpoint to next page URL
            clean_params = {}  # Clear params after the first request
        return all_results

    async def close(self):
        """Close async session"""
        if self._async_session:
            await self._async_session.close()
            self._async_session = None
