
from datetime import timedelta

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
        return text
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