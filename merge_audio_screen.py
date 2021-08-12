import threading
import time
import subprocess
from pathlib import Path


def merge(video_name):
    # Makes sure the threads have finished
    while threading.active_count() > 1:
        time.sleep(1)

    _create_records_folder()
    output_path = _get_output_path(video_name)

    cmd = "ffmpeg -i ./temp/screen.avi -i ./temp/audio.wav -shortest -c copy " + str(output_path)
    subprocess.call(cmd, shell=True)


def _create_records_folder():
    records_folder = Path.cwd() / "insta_videos"
    records_folder.mkdir(parents=True, exist_ok=True)


def _get_output_path(video_name):
    record_folder = Path.cwd() / "records"
    output_name = video_name + ".mkv"
    i = 0
    while (record_folder / output_name).exists():
        i += 1
        output_name = video_name + "_" + str(i) + ".mkv"

    output_path = record_folder / output_name
    return output_path
