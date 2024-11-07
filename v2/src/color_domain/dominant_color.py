import cv2
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from src.color_domain.base import BaseColor
from utils.dataset_level import read_csv


class DominantColorDetector(BaseColor):
    STRATEGIES = ['centric', 'hicherachy']
    def __init__(self, 
                 strategy: str = 'centric',
                 col_names = ["color", "color_name", "hex", "R", "G", "B"]):
        self.strategy = strategy
        if self.strategy not in self.STRATEGIES:
            raise ValueError(f"Strategy must be one of the following: {self.STRATEGIES}")
        self.col_names = col_names
        super().__init__()
    
    @staticmethod
    def hicherachy_color(img, w: str, h: str, level: str = 2):
        center_x, center_y = w // level, h // level
        b, g, r = img[center_y, center_x]
        b, g, r = int(b), int(g), int(r)
        return r, b, g
    
    def get_color_name(self, R, G, B, file_path):
        csv = read_csv(file_path, self.col_names)
        minimum = 10000
        cname = None
        for i in range(len(csv)):
            d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
            if d < minimum:
                minimum = d
                cname = csv.loc[i, "color_name"]
        return cname
        
    def get_color_main(self, img_path):
        img = cv2.imread(f"./{img_path}")
        if img is not None:
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, _  = img.shape
            
            if self.strategy == 'centric':
                r, g, b = self.hicherachy_color(img, w, h, 2)
                color_name =  self.get_color_name(r, g, b, img_path)
            else:
                raise ValueError("PLease choose one of the above strategy: centric, median")
        else: 
            raise ValueError("File not found")
            
        return color_name
    

# import cv2
# import pandas as pd
# from pathlib import Path
# from typing import List, Tuple, Optional
# from pydantic import BaseModel, Field, validator

# class ColorBase(BaseModel):
#     """Base class for color detection operations."""
#     color_names: List[str] = Field(default=["color", "color_name", "hex", "R", "G", "B"])
    
#     def get_color_name(self, r: int, g: int, b: int, color_data: pd.DataFrame) -> str:
#         """Find the closest matching color name for given RGB values."""
#         raise NotImplementedError

#     def analyze_image(self, image_path: str) -> Optional[str]:
#         """Analyze the dominant color in an image."""
#         raise NotImplementedError

# class DominantColorDetector(ColorBase):
#     """Implementation for detecting and naming dominant colors in images."""
    
#     class Config:
#         arbitrary_types_allowed = True

#     VALID_STRATEGIES = ['centric', 'hierarchical']
    
#     strategy: str = Field(
#         default='centric',
#         description="Strategy to use for color detection"
#     )
    
#     @validator('strategy')
#     def validate_strategy(cls, v):
#         if v not in cls.VALID_STRATEGIES:
#             raise ValueError(f"Strategy must be one of: {cls.VALID_STRATEGIES}")
#         return v

#     def _extract_center_color(
#         self, 
#         image: np.ndarray, 
#         divisions: int = 2
#     ) -> Tuple[int, int, int]:
#         """Extract color from the center region of the image."""
#         height, width = image.shape[:2]
#         center_x = width // divisions
#         center_y = height // divisions
        
#         b, g, r = image[center_y, center_x]
#         return int(r), int(g), int(b)

#     def _load_color_data(self, filepath: str) -> pd.DataFrame:
#         """Load and validate color reference data."""
#         try:
#             color_data = pd.read_csv(filepath, names=self.color_names)
#             required_columns = {'R', 'G', 'B', 'color_name'}
#             if not all(col in color_data.columns for col in required_columns):
#                 raise ValueError(f"CSV must contain columns: {required_columns}")
#             return color_data
#         except FileNotFoundError:
#             raise FileNotFoundError(f"Color reference file not found: {filepath}")
#         except Exception as e:
#             raise ValueError(f"Error loading color data: {str(e)}")

#     def get_color_name(
#         self, 
#         r: int, 
#         g: int, 
#         b: int, 
#         color_data: pd.DataFrame
#     ) -> str:
#         """Find the closest matching color name for given RGB values."""
#         min_distance = float('inf')
#         closest_color = None
        
#         for _, row in color_data.iterrows():
#             distance = sum(
#                 abs(c1 - c2) for c1, c2 in 
#                 zip([r, g, b], [row['R'], row['G'], row['B']])
#             )
            
#             if distance < min_distance:
#                 min_distance = distance
#                 closest_color = row['color_name']
                
#         return closest_color

#     def analyze_image(self, image_path: str) -> Optional[str]:
#         """
#         Analyze an image to determine its dominant color name.
        
#         Args:
#             image_path: Path to the image file
            
#         Returns:
#             str: Name of the dominant color
            
#         Raises:
#             ValueError: If image cannot be loaded or strategy is invalid
#             FileNotFoundError: If image file doesn't exist
#         """
#         image_path = Path(image_path)
#         if not image_path.exists():
#             raise FileNotFoundError(f"Image file not found: {image_path}")
            
#         # Load and verify image
#         img = cv2.imread(str(image_path))
#         if img is None:
#             raise ValueError(f"Failed to load image: {image_path}")
            
#         # Get color values based on strategy
#         if self.strategy == 'centric':
#             r, g, b = self._extract_center_color(img)
#         elif self.strategy == 'hierarchical':
#             # Implement hierarchical strategy here if needed
#             raise NotImplementedError("Hierarchical strategy not yet implemented")
#         else:
#             raise ValueError(f"Unknown strategy: {self.strategy}")
            
#         # Load color reference data and get color name
#         color_data = self._load_color_data(str(image_path))
#         return self.get_color_name(r, g, b, color_data)

# # Usage example:
# if __name__ == "__main__":
#     try:
#         detector = DominantColorDetector(strategy='centric')
#         color_name = detector.analyze_image("path/to/image.jpg")
#         print(f"Dominant color: {color_name}")
#     except Exception as e:
#         print(f"Error: {str(e)}")