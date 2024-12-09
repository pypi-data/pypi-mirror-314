class DynamicAdsError(Exception):
    """Base exception for DynamicAds SDK."""
    pass

class DynamicAdsTimeoutError(DynamicAdsError):
    """Raised when an operation times out."""
    pass

class DynamicAdsAuthError(DynamicAdsError):
    """Raised when authentication fails."""
    pass

class DynamicAdsRateLimitError(DynamicAdsError):
    """Raised when rate limit is exceeded."""
    pass

class DynamicAdsValidationError(DynamicAdsError):
    """Raised when request validation fails."""
    pass
