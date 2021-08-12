"""
This modules allows you to extract the frames from a video, and store them in a folder as jpeg images
"""

import os
from pathlib import Path
import cv2


def get_frames(video_path: Path):
    """
    Checks if the video wasnt loaded yet, if it wasn't, extract every frame from the video,
    and save them in the folder videos/<name of the video>
    :param video_path: the video we want to extract the frames from
    :return: None
    """

    _create_video_folder()

    vid_name = video_path.stem
    working_folder = Path().cwd() / "videos" / vid_name
    already_loaded = _check_if_loaded(working_folder)

    if not already_loaded:
        _clear_dir(working_folder)
        vid = cv2.VideoCapture(str(video_path))

        # loop over the frames of the video
        frame_count = 0
        while True:
            ret, frame = vid.read()

            if ret:
                if (frame_count % 10) == 0:
                    print("creating frame nb " + str(frame_count))

                name = './videos/' + vid_name + '/frame' + str(frame_count) + '.jpg'
                cv2.imwrite(name, frame)

                frame_count += 1
            else:
                break

        # At the last iteration, the frame count is still increase, but there no more images created
        frame_count -= 1

        fps = round(vid.get(cv2.CAP_PROP_FPS))
        _create_info_file(frame_count, fps, vid_name)
        vid.release()


def _create_video_folder():
    """
    creates the folder "videos" if it doesnt exists
    :return: None
    """

    video_folder = Path.cwd() / "videos"
    video_folder.mkdir(parents=True, exist_ok=True)


def _clear_dir(directory):
    """
    Empties the directory "directory"
    :param directory: the directory we want to empty
    :return: None
    """

    for file in os.listdir(directory):
        os.remove(directory / file)


def _create_info_file(frame_count, fps, vid_name):
    """
    Create the info file, a .txt file with the nb of frames and the fps of the video
    :param frame_count:  the number of frames of the video
    :param fps: the fps of the video
    :param vid_name: the name of the viode
    :return: None
    """

    info_file = './videos/' + vid_name + '/info.txt'
    with open(info_file, 'x') as file:
        file.writelines([str(frame_count), '\n' + str(fps)])


def _check_if_loaded(working_folder):
    """
    try to create the folder working_folder and checks if the video was already fully loaded
    :param working_folder: The folder where the frames will be
    :return already_loaded: boolean, True if the video was already loaded before
    """

    already_loaded = False

    # Tries to create the folder
    try:
        os.mkdir(working_folder)

    except FileExistsError:
        # if it exists checks if the info file exists
        info_file = working_folder / "info.txt"
        if info_file.exists():
            with open(info_file) as file:
                nb_frame = int(file.readline().rstrip())

            # Then checks if all the frames already exists
            already_loaded = True
            for i in range(nb_frame+1):
                frame = working_folder / ("frame" + str(i) + ".jpg")

                # if one frame is missing, the video is not fully loaded
                if not frame.exists():
                    already_loaded = False
                    print("missing frame " + str(i))

    if already_loaded:
        print("video already loaded")

    return already_loaded
