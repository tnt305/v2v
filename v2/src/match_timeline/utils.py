
import os
from PIL import Image
from datetime import timedelta
from src.logger.logger import Logging

log = Logging()


def is_timestamp(text: str):
    """
        Function:
            Kiểm tra một giá trị bounding box có phải là timestamp không
            Một bbox được coi là timestamp khi được phân biệt bởi dấu , hoặc : hoặc có dấu .

        Output:
            Một output nếu không phải là timestamp thì sẽ trả về None
    """
    try:
        float(text)
        return text.replace(".", ":")
    except ValueError:
        if ':' in text:
            before , _ = text.split(":")
            try:
                float(before.strip())
                return text
            except:
                return text
        elif ',' in text:
            try:
                float(before.strip())
                return text.replace(",", ":")
            except:
                return text.replace(",", ":")
        elif '.' in text:
            try:
                float(before.strip())
                return text.replace(",", ":")
            except:
                return text.replace(",", ":")
        else:
            pass


def convert_to_timedelta(time_str: str) -> timedelta:
    # Tách phút và giây từ chuỗi "mm:ss"
    minutes, seconds = map(int, time_str.split(':'))
    
    # Tạo đối tượng timedelta từ phút và giây
    return timedelta(minutes=minutes, seconds=seconds)


def scoreboard_cropper(root_dir: str, image_name: str):
    image_path = os.path.exists(root_dir, image_name)
    crop_area = (0,0,400,100)
    
    image=  Image.open(image_path)
    cropped_image = image.crop(crop_area)
    cropped_image_dir = image_name.split(".")[0] + "_" + "cropped" + ".png"
    cropped_image_path = os.path.join(root_dir, cropped_image_dir)
    cropped_image.save(cropped_image_path)
    log.info(f'Ảnh scoreboard được lưu tại {cropped_image_dir}')
    return cropped_image_path