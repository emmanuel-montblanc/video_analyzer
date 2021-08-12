import cv2
import numpy as np
import pyautogui
import threading
import time


class ScreenRecorder:
    def __init__(self):
        self.screen_size = pyautogui.size()
        self.fps = 15
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.writer = cv2.VideoWriter("./temp/screen.avi", self.codec, self.fps, self.screen_size)

        self.recording_thread = threading.Thread(target=self._record)

    def start_recording(self):
        self.recording_thread.start()
        print("started")

    def _record(self):
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
        self.recording_thread.recording = False


if __name__ == '__main__':
    sr = ScreenRecorder()
    time.sleep(20)
    print("stoping")
    sr.stop_recording()
