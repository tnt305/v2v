import pandas as pd

from typing import List, Tuple, Optional
from pydantic import BaseModel, Field, validator

class ColorBase(BaseModel):
    """Base class for color detection operations."""
    color_names: List[str] = Field(default=["color", "color_name", "hex", "R", "G", "B"])
    
    def get_color_name(self, r: int, g: int, b: int, color_data: pd.DataFrame) -> str:
        """Find the closest matching color name for given RGB values."""
        raise NotImplementedError

    def analyze_image(self, image_path: str) -> Optional[str]:
        """Analyze the dominant color in an image."""
        raise NotImplementedError