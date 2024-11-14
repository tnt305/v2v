from pathlib import Path
from typing import List, Tuple, Optional
from src.match_timeline.utils import scoreboard_cropper
from abc import abstractmethod
from src.match_timeline.event_detection import ServeBall
from src.color_domain.dominant_color import DominantColorDetector

class PeriodDetection:
    PERIODS = {"Kick-off", "Secondhalf", "Advertising"}
    def __init__(self,
                 image_dir: str|Path,
                 ):
        self.serve_ball = ServeBall()
        self.color_check = DominantColorDetector()
        pass
    
    @abstractmethod
    def base_detector(self, image: str| Path):
        image_path = scoreboard_cropper(self.image_dir, image)
        timing = self.serve_ball.at_timestamp(image_path)
        if timing is not None and int(timing):
            period = "Kick-off"
            return period
    
    def detector(self):
        period = None
        for image in self.image_dir:
            period = self.base_detector(image)