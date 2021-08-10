import re

import requests
import os
from bs4 import BeautifulSoup


def download_video(video_url, local_filename):
    r = requests.get(video_url, stream=True)
    with open(os.getcwd()+"/"+local_filename, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)
                f.flush()


def get_response(url):
    response = requests.get(url, headers={'User-agent': 'idk_just_let_me_dl_this'})
    while response.status_code != 200:
        response = requests.get(url)
    return response


def get_video_url(response):
    soup = BeautifulSoup(response.text, "html.parser")
    script_with_url = soup.find('script', text=re.compile('window\._sharedData'))
    list_attributes = script_with_url.string.split(',')

    for elem in list_attributes:
        if "video_url" in elem:
            video_url = elem.split('":"')[1].rstrip('"')

            # Replace the hexadecimal char
            video_url = video_url.replace("\\u0026", "&")
            return video_url


def download_from_instagram(url):
    response = get_response(url)
    video_url = get_video_url(response)
    # print(video_url)
    post_name = url.split('/p/')[-1].rstrip('/')
    file_name = "insta_video_" + post_name + ".mp4"
    download_video(video_url,  "insta_videos/" + file_name)
    return file_name


if __name__ == '__main__':
    url = "https://www.instagram.com/p/CSXN0i9FVgi/"
    download_from_instagram(url)
