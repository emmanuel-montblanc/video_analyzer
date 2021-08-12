"""
This module allows you to download a video from instagram with the url of a post
"""


import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def _download_video(video_url, video_path):
    """
    download the video at the url <video_url> and save it at the location <video_path>
    :param video_url: The video we want to download
    :param video_path: The location where we save the video
    :return: None
    """

    r = requests.get(video_url, stream=True)
    with open(video_path, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)
                f.flush()


def _get_response(url):
    """
    do a html request on the url <url> until it suceeds, and return the response,
    :param url: the url we want to make a request on
    :return: response: the response to the request
    """

    response = requests.get(url, headers={'User-agent': 'idk_just_let_me_dl_this'})
    while response.status_code != 200:
        response = requests.get(url)
    return response


def _get_video_url(response):
    """
    Parse the reponse to the html request, search and return the url of the video
    :param response:
    :return: video_url: the url of the video
    """
    soup = BeautifulSoup(response.text, "html.parser")
    script_with_url = soup.find('script', text=re.compile('window\._sharedData'))
    list_attributes = script_with_url.string.split(',')

    for elem in list_attributes:
        if "video_url" in elem:
            video_url = elem.split('":"')[1].rstrip('"')

            # Replace the hexadecimal char
            video_url = video_url.replace("\\u0026", "&")
            return video_url


def _create_insta_videos_folder():
    """
    create the folder "insta_videos" if it doesnt exists
    :return: None
    """

    insta_videos_folder = Path.cwd() / "insta_videos"
    insta_videos_folder.mkdir(parents=True, exist_ok=True)


def download_from_instagram(post_url):
    """
    do a request on <post_url>, get the response and parse it to find the video url,
    then download the video and save it in the folder "insta_videos"
    :param post_url: the post of the video we want to download
    :return: video_path: the path of the video downloaded
    """

    response = _get_response(post_url)
    video_url = _get_video_url(response)

    post_name = post_url.split('/p/')[-1].rstrip('/')
    file_name = "insta_video_" + post_name + ".mp4"
    video_path = Path.cwd() / "insta_videos" / file_name

    _create_insta_videos_folder()
    _download_video(video_url, video_path)

    return video_path
