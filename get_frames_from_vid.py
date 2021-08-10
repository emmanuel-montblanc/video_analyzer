import os
from pathlib import Path
import cv2


def get_frames(video_path: Path):

    vid_name = video_path.stem
    working_folder = Path().cwd() / "videos" / vid_name
    already_loaded = check_if_loaded(working_folder)

    if not already_loaded:
        clear_dir(working_folder)
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
        create_info_file(frame_count, fps, vid_name)
        vid.release()


def clear_dir(directory):
    for file in os.listdir(directory):
        os.remove(directory / file)


def create_info_file(frame_count, fps, vid_name):
    info_file = './' + vid_name + '/info.txt'
    with open(info_file, 'x') as file:
        file.writelines([str(frame_count), '\n' + str(fps)])


def check_if_loaded(working_folder):
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
