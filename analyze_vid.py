import shutil
import time
from datetime import datetime

from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QPen, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QShortcut, QPushButton, QLabel, QMessageBox

from screen_recorder import ScreenRecorder
from audi_recorder import AudioRecorder
from merge_audio_screen import merge


class AnalyzeVidWindow(QMainWindow):

    def __init__(self, master_window, video_name):
        super().__init__()
        self.resize(1380, 770)

        self.master_window = master_window

        self.video_name = video_name
        with open("./videos/" + video_name + "/info.txt") as file:
            self.nb_frames = int(file.readline().strip())
            self.fps = int(file.readline().strip())

        self.current_frame = 0
        self.pixmap = QPixmap("./videos/" + self.video_name + "/frame0.jpg")
        if self.pixmap.width() >= 1920:
            self.pixmap = self.pixmap.scaledToWidth(1280)
        if self.pixmap.height() >= 1080:
            self.pixmap = self.pixmap.scaledToHeight(720)
        self.resize(self.pixmap.width() + 100, self.pixmap.height() + 50)

        self.screen_recorder = ScreenRecorder()
        self.audio_recorder = AudioRecorder()

        self.now = datetime.now()

        self.drawing = False
        self.playing_using_mouse = False
        self.play_using_button = False

        self.lastPoint = QPoint()
        self.lines = []
        self.current_line = []
        self.drawing_color = Qt.red

        # Undo button
        self.button_ctrlz = QPushButton(self)
        self.button_ctrlz.setText("undo")
        self.button_ctrlz.setGeometry(self.frameGeometry().width() - 85, 50, 80, 40)
        self.button_ctrlz.clicked.connect(self.remove_last_line)

        # Undo shortcut
        self.ctrlz = QShortcut(QKeySequence('Ctrl+Z'), self)
        self.ctrlz.activated.connect(self.remove_last_line)

        # Label for choosing colors
        self.color_label = QLabel(self)
        self.color_label.setText("drawing color:")
        self.color_label.setGeometry(self.frameGeometry().width() - 80, 150, 80, 40)

        # green color button
        self.button_green = QPushButton(self)
        self.button_green.setStyleSheet("background-color: green")
        self.button_green.setGeometry(self.frameGeometry().width() - 85, 180, 40, 40)
        self.button_green.clicked.connect(lambda: self.select_color(Qt.darkGreen))

        # red color button
        self.button_red = QPushButton(self)
        self.button_red.setStyleSheet("background-color: red")
        self.button_red.setGeometry(self.frameGeometry().width() - 42, 180, 40, 40)
        self.button_red.clicked.connect(lambda: self.select_color(Qt.red))

        # Label for choosing colors
        self.speed_label = QLabel(self)
        self.speed_label.setText("playing speed:")
        self.speed_label.setGeometry(self.frameGeometry().width() - 80, 250, 80, 40)

        # x1 speed button
        self.speed_x1 = QPushButton(self)
        self.speed_x1.setText("x1")
        self.speed_x1.setGeometry(self.frameGeometry().width() - 85, 280, 80, 20)
        self.speed_x1.clicked.connect(lambda: self.set_speed(1))

        # x0.5 speed button
        self.speed_x05 = QPushButton(self)
        self.speed_x05.setText("x0.5")
        self.speed_x05.setGeometry(self.frameGeometry().width() - 85, 300, 80, 20)
        self.speed_x05.clicked.connect(lambda: self.set_speed(0.5))

        # x0.25 speed button
        self.speed_x025 = QPushButton(self)
        self.speed_x025.setText("x0.25")
        self.speed_x025.setGeometry(self.frameGeometry().width() - 85, 320, 80, 20)
        self.speed_x025.clicked.connect(lambda: self.set_speed(0.25))

        # x0.125 speed button
        self.speed_x0125 = QPushButton(self)
        self.speed_x0125.setText("x0.125")
        self.speed_x0125.setGeometry(self.frameGeometry().width() - 85, 340, 80, 20)
        self.speed_x0125.clicked.connect(lambda: self.set_speed(0.125))

        # Play button
        self.button_play = QPushButton(self)
        self.button_play.setText("Play")
        self.button_play.setGeometry(self.frameGeometry().width() - 85, 380, 40, 40)
        self.button_play.clicked.connect(self.play_vid)

        # Pause button
        self.button_pause = QPushButton(self)
        self.button_pause.setText("Pause")
        self.button_pause.setGeometry(self.frameGeometry().width() - 42, 380, 40, 40)
        self.button_pause.clicked.connect(self.pause_vid)

        # Play pause shortcut
        self.space_bar = QShortcut(QKeySequence("Space"), self)
        self.space_bar.activated.connect(self.space_bar_pressed)

        # Record button
        self.button_record = QPushButton(self)
        self.button_record.setText("start recording")
        self.button_record.setGeometry(self.frameGeometry().width() - 85, 450, 80, 40)
        self.button_record.clicked.connect(self.record_video)

        # change video button
        self.button_change_vid = QPushButton(self)
        self.button_change_vid.setText("change video")
        self.button_change_vid.setGeometry(self.frameGeometry().width() - 85, 500, 80, 40)
        self.button_change_vid.clicked.connect(self.change_video)

        # Timer for playing video
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_update)
        self.timer.start(round(1000/self.fps))

        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        # Draw the video
        painter.drawPixmap(self.pixmap.rect(), self.pixmap)

        # Draw the progress bar of the video
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.drawLine(QPoint(0, self.frameGeometry().height() - 60),
                         QPoint(self.pixmap.width(), self.frameGeometry().height()-60))

        # Draw the cursor on the progress bar
        painter.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
        x_pos = int(self.current_frame * self.pixmap.width() / self.nb_frames)
        painter.drawLine(QPoint(x_pos, self.frameGeometry().height()),
                         QPoint(x_pos, self.frameGeometry().height() - 80))

        # Draw the finished lines
        for line_group in self.lines:
            painter.setPen(QPen(line_group[0][2], 3, Qt.SolidLine))
            for line in line_group:
                painter.drawLine(line[0], line[1])

        # Draw the line we are currently drawing
        painter.setPen(QPen(self.drawing_color, 3, Qt.SolidLine))
        for line in self.current_line:
            painter.drawLine(line[0], line[1])
        painter.end()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            if event.x() < self.pixmap.width() and event.y() < self.pixmap.height():
                self.current_line.append((self.lastPoint, event.pos(), self.drawing_color))
                self.lastPoint = event.pos()
                self.update()

        if event.buttons() and Qt.RightButton and self.playing_using_mouse:
            self.update_current_frame(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

        if event.button() == Qt.RightButton:
            self.update_current_frame(event)
            self.playing_using_mouse = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.current_line:
                self.lines.append(self.current_line)
            self.current_line = []
            self.drawing = False

        if event.button() == Qt.RightButton:
            self.playing_using_mouse = False

    def update_current_frame(self, event):
        relative_pos = event.pos().x() / self.pixmap.width()
        self.current_frame = int(relative_pos * self.nb_frames)

        self.check_current_frame()
        self.load_current_frame()
        self.update()

    def check_current_frame(self):
        if self.current_frame > self.nb_frames:
            self.current_frame = self.nb_frames
        if self.current_frame < 0:
            self.current_frame = 0

    def load_current_frame(self):
        self.pixmap = QPixmap("./videos/" + self.video_name + "/frame" + str(self.current_frame) + ".jpg")
        self.pixmap = self.pixmap.scaledToWidth(my_round(self.frameGeometry().width() - 90))

    def remove_last_line(self):
        if self.lines:
            self.lines.pop()
            self.update()

    def select_color(self, color):
        self.drawing_color = color

    def play_vid(self):
        self.play_using_button = True

    def pause_vid(self):
        self.play_using_button = False

    def space_bar_pressed(self):
        if self.play_using_button:
            self.play_using_button = False
        else:
            self.play_using_button = True

    def set_speed(self, speed):
        refresh_rate = round(1000/(self.fps * speed))
        self.timer.start(refresh_rate)

    def timer_update(self):
        if self.play_using_button:
            self.current_frame += 1
            self.check_current_frame()
            self.load_current_frame()
            self.update()

    def record_video(self):
        if self.button_record.text() == "start recording":
            self.screen_recorder.start_recording()
            self.audio_recorder.start_recording()
            self.button_record.setText("stop recording")
        else:
            self.screen_recorder.stop_recording()
            self.audio_recorder.stop_recording()
            merge(self.video_name)

    def change_video(self):
        self.master_window.show()
        self.close()


def my_round(x, base=5):
    return base * round(x/base)

