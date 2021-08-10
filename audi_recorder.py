import pyaudio
import wave
import threading
import time


class AudioRecorder:
    def __init__(self):

        self.open = True
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "./temp/audio.wav"
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.audio_frames = []

        self.recording_thread = threading.Thread(target=self.record)

    def record(self):
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
        print("ended")

    def start_recording(self):
        self.recording_thread.start()
        print("started")

    def stop_recording(self):
        self.recording_thread.recording = False


if __name__ == '__main__':
    ar = AudioRecorder()
    ar.start_recording()
    time.sleep(10)
    ar.stop_recording()


