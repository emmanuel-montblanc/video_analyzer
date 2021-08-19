"""
This module allows you to download a video from instagram with the url of a post
"""


import re
import time
from pathlib import Path

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup


class DownloadInstaVideoThread(QThread):
    """
    QThread class, made to be use with the select_vid windows,
    downloads the video of the post <post_url>
    :param str post_url: the post of the video we want to download
    """

    finished_request = pyqtSignal()
    found_url = pyqtSignal()
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, post_url):
        super().__init__()
        self.post_url = post_url

    def run(self):
        """
        do a request on <post_url>, get the response and parse it to find the video url,
        then download the video and save it in the folder "insta_videos"
        emits signals to indicate to the gui at which state is it.
        """

        _create_insta_videos_folder()

        try:
            response = _get_response(self.post_url)
            if response != "timeout":
                self.finished_request.emit()

                video_url = _get_video_url(response)
                self.found_url.emit()

                post_name = self.post_url.split('/p/')[-1].rstrip('/')
                file_name = "insta_video_" + post_name + ".mp4"
                video_path = Path.cwd().parent / "insta_videos" / file_name

                _download_video(video_url, video_path)
                self.finished.emit(file_name)

            else:
                self.error.emit("timeout")
        except (requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema,
                requests.exceptions.InvalidURL):
            self.error.emit("url")
        except requests.exceptions.ConnectionError:
            self.error.emit("connection")


def _download_video(video_url, video_path):
    """
    download the video at the url <video_url> and save it at the location <video_path>
    :param str video_url: The video we want to download
    :param Path video_path: The location where we save the video
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
    :param str url: the url we want to make a request on
    :return: Response: the response to the request
    """

    time_first_attempt = time.time()
    response = requests.get(url, headers={'User-agent': 'idk_just_let_me_dl_this'})
    while response.status_code != 200:
        response = requests.get(url)

        print(time.time() - time_first_attempt)
        if time.time() - time_first_attempt > 10:
            return "timeout"
    return response


def _get_video_url(response):
    """
    Parse the reponse to the html request, search and return the url of the video
    :param Response response: the response to the request made
    :return: str: The url of the video
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

    insta_videos_folder = Path.cwd().parent / "insta_videos"
    insta_videos_folder.mkdir(parents=True, exist_ok=True)


def download_from_instagram(post_url):
    """
    do a request on <post_url>, get the response and parse it to find the video url,
    then download the video and save it in the folder "insta_videos"
    :param str post_url: the post of the video we want to download
    :return: the path of the video downloaded
    """

    _create_insta_videos_folder()

    response = _get_response(post_url)
    video_url = _get_video_url(response)

    post_name = post_url.split('/p/')[-1].rstrip('/')
    file_name = "insta_video_" + post_name + ".mp4"
    video_path = Path.cwd().parent / "insta_videos" / file_name

    _download_video(video_url, video_path)

    return video_path
