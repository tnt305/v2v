import easyocr
from typing import List
from src.utils import is_timestamp

class ServeBall:
    def __init__(self,
                 use_gpu: bool = True,
                 lang: str =  'en'):
        self.lang = lang
        self.use_gpu  = use_gpu
        self.reader =  easyocr.Reader([lang], gpu =  use_gpu)

    def scoreboard_reader(self, image_path):
        return self.reader.readtext(image_path)
    
    @staticmethod
    def get_item(data: List):
        # bbox result
        bbox = [item[0] for item in data]
        y_values = [point[0][1] for point in bbox]
        # get text 
        text = [item[1] for item in data]
        # get confidence score
        conf_score = [item[2] for item in data]

        return y_values, text, conf_score

    def get_item_by_lines(self, image_path: str, y_threshold: int = 5):
        """
        Chia dữ liệu thành các dòng (lines) dựa trên các giá trị y của bounding boxes.
        Dữ liệu có giá trị y gần nhau sẽ được coi là cùng một dòng.
        """
        # Lấy thông tin y_values, confidence score và text
        data = self.scoreboard_reader(image_path)
        y_values, conf_scores, texts = self.get_item(data)

        # Sắp xếp các item theo giá trị y (từ thấp đến cao)
        sorted_data = list(zip(y_values, conf_scores, texts, data))
        
        # Khởi tạo danh sách các dòng (lines)
        lines = []
        current_line = []
        current_y = sorted_data[0][0]
        
        # Duyệt qua từng item trong dữ liệu đã sắp xếp và nhóm chúng theo dòng
        for y, _, _, item in sorted_data:
            # Nếu y_value của item này gần với y_value hiện tại, chúng cùng một dòng
            if abs(y - current_y) <= y_threshold:
                current_line.append(item)
            else:
                # Nếu không, tạo một dòng mới
                lines.append(current_line)
                current_line = [item]
                current_y = y
        
        # Đừng quên thêm dòng cuối vào danh sách
        if current_line:
            lines.append(current_line)
        
        return lines

    @staticmethod
    def timestamp2frames(timestamp: str, fps: str = 2):
        _, seconds = map(int, timestamp.split(':'))
        back_frames = fps * seconds
        return back_frames
    
    def at_timestamp(self, image_path: str, y_threshold: int = 5):
        lines = self.get_item_by_lines(image_path, y_threshold)
        for line in lines:
            text1, text2 =  line[0][1], line[-1][1]
            if is_timestamp(text1):
                current_time = is_timestamp(text1)
                break
            elif is_timestamp(text2):
                current_time = is_timestamp(text2)
                break
        
        back_nframes = self.timestamp2frames(current_time)

        return back_nframes

