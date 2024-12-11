import os
from bgeditor.common.utils import get_dir, download_file
from moviepy.editor import *
import uuid
from cloudflare import CloudFlareHelper
from gbackup import DriverHelper
import requests
import traceback
from  bgeditor.dao.FootageHelper import split_videos, zip_video_file
def get_video_aspect_ratio(w, h, tolerance=0.1):
    # Danh sách các tỉ lệ tiềm năng
    aspect_ratios = [(16, 9), (9, 16), (1, 1)]

    min_error = float('inf')  # Khởi tạo sai số tối thiểu với giá trị vô cực
    best_aspect_ratio = None

    for ratio in aspect_ratios:
        target_ratio = ratio[0] / ratio[1]
        actual_ratio = w / h
        error = abs(actual_ratio - target_ratio)

        if error <= tolerance and error < min_error:
            min_error = error
            best_aspect_ratio = ratio

    if best_aspect_ratio:
        return f"{best_aspect_ratio[0]}:{best_aspect_ratio[1]}"
    else:
        closest_ratio = min(aspect_ratios, key=lambda x: abs(x[0] / x[1] - actual_ratio))
        return f"{closest_ratio[0]}:{closest_ratio[1]}"

def get_thumbs(video_path, duration):

    # if duration>5*50:
    #     thumb_path = os.path.join(get_dir("results"), f"{str(uuid.uuid4())}-thumb.jpg")
    #     cmd_get_thumb = f"ffmpeg -i \"{video_path}\"  -filter:v scale=\"iw/2:ih/2\" -frames:v 1 \"{thumb_path}\""
    #     os.system(cmd_get_thumb)
    #     return thumb_path, None
    number_get_thumb = (duration/10)
    if number_get_thumb <1:
        number_get_thumb=1
    video_rs= os.path.join(get_dir("results"), f"{str(uuid.uuid4())}_animaton_thumbs.webm")
    tmp_thumbs = os.path.join(get_dir("coolbg_ffmpeg"), f"{str(uuid.uuid4())}-thumbs%03d.jpg")
    thumb_path =  os.path.join(get_dir("results"), f"{str(uuid.uuid4())}-thumb.jpg")
    cmd_get_thumb = f"ffmpeg  -ss {duration/2} -i \"{video_path}\" -filter:v scale=\"iw/2:ih/2\" -frames:v 1 \"{thumb_path}\""
    os.system(cmd_get_thumb)
    cmd_get_thumbs = f"ffmpeg -i \"{video_path}\"  -vf fps=1/{number_get_thumb} \"{tmp_thumbs}\""
    os.system(cmd_get_thumbs)
    cmd_create_animation_thumbs=f"ffmpeg -y -framerate 3 -i \"{tmp_thumbs}\" -filter:v scale=\"iw/2:ih/2\" \"{video_rs}\""
    os.system(cmd_create_animation_thumbs)
    os.system(f"rm -rf {tmp_thumbs.replace('%03d','*')}")
    return thumb_path, video_rs

def normalized_and_upload(video_path):
    download_link = None
    try:
        arr_split_vds = split_videos(video_path)
        zip_path = zip_video_file(arr_split_vds)
        cf = CloudFlareHelper("moonseo-source")
        dh = DriverHelper()
        download_link = dh.upload_file_auto("moonseo", [zip_path])[0]
        if "None" == download_link:
            download_link = cf.upload(video_path, 'download')
    except:
        traceback.print_exc()
        pass
    return download_link
def process_video_sd(video_path):
    data= None
    try:
        file_size = os.path.getsize(video_path)/1024 #kb
        rs = VideoFileClip(video_path)
        duration = rs.duration
        width, height = rs.size
        bitrate_kbps = file_size * 8 / duration
        ratio = get_video_aspect_ratio(width, height)
        thumb_path, thumb_video=get_thumbs(video_path, duration)
        cf = CloudFlareHelper("moonseo-source")
        dh = DriverHelper()
        download_link = dh.upload_file_auto("moonseo", [video_path])[0]
        if "None" == download_link:
            download_link = cf.upload(video_path, 'download')
        thumb_link=""
        animation_thumb_link=""
        if thumb_path:
            thumb_link = cf.upload(thumb_path, 'thumb')
        if thumb_video:
            animation_thumb_link = cf.upload(thumb_video, 'ani_thumb')
        data = {
            "duration": duration,
            "width": width,
            "height": height,
            "ratio": ratio,
            "download_link": download_link,
            "thumb_link": thumb_link,
            "animation_thumb_link": animation_thumb_link,
            "bitrate": bitrate_kbps
        }
        os.unlink(video_path)
        os.unlink(thumb_path)
        os.unlink(thumb_video)
    except:
        traceback.print_exc()
        pass
    return data


# rs=process_video_sd(r"C:\Users\Hoa Bui\AppData\Local\Temp\Hoa_Bui\download\ddcc333f-65aa-45c6-8e44-378d334605bf.mp4")
# rs=download_tiktok_video("https://www.tiktok.com/@deanscheider.offfical/video/7281227303630376238")
# print(rs)
