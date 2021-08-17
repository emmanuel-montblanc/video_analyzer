import sys

from PyQt5.QtCore import Qt, QPoint, QTimer, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen, QKeySequence, QIcon, QFont, QColor
from PyQt5.QtWidgets import QMainWindow, QShortcut, QPushButton, QLabel, QTextEdit, QFrame, \
    QApplication

from recorder import Recorder
from style_sheets import wndw_style, btn_style, btn_style_red, btn_style_green, lbl_style, WHITE

# TODO: rendre le truc un peu moins moche
# TODO: comparer deux video


class AnalyzeVidWindow(QMainWindow):

    def __init__(self, master_window, video_name):
        super().__init__()

        self.master_window = master_window
        self.video_name = video_name

        self.resize(1380, 770)
        self.setWindowTitle(video_name)
        self.setWindowIcon(QIcon("diamond_twist.png"))
        self.setStyleSheet(wndw_style)

        with open("./videos/" + self.video_name + "/info.txt") as file:
            self.nb_frames = int(file.readline().strip())
            self.fps = int(file.readline().strip())

        self.current_frame = 0
        self.pixmap = QPixmap("./videos/" + self.video_name + "/frame0.jpg")
        if self.pixmap.width() >= 1920:
            self.pixmap = self.pixmap.scaledToWidth(1280)
        if self.pixmap.height() >= 1080:
            self.pixmap = self.pixmap.scaledToHeight(720)
        self.resize(self.pixmap.width() + 120, self.pixmap.height() + 50)

        self.fixed_width = self.pixmap.width()
        self.vid_ratio = self.pixmap.width() / self.pixmap.height()

        self.help_wdw = QMainWindow()
        self.recorder = Recorder(self.video_name)

        self.drawing = False
        self.playing_using_mouse = False
        self.play_using_button = False

        self.select_zooming = False
        self.zooming = False
        self.zoom_point = QPoint()
        self.zooming_rect = QRect()

        self.lastPoint = QPoint()
        self.lines = []
        self.current_line = []
        self.drawing_color = Qt.red

        self.frame = QFrame(self)
        self.frame.setGeometry(self.fixed_width, 20,
                               self.frameGeometry().width(), self.frameGeometry().height())

        # Help / change vid / record / zoom widgets
        self.button_help = QPushButton(self.frame)
        self.button_change_vid = QPushButton(self.frame)
        self.button_record = QPushButton(self.frame)
        self.button_zoom = QPushButton(self.frame)

        # Drawing widgets
        self.color_label = QLabel(self.frame)
        self.button_green = QPushButton(self.frame)
        self.button_red = QPushButton(self.frame)
        self.button_ctrlz = QPushButton(self.frame)

        # Playing widgets
        self.speed_label = QLabel(self.frame)
        self.speed_x1 = QPushButton(self.frame)
        self.speed_x05 = QPushButton(self.frame)
        self.speed_x025 = QPushButton(self.frame)
        self.speed_x0125 = QPushButton(self.frame)
        self.button_play_pause = QPushButton(self.frame)

        self.init_widgets()

        # Undo shortcut
        self.ctrlz = QShortcut(QKeySequence('Ctrl+Z'), self)
        self.ctrlz.activated.connect(self.remove_last_line)

        # Play pause shortcut
        self.space_bar = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.space_bar.activated.connect(self.play_pause_vid)

        # Next frame shortcut
        self.right_key = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.right_key.activated.connect(self.next_frame)

        # Previous frame shortcut
        self.left_key = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.left_key.activated.connect(self.previous_frame)

        # Timer for playing video
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_update)
        self.timer.start(round(1000/self.fps))

        self.show()

    def init_widgets(self):
        # Button help
        self.button_help.setText("help")
        self.button_help.setGeometry(10, 0, 100, 40)
        self.button_help.clicked.connect(self.help)
        self.button_help.setStyleSheet(btn_style)

        # Button change video
        self.button_change_vid.setText("change video")
        self.button_change_vid.setGeometry(10, 50, 100, 40)
        self.button_change_vid.clicked.connect(self.change_video)
        self.button_change_vid.setStyleSheet(btn_style)

        # Button record
        self.button_record.setText("start recording")
        self.button_record.setGeometry(10, 100, 100, 40)
        self.button_record.clicked.connect(self.record_video)
        self.button_record.setStyleSheet(btn_style)

        # Button zoom
        self.button_zoom.setText("zoom")
        self.button_zoom.setGeometry(10, 150, 100, 40)
        self.button_zoom.clicked.connect(self.zoom_image)
        self.button_zoom.setStyleSheet(btn_style)

        # Drawing widgets
        self.color_label.setText("drawing color:")
        self.color_label.setGeometry(20, 200, 100, 20)
        self.color_label.setStyleSheet(lbl_style)
        self.button_green.setGeometry(15, 220, 40, 40)
        self.button_green.clicked.connect(lambda: self.select_color(Qt.darkGreen))
        self.button_green.setStyleSheet(btn_style_green)
        self.button_red.setGeometry(60, 220, 40, 40)
        self.button_red.clicked.connect(lambda: self.select_color(Qt.red))
        self.button_red.setStyleSheet(btn_style_red)
        self.button_ctrlz.setText("undo")
        self.button_ctrlz.setGeometry(10, 270, 100, 40)
        self.button_ctrlz.clicked.connect(self.remove_last_line)
        self.button_ctrlz.setStyleSheet(btn_style)

        # Playing widgets
        self.speed_label.setText("playing speed:")
        self.speed_label.setGeometry(20, 320, 100, 20)
        self.speed_label.setStyleSheet(lbl_style)
        self.speed_x1.setText("x1")
        self.speed_x1.setGeometry(10, 340, 100, 20)
        self.speed_x1.clicked.connect(lambda: self.set_speed(1))
        self.speed_x1.setStyleSheet(btn_style)
        self.speed_x05.setText("x0.5")
        self.speed_x05.setGeometry(10, 360, 100, 20)
        self.speed_x05.clicked.connect(lambda: self.set_speed(0.5))
        self.speed_x05.setStyleSheet(btn_style)
        self.speed_x025.setText("x0.25")
        self.speed_x025.setGeometry(10, 380, 100, 20)
        self.speed_x025.clicked.connect(lambda: self.set_speed(0.25))
        self.speed_x025.setStyleSheet(btn_style)
        self.speed_x0125.setText("x0.125")
        self.speed_x0125.setGeometry(10, 400, 100, 20)
        self.speed_x0125.clicked.connect(lambda: self.set_speed(0.125))
        self.speed_x0125.setStyleSheet(btn_style)
        self.button_play_pause.setText("Play")
        self.button_play_pause.setGeometry(10, 430, 100, 40)
        self.button_play_pause.clicked.connect(self.play_pause_vid)
        self.button_play_pause.setStyleSheet(btn_style)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.drawPixmap(self.pixmap.rect(), self.pixmap)
        self.draw_progress_bar(painter)
        self.draw_lines(painter)
        self.draw_zooming_rect(painter)

        painter.end()

    def draw_zooming_rect(self, painter):
        if self.select_zooming and self.zoom_point != QPoint():
            painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
            painter.drawRect(self.zooming_rect)

    def draw_lines(self, painter):
        # Draw the finished lines
        for line_group in self.lines:
            painter.setPen(QPen(line_group[0][2], 3, Qt.SolidLine))
            for line in line_group:
                painter.drawLine(line[0], line[1])
        # Draw the line we are currently drawing
        painter.setPen(QPen(self.drawing_color, 3, Qt.SolidLine))
        for line in self.current_line:
            painter.drawLine(line[0], line[1])

    def draw_progress_bar(self, painter):
        # Draw the progress bar
        painter.setPen(QPen(QColor(WHITE), 3, Qt.SolidLine))
        painter.drawLine(QPoint(0, self.frameGeometry().height() - 60),
                         QPoint(self.pixmap.width(), self.frameGeometry().height() - 60))

        # Draw the cursor on the progress bar
        painter.setPen(QPen(QColor(WHITE), 3, Qt.SolidLine))
        x_pos = int(self.current_frame * self.pixmap.width() / self.nb_frames)
        painter.drawLine(QPoint(x_pos, self.frameGeometry().height()),
                         QPoint(x_pos, self.frameGeometry().height() - 80))

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            if event.x() < self.pixmap.width() and event.y() < self.pixmap.height():
                self.current_line.append((self.lastPoint, event.pos(), self.drawing_color))
                self.lastPoint = event.pos()

        if event.buttons() and Qt.LeftButton and self.select_zooming:
            self.zooming_rect = QRect(self.zoom_point.x(), self.zoom_point.y(),
                                      event.x(), event.x()/self.vid_ratio)

        if event.buttons() and Qt.RightButton and self.playing_using_mouse:
            self.update_current_frame(event)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.select_zooming:
                if self.zoom_point == QPoint():
                    self.zoom_point = event.pos()
            else:
                self.drawing = True
                self.lastPoint = event.pos()

        if event.button() == Qt.RightButton:
            if self.select_zooming:
                self.unzoom()
            else:
                self.update_current_frame(event)
                self.playing_using_mouse = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.select_zooming:
                self.zooming_rect = QRect(self.zoom_point.x(), self.zoom_point.y(),
                                          event.x(), event.x() / self.vid_ratio)
                self.zoom_point = QPoint()
                self.select_zooming = False
                self.zooming = True
                self.load_current_frame()
                self.update()
            else:
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

    def check_current_frame(self):
        if self.current_frame > self.nb_frames:
            self.current_frame = self.nb_frames
        if self.current_frame < 0:
            self.current_frame = 0

    def load_current_frame(self):
        self.pixmap = QPixmap("./videos/" + self.video_name + "/frame" + str(self.current_frame) + ".jpg")
        self.pixmap = self.pixmap.scaledToWidth(self.fixed_width)

        if self.zooming:
            copy = self.pixmap.copy(self.zooming_rect)
            self.pixmap = copy.scaledToWidth(self.fixed_width)

    def remove_last_line(self):
        if self.lines:
            self.lines.pop()
            self.update()

    def select_color(self, color):
        self.drawing_color = color

    def play_pause_vid(self):
        if self.play_using_button:
            self.button_play_pause.setText("play")
            self.play_using_button = False
        else:
            self.button_play_pause.setText("pause")
            self.play_using_button = True

    def next_frame(self):
        self.current_frame += 1
        self.check_current_frame()
        self.load_current_frame()
        self.update()

    def previous_frame(self):
        self.current_frame -= 1
        self.check_current_frame()
        self.load_current_frame()
        self.update()

    def set_speed(self, speed):
        refresh_rate = round(1000/(self.fps * speed))
        self.timer.start(refresh_rate)


    def timer_update(self):
        if self.play_using_button:
            self.next_frame()

    def record_video(self):
        if self.button_record.text() == "start recording":
            self.recorder.start_recording()
            self.button_record.setText("stop recording")
        else:
            self.recorder.stop_recording()
            self.button_record.setText("start recording")

    def change_video(self):
        # Stop the recording before leaving
        if self.button_record.text() == "stop recording":
            self.record_video()

        # return to the select video windows
        self.master_window.show()
        self.close()

    def zoom_image(self):
        if not self.zooming:
            self.select_zooming = True
            self.button_zoom.setText("Unzoom")
            self.button_zoom.clicked.connect(self.unzoom)

    def unzoom(self):
        self.button_zoom.setText("zoom")
        self.zooming = False
        self.select_zooming = False
        self.zoom_point = QPoint()

        self.button_zoom.clicked.connect(self.zoom_image)

        self.load_current_frame()
        self.update()

    def help(self):
        self.help_wdw = HelpWindow()
        self.help_wdw.show()


class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(720, 480)
        self.setWindowTitle("Help")

        self.displayer = QTextEdit(self)
        self.displayer.setGeometry(0, 0, 720, 480)
        self.displayer.setCurrentFont(QFont('Consolas, 12'))

        text = open("help.txt").read()
        self.displayer.setPlainText(text)
        self.displayer.setReadOnly(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = AnalyzeVidWindow("", "VID_20201026_190145")
    sys.exit(app.exec_())
