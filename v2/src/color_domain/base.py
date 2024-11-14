import pandas as pd

from typing import List, Tuple, Optional, ClassVar
from pydantic import BaseModel, Field, validator

class BaseColor(BaseModel):
    """Base class for color processing operations."""
    STRATEGIES: ClassVar[List[str]] = ['centric', 'kmeans', 'hierarchy'] 
    
    class Config:
        arbitrary_types_allowed = True  # Allow non-pydantic compatible types
        # validate_assignment = True
    def get_color_name(self, r: int, g: int, b: int, color_data: pd.DataFrame) -> str:
        """Find the closest matching color name for given RGB values."""
        raise NotImplementedError
    
    def get_color_main(self, image):
        raise NotImplementedError