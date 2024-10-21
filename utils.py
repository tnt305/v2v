import json
import subprocess
def get_video_fps(file_path):
    cmd = [
        'ffprobe', 
        '-v', 'quiet', 
        '-print_format', 'json', 
        '-show_streams', 
        file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)

    if 'streams' in data and len(data['streams']) > 0:
        fps_info = data['streams'][0].get('r_frame_rate', '0/1')
        numerator, denominator = map(int, fps_info.split('/'))
        fps = numerator / denominator
        return fps
    else:
        raise ValueError("Không thể lấy thông tin FPS từ dữ liệu trả về của ffprobe.")

def get_video_duration(input_file):
    cmd = [
        'ffprobe', 
        '-v', 'quiet', 
        '-print_format', 'json', 
        '-show_format', 
        '-show_streams', 
        input_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
        if 'format' in data and 'duration' in data['format']:
            return float(data['format']['duration'])
        else:
            raise ValueError("Không tìm thấy thông tin độ dài video.")
    except json.JSONDecodeError:
        raise ValueError("Lỗi phân tích cú pháp JSON từ ffprobe.")