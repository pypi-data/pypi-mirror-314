"""
DynamicAds Python SDK
~~~~~~~~~~~~~~~~~~~~

A Python SDK for the DynamicAds API.

Basic usage:

    >>> from dynamicads import DynamicAdsClient
    >>> client = DynamicAdsClient('your-api-key')
    >>> ad = client.generate(prompt='Create a dynamic product showcase')
    >>> print(ad.id)
"""

from .client import DynamicAdsClient
from .models import Ad, Usage, AdDimensions

__version__ = '2.0.0'
__all__ = ['DynamicAdsClient', 'Ad', 'Usage', 'AdDimensions']
