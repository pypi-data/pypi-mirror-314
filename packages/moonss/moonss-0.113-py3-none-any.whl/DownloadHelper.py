import json
import os
from bgeditor.common.utils import get_dir, download_file
from gbackup import DriverHelper
import uuid
import requests

def get_proxy_iproyal():
    proxy_tmp = f"http://victor69:dota2hoabt2@geo.iproyal.com:12321"
    proxies = {"http": proxy_tmp, "https": proxy_tmp}
    return proxies

def get_download_nwm_tiktok(url, retries=3):
    try:
        video_id=url.split('/')[-1]
        urld = f"https://api22-normal-c-useast2a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}&iid=7329834909681551122&device_id=7325735055111128585&channel=googleplay&app_name=musical_ly&version_code=330205&device_platform=android&device_type=SM-N950F&version=9"
        proxies=get_proxy_iproyal()
        headers={'user-agent':'com.zhiliaoapp.musically/2023302050 (Linux; U; Android 9; en; SM-N950F; Build/PPR1.180610.011; Cronet/TTNetVersion:996128d2 2024-01-12 QuicVersion:ce58f68a 2024-01-12)'}
        res=requests.get(urld,headers=headers,proxies=proxies).json()
        data=res['aweme_list'][0]
        nwm_video_url_HQ= data['video']['bit_rate'][0]['play_addr']['url_list'][0]
        return nwm_video_url_HQ
    except:
        if retries > 1:
            return get_download_nwm_tiktok(url,retries-1)
        pass
    return None
def get_download_nwm_tiktok_old(url, retries=3):
    try:
        video_id=url.split('/')[-1]
        urld = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"
        proxies=get_proxy_iproyal()
        headers={'user-agent':'com.ss.android.ugc.trill/494+Mozilla/5.0+(Linux;+Android+12;+2112123G+Build/SKQ1.211006.001;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/107.0.5304.105+Mobile+Safari/537.36'}
        res=requests.get(urld, headers=headers, proxies=proxies).json()
        # print(res)
        data=res['aweme_list'][0]
        nwm_video_url_HQ= data['video']['bit_rate'][0]['play_addr']['url_list'][0]
        return nwm_video_url_HQ
    except:
        if retries > 1:
            return get_download_nwm_tiktok_old(url,retries-1)
        pass
    return None

def download_ytdlp(videoId):
    def convert_to_netscape(cookie_header, domain):
        cookies = cookie_header.split(";")
        netscape_cookies = []
        for cookie in cookies:
            try:
                name, value = cookie.split("=")
                netscape_cookies.append(f"{domain}\tTRUE\t/\tTRUE\t3855747771\t{name}\t{value}")
            except:
                pass
        return "\n".join(netscape_cookies)

    def get_cookies():
        headers = {"Bas-Name": "AutoWin"}
        domain = ".youtube.com"
        res = requests.get("http://bas.reupnet.info/profile/get-random-cookie-ytb", headers=headers).text
        netscape_cookie_file = convert_to_netscape(res, domain)
        with open("cookies.txt", "w") as file:
            file.write("# Netscape HTTP Cookie File\n")
            file.write(netscape_cookie_file)
    get_cookies()
    videoId = videoId.strip()
    result = os.path.join(get_dir("download"), f"{videoId}.webm")
    cmd = f"yt-dlp --cookies cookies.txt -f bv+ba/b -o {result} \"{videoId}\""
    print(cmd)
    rs= os.system(cmd)
    if not os.path.exists(result):
        result=f"{result}.mp4" #maybe merge can be mp4
    print(rs)
    return result

def download_tiktok_video(video_url):
    download_url = get_download_nwm_tiktok(video_url)
    return download_file(download_url,None,"mp4")

def download_tiktok_video_crawl_data(crawl_data_txt):
    crawl_data = json.loads(crawl_data_txt)
    rs=None
    if "video_url" in crawl_data:
        url=crawl_data['video_url']
        headers={}
        if "cookies" in crawl_data:
            headers['Cookie'] = crawl_data['cookies']
        file_name = str(uuid.uuid4()) + "." + "mp4"
        rs = os.path.join(get_dir('download'), file_name)
        r = requests.get(url, headers=headers, verify=False)
        with open(rs, 'wb') as f:
            f.write(r.content)
    return rs
def download_douyin_video(video_id):
    return download_file(f"https://aweme.snssdk.com/aweme/v1/play/?video_id={video_id}&ratio=1080p&line=0",None, "mp4")
def donwload_instagram_video(crawl_data_txt):
    crawl_data = json.loads(crawl_data_txt)
    if "video_url" in crawl_data:
        return download_file(crawl_data['video_url'],None, "mp4")
    else:
        return None
def download_ffmpeg(url):
    file_path=os.path.join(get_dir('ffmpeg'),uuid.uuid4().hex+".mp4")
    cmd=f"ffmpeg -i \"{url}\" -c copy \"{file_path}\""
    os.system(cmd)
    return file_path
def donwload_artlistio_video(crawl_data_txt):
    crawl_data = json.loads(crawl_data_txt)
    if "video_m3u8" in crawl_data:
        url=crawl_data['video_m3u8'].replace("_playlist","_1080p")
        return download_ffmpeg(url)
    else:
        return None
def donwload_canva_video(crawl_data_txt):
    crawl_data = json.loads(crawl_data_txt)
    if "video_url" in crawl_data:
        return download_file(crawl_data['video_url'],None, "mp4")
    else:
        return None
def download_drive_video(platform_id):
    url=f"gdrive;;resource2@soundhex.com;;{platform_id}"
    return download_file(url, None, "mp4")
# print(donwload_artlistio_video('{"video_url":"https:\/\/cms-artifacts.artlist.io\/content\/artgrid\/footage-hd\/1269510_hdgraded_1157601_Habitas_V1-0011.mp4?d=true&filename=218447_Woman%20Forest%20Jungle%20Smoke_By_Robert_Pilichowski_Artlist_HD.mp4&Expires=1714642023288&Key-Pair-Id=K2ZDLYDZI2R1DF&Signature=cKKt-jNIu8Ad9~J5QUbyZxJb8ycV-8eVxRHsb~F7kYLm38eFLJRj3vdWDvmwfXI0tM0KegrLuVGDk6ECDiHEbrxn52CIm5Y7fX2fdRnu3uGKttaTO0JA1K0oDOW4ctjyWQ8tud~Bi7K5L09LujhNW-60ryLz2T7F7ncZpKqLl7N2qwev2mQGmhZN2CB21VuhNdZPndRFivkBYAwNOHMn6Cpfwg3LLBPWdzCqxrXhDk6RisAyAPrfxuQCiFd2yyymJKM6ijrJBkXKleEDIe0bLUIl3A5Qucu99vJUszAT~JCbCfkspedrRLZ75~-tp3Ey5hz6eioq~xG6qbL0wMJXHA__","video_m3u8":"https:\/\/cms-public-artifacts.artlist.io\/content\/artgrid\/footage-hls\/218447_playlist.m3u8","thumbnail_url":"https:\/\/artgrid.imgix.net\/footage-graded-thumbnail\/7d29ad821b_1157601_0-second_w800px.jpeg"}'))