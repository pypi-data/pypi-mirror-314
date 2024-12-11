import os
import time
from DownloadHelper import download_drive_video, download_ytdlp, download_tiktok_video,download_tiktok_video_crawl_data, download_douyin_video, donwload_instagram_video, donwload_artlistio_video, donwload_canva_video
from SourceDataHelper import process_video_sd, normalized_and_upload
import requests


URL_HOME="https://moonseo.app"
URL_GET_JOB=f"{URL_HOME}/api/source/data/crawl"
URL_UPDATE_JOB=f"{URL_HOME}/api/source/data/update-by-id"
headers={"platform":"autowin"}


def execute():
    print("crawling: "+str(time.time()))
    obj = requests.get(URL_GET_JOB, headers=headers).json()
    if "id" in obj:
        print("Process: "+str(obj['id']))
        video_path = None
        normalized_url=None
        if obj['platform'] =='tiktok':
            # video_path = download_tiktok_video(obj['ori_link'])
            video_path = download_tiktok_video_crawl_data(obj['crawl_data'])
        if obj['platform'] =='youtube' or obj['platform'] =='youtube-long':
            video_path = download_ytdlp(obj['ori_link'])
        if obj['platform'] =='douyin':
            video_path = download_douyin_video(obj['platform_id'])
        if obj['platform'] == 'instagram':
            video_path = donwload_instagram_video(obj['crawl_data'])
        if obj['platform'] == 'artlistio':
            video_path = donwload_artlistio_video(obj['crawl_data'])
            normalized_url = normalized_and_upload(video_path)
        if obj['platform'] == 'canva':
            video_path = donwload_canva_video(obj['crawl_data'])
            normalized_url = normalized_and_upload(video_path)
        if obj['platform'] == 'drive':
            video_path = download_drive_video(obj['platform_id'])
            normalized_url = normalized_and_upload(video_path)
        if not obj['download_link']:
            sc_new = process_video_sd(video_path)
        else:
            sc_new = {}
        if not sc_new:
            sc_new={"id": obj['id']}
            if(obj['crawl_retries']<3):
                sc_new['crawl_retries']=obj['crawl_retries']+1
                sc_new['status'] = 1 #retries
            else:
                sc_new['status'] = 4
        else:
            sc_new['id']=obj['id']
            sc_new['status'] = 3
            sc_new['video_normalize'] = normalized_url
        rs=requests.post(URL_UPDATE_JOB, json=sc_new, headers=headers).json()
        print(rs)
        return True
    else:
        return False
def update():
    libs=["moonss", "coolbg", "gbak"]
    for lib in libs:
        os.system(f"pip install -U {lib}")

