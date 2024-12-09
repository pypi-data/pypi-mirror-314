import time
from typing import Dict, List, Optional, Union
import requests

from .models import Ad, Usage, AdDimensions
from .exceptions import DynamicAdsError, DynamicAdsTimeoutError

class DynamicAdsClient:
    """
    Client for the DynamicAds API.
    """
    def __init__(
        self,
        api_key: str,
        base_url: str = 'https://api.dynamicads.dev/api',
        debug: bool = False
    ):
        """
        Initialize the DynamicAds client.

        Args:
            api_key: Your API key
            base_url: API base URL (optional)
            debug: Enable debug logging (optional)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.debug = debug
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-api-key': api_key
        })

    def _log(self, *args) -> None:
        """Internal logging function."""
        if self.debug:
            print('[DynamicAds]', *args)

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            API response data

        Raises:
            DynamicAdsError: If the API request fails
        """
        url = f"{self.base_url}{endpoint}"
        self._log(f"{method} {url}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if response := getattr(e, 'response', None):
                try:
                    error_data = response.json()
                    message = error_data.get('error', str(e))
                except ValueError:
                    message = str(e)
            else:
                message = str(e)
            
            raise DynamicAdsError(message) from e

    def generate(
        self,
        prompt: str,
        media_type: str = 'video',
        dimensions: Optional[Dict[str, int]] = None
    ) -> Ad:
        """
        Generate a new ad.

        Args:
            prompt: Description of the ad to generate
            media_type: Type of media ('video' or 'image')
            dimensions: Custom dimensions (optional)

        Returns:
            Ad object with generation details

        Raises:
            DynamicAdsError: If generation fails
        """
        self._log('Generating ad:', prompt)
        
        data = {
            'prompt': prompt,
            'mediaType': media_type,
            'dimensions': dimensions or {
                'width': 672,
                'height': 384
            }
        }
        
        response = self._request('POST', '/ads/generate', json=data)
        return Ad(**response)

    def get_ad(self, ad_id: str) -> Ad:
        """
        Get details of a specific ad.

        Args:
            ad_id: ID of the ad to retrieve

        Returns:
            Ad object with full details

        Raises:
            DynamicAdsError: If retrieval fails
        """
        self._log('Getting ad:', ad_id)
        response = self._request('GET', f'/ads/{ad_id}')
        return Ad(**response)

    def list_ads(self) -> List[Ad]:
        """
        List all ads associated with your API key.

        Returns:
            List of Ad objects

        Raises:
            DynamicAdsError: If listing fails
        """
        self._log('Listing ads')
        response = self._request('POST', '/ads/list', json={'apiKey': self.api_key})
        return [Ad(**ad) for ad in response['ads']]

    def get_usage(self) -> Usage:
        """
        Get current usage information.

        Returns:
            Usage object with current usage stats

        Raises:
            DynamicAdsError: If usage check fails
        """
        self._log('Getting usage')
        response = self._request('GET', '/auth/usage')
        return Usage(**response)

    def wait_for_completion(
        self,
        ad_id: str,
        timeout: int = 300,
        interval: int = 2
    ) -> Ad:
        """
        Wait for an ad to complete generation.

        Args:
            ad_id: ID of the ad to wait for
            timeout: Maximum time to wait in seconds
            interval: Check interval in seconds

        Returns:
            Completed Ad object

        Raises:
            DynamicAdsTimeoutError: If timeout is reached
            DynamicAdsError: If checking status fails
        """
        self._log('Waiting for completion:', ad_id)
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise DynamicAdsTimeoutError(
                    f"Timeout waiting for ad {ad_id} to complete"
                )
            
            ad = self.get_ad(ad_id)
            
            if ad.status == 'complete':
                return ad
            elif ad.status == 'error':
                raise DynamicAdsError(ad.error or 'Ad generation failed')
            
            time.sleep(interval)
