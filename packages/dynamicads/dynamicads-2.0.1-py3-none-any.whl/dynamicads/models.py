from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class AdDimensions:
    """Dimensions for an ad."""
    width: int
    height: int

@dataclass
class Usage:
    """API usage information."""
    current_usage: int
    limit: int

@dataclass
class Ad:
    """
    An ad object returned by the API.
    
    Attributes:
        id: Unique identifier for the ad
        status: Current status ('processing', 'complete', or 'error')
        media_url: URL to the generated media file (when complete)
        voice_url: URL to the generated voice file (when complete)
        component_code: React component code (when complete)
        voice_script: Generated voice script (when complete)
        prompt: Original prompt used to generate the ad
        dimensions: Width and height of the ad
        media_type: Type of media ('video' or 'image')
        error: Error message if status is 'error'
        created_at: Timestamp when the ad was created
    """
    id: str
    status: str
    media_url: Optional[str] = None
    voice_url: Optional[str] = None
    component_code: Optional[str] = None
    voice_script: Optional[str] = None
    prompt: str = ''
    dimensions: Dict[str, int] = None
    media_type: str = 'video'
    error: Optional[str] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        """Convert dimensions dict to AdDimensions object."""
        if isinstance(self.dimensions, dict):
            self.dimensions = AdDimensions(**self.dimensions)

    @property
    def is_complete(self) -> bool:
        """Check if the ad generation is complete."""
        return self.status == 'complete'

    @property
    def is_error(self) -> bool:
        """Check if the ad generation failed."""
        return self.status == 'error'

    @property
    def is_processing(self) -> bool:
        """Check if the ad is still processing."""
        return self.status == 'processing'
