# %%
from SoccerNet.Downloader import SoccerNetDownloader
mySoccerNetDownloader = SoccerNetDownloader(LocalDirectory="./data/soccer_dataset")
mySoccerNetDownloader.password = "s0cc3rn3t"

# %%
import os
os.cpu_count()

# %%
import concurrent.futures
from SoccerNet.Downloader import SoccerNetDownloader
mySoccerNetDownloader = SoccerNetDownloader(LocalDirectory="./data/soccer_dataset")
mySoccerNetDownloader.password = "s0cc3rn3t"

def download_frames():
    mySoccerNetDownloader.downloadGames(files=["Frames-v3.zip"], split=["train","valid","test"], task= "frames")

def download_spotting_2023():
    mySoccerNetDownloader.downloadDataTask(task="spotting-2023", split=["train", "valid", "test"])

def download_labels_v2():
    mySoccerNetDownloader.downloadGames(files=["Labels-v2.json"], split=["train","valid","test"])

def download_labels_cameras():
    mySoccerNetDownloader.downloadGames(files=["Labels-cameras.json"], split=["train","valid","test"])
def download_mp4_video():
    mySoccerNetDownloader.downloadGames(files=["1_720p.mkv", "2_720p.mkv", "video.ini"], split=["train","valid","test"])

# Chạy đồng thời các tác vụ tải xuống
with concurrent.futures.ThreadPoolExecutor(max_workers= 30) as executor:
    executor.submit(download_frames)
    executor.submit(download_spotting_2023)
    executor.submit(download_labels_v2)
    executor.submit(download_labels_cameras)

# %%
mySoccerNetDownloader.password = "s0cc3rn3t"
mySoccerNetDownloader.downloadGames(files=["1_720p.mkv", "2_720p.mkv", "video.ini"], split=["train","valid","test"])


