"""
This module allows you to record your screen and the audio from your microphone
"""

import subprocess
import threading
import time
import wave
from pathlib import Path

import cv2
import numpy as np
import pyaudio
import pyautogui


class Recorder:
    """
    This class creates an instance of AudioRecorder and of ScreenRecorder, to capture both audio
    and video, and then merge the two together using ffmpeg.
    :param: str video_name: the name of the video we're analysing (is used to name the output file)
    """

    def __init__(self, video_name):
        self.video_name = video_name

        _create_temp_folder()

        self.audio_recorder = AudioRecorder()
        self.screen_recorder = ScreenRecorder()

    def start_recording(self):
        """
        Start recording the audio and the video
        :return: None
        """

        self.audio_recorder.start_recording()
        self.screen_recorder.start_recording()

    def stop_recording(self):
        """
        Stop recording the audio and the video, then merge the two together
        :return: None
        """

        self.audio_recorder.stop_recording()
        self.screen_recorder.stop_recording()
        self.merge_audio_video()

    def merge_audio_video(self):
        """
        Merge the audio and the video in a mkv file by using ffmpeg
        :return: None
        """

        self.audio_recorder.recording_thread.join()
        self.screen_recorder.recording_thread.join()

        _create_records_folder()
        output_path = self._get_output_path()

        cmd = "ffmpeg -i ../temp/screen.avi -i ../temp/audio.wav -shortest -c copy " + str(output_path)
        subprocess.call(cmd, shell=True)

    def _get_output_path(self):
        """
        Find a unused name for the output file, and returns the path to it
        :return: Path: the path to the output file
        """

        record_folder = Path.cwd().parent / "records"
        output_name = self.video_name + ".mkv"
        i = 0
        while (record_folder / output_name).exists():
            i += 1
            output_name = self.video_name + "_" + str(i) + ".mkv"

        output_path = record_folder / output_name
        return output_path


class AudioRecorder:
    """
    Audio recorder class, as the name indicates, it records audio and save it in the temp folder
    """

    def __init__(self):

        self.open = True
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "../temp/audio.wav"
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.audio_frames = []

        self.recording_thread = threading.Thread(target=self._record)

    def _record(self):
        """
        recording loop, continues until the attribute "recording" of the thread is set to False
        :return: None
        """

        curr_thread = threading.currentThread()

        self.stream.start_stream()

        while getattr(curr_thread, "recording", True):
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        waveFile = wave.open(self.audio_filename, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.audio.get_sample_size(self.format))
        waveFile.setframerate(self.rate)
        waveFile.writeframes(b''.join(self.audio_frames))
        waveFile.close()
        print("audio ended")

    def start_recording(self):
        """
        Start recording the audio in a separated thread
        :return: None
        """

        self.__init__()
        self.recording_thread.start()
        print("audio started")

    def stop_recording(self):
        """
        Stop recording by changing the attribute "recording" of the thread
        :return: None
        """

        self.recording_thread.recording = False


class ScreenRecorder:
    """
    Screen recorder class, it takes multiples screenshot and then assemble them into a vide,
    and save it in the temp folder
    """

    def __init__(self):
        self.screen_size = pyautogui.size()
        self.fps = 15
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.writer = cv2.VideoWriter("../temp/screen.avi", self.codec, self.fps, self.screen_size)

        self.recording_thread = threading.Thread(target=self._record)

    def start_recording(self):
        """
        Start recording the video in a separated thread
        :return: None
        """

        self.__init__()
        self.recording_thread.start()
        print("started")

    def _record(self):
        """
        recording loop, continues until the attribute "recording" of the thread is set to False
        :return: None
        """

        last_time = time.time()
        curr_thread = threading.currentThread()
        while getattr(curr_thread, "recording", True):
            if time.time() - last_time >= 1/self.fps:
                last_time = time.time()
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.writer.write(frame)

        self.writer.release()
        print("ended")

    def stop_recording(self):
        """
        Stop recording by changing the attribute "recording" of the thread
        :return: None
        """

        self.recording_thread.recording = False


def _create_temp_folder():
    """
    creates the folder "temp" if it doesnt exists
    :return: None
    """

    temp_folder = Path.cwd().parent / "temp"
    temp_folder.mkdir(parents=True, exist_ok=True)


def _create_records_folder():
    """
    creates the folder "records" if it doesnt exists
    :return: None
    """

    records_folder = Path.cwd() / "records"
    records_folder.mkdir(parents=True, exist_ok=True)
