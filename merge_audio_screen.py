import threading
import time
import subprocess
from pathlib import Path


def merge(video_name):
    # Makes sure the threads have finished
    while threading.active_count() > 1:
        time.sleep(1)

    output_name = _get_output_name(video_name)

    cmd = "ffmpeg -i ./temp/screen.avi -i ./temp/audio.wav -shortest -c copy " + output_name
    subprocess.call(cmd, shell=True)


def _get_output_name(video_name):
    output_name = video_name + ".mkv"
    i = 0
    while Path(output_name).exists():
        i += 1
        output_name = video_name + "_" + str(i) + ".mkv"

    return output_name
