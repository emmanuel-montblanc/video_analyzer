"""
This modules contains AnalyzeViWindow, the class defining the interface to analyze the videos
"""

import sys

from PyQt5.QtCore import Qt, QPoint, QTimer, QRect
from PyQt5.QtGui import (
    QPixmap,
    QPainter,
    QPen,
    QKeySequence,
    QIcon,
    QColor,
    QFontDatabase,
)
from PyQt5.QtWidgets import (
    QMainWindow,
    QShortcut,
    QPushButton,
    QLabel,
    QTextEdit,
    QFrame,
    QApplication,
)

from recorder import Recorder
from style_sheets import (
    wndw_style,
    lbl_style,
    btn_style,
    btn_style_selected,
    btn_style_red,
    btn_style_red_selected,
    btn_style_green,
    btn_style_green_selected,
    dsply_txt_style,
    WHITE,
    RED,
    GREEN,
)


# TODO: Select second vid?

class AnalyzeVidWindow(QMainWindow):
    """
    Window made to analyze the videos
    :param: QMainWindow parent_window: the window that created this one, so we can go back to it if
    we want to change video
    :param: str video_name: the name of the video we're analyzing
    """

    def __init__(self, parent_window, video_name):
        super().__init__()

        self.parent_window = parent_window
        self.video_name = video_name

        self.init_window()

        with open("../videos/" + self.video_name + "/info.txt") as file:
            self.nb_frames = int(file.readline().strip())
            self.fps = int(file.readline().strip())

        self.current_frame = 0
        self.pixmap = QPixmap()
        self.screen_size = QApplication.primaryScreen().geometry()
        self.adapt_size()

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
        self.drawing_color = QColor(RED)

        self.frame = QFrame(self)
        self.frame.setGeometry(self.fixed_width, 10,
                               170, self.frameGeometry().height())

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

        # Shortcuts
        self.ctrlz = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.space_bar = QShortcut(QKeySequence(Qt.Key_Space), self)
        self.right_key = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.left_key = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.init_shortcuts()

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_update)
        self.timer.start(round(1000 / self.fps))

        # -----------------------------------------------
        # Compare
        self.button_compare_vid = QPushButton(self.frame)
        self.button_compare_vid.setText("Compare videos")
        self.button_compare_vid.setGeometry(10, 480, 150, 40)
        self.button_compare_vid.setStyleSheet(btn_style)
        self.button_compare_vid.clicked.connect(self.compare_video)

        self.button_zoom2 = QPushButton(self.frame)
        self.button_zoom2.setText("zoom 2")
        self.button_zoom2.setGeometry(90, 150, 70, 40)
        self.button_zoom2.setStyleSheet(btn_style)
        self.button_zoom2.clicked.connect(self.zoom_image)
        self.button_zoom2.hide()

        self.video_to_compare = "VID_20201105_150534_01"
        self.nb_frames_to_compare = 304
        self.current_frame_to_compare = 50
        self.compare_vid = False

        self.select_zooming2 = False
        self.zooming2 = False
        self.zoom_point2 = QPoint()
        self.zooming_rect2 = QRect()
        self.pixmap_to_compare = QPixmap(
            "../videos/" + self.video_to_compare + "/frame0.jpg"
        )
        self.vid_ratio_to_compare = (
            self.pixmap_to_compare.width() / self.pixmap_to_compare.height()
        )
        self.fixed_width_vid1 = self.fixed_width
        self.fixed_height_vid2 = self.pixmap.height()
        self.vid2_y_pos = 0

        # ------------------------------------------------

        self.show()

    def init_window(self):
        """
        Configure the title, icon and style sheet of the window
        """

        self.setWindowTitle(self.video_name)
        self.setWindowIcon(QIcon("../resources/diamond_twist.png"))
        self.setStyleSheet(wndw_style)

    def adapt_size(self):
        """
        Adapt the size of the video and of the window,
        if the video + the button would be larger than the screen, reduce its size,
        if the video is too small compared to the buttons, increase its size
        """

        self.pixmap = QPixmap("../videos/" + self.video_name + "/frame0.jpg")

        if self.pixmap.width() >= self.screen_size.width() - 200:
            self.pixmap = self.pixmap.scaledToWidth(self.screen_size.width() - 200)
        if self.pixmap.height() >= self.screen_size.height() - 120:
            self.pixmap = self.pixmap.scaledToHeight(self.screen_size.height() - 120)
        if self.pixmap.height() < 530:
            self.pixmap = self.pixmap.scaledToHeight(530)
        self.resize(self.pixmap.width() + 170, self.pixmap.height() + 50)

    def init_widgets(self):
        """
        Initialize all the buttons,
        configure their text, size, positioning, style sheets, and the method their connected with
        """

        # Button help
        self.button_help.setText("help")
        self.button_help.setGeometry(10, 0, 150, 40)
        self.button_help.clicked.connect(self.help)
        self.button_help.setStyleSheet(btn_style)

        # Button change video
        self.button_change_vid.setText("change video")
        self.button_change_vid.setGeometry(10, 50, 150, 40)
        self.button_change_vid.clicked.connect(self.change_video)
        self.button_change_vid.setStyleSheet(btn_style)

        # Button record
        self.button_record.setText("start recording")
        self.button_record.setGeometry(10, 100, 150, 40)
        self.button_record.clicked.connect(self.record_video)
        self.button_record.setStyleSheet(btn_style)

        # Button zoom
        self.button_zoom.setText("zoom")
        self.button_zoom.setGeometry(10, 150, 150, 40)
        self.button_zoom.clicked.connect(self.zoom_image)
        self.button_zoom.setStyleSheet(btn_style)

        # Drawing widgets
        self.color_label.setText("drawing color:")
        self.color_label.setGeometry(30, 200, 150, 20)
        self.color_label.setStyleSheet(lbl_style)
        self.button_green.setGeometry(40, 220, 40, 40)
        self.button_green.clicked.connect(self.select_color)
        self.button_green.setStyleSheet(btn_style_green)
        self.button_red.setGeometry(90, 220, 40, 40)
        self.button_red.clicked.connect(self.select_color)
        self.button_red.setStyleSheet(btn_style_red_selected)
        self.button_ctrlz.setText("undo")
        self.button_ctrlz.setGeometry(10, 270, 150, 40)
        self.button_ctrlz.clicked.connect(self.remove_last_line)
        self.button_ctrlz.setStyleSheet(btn_style)

        # Playing widgets
        self.speed_label.setText("playing speed:")
        self.speed_label.setGeometry(30, 320, 150, 20)
        self.speed_label.setStyleSheet(lbl_style)
        self.speed_x1.setText("x1")
        self.speed_x1.setGeometry(10, 340, 150, 20)
        self.speed_x1.clicked.connect(self.set_speed)
        self.speed_x1.setStyleSheet(btn_style_selected)
        self.speed_x05.setText("x0.5")
        self.speed_x05.setGeometry(10, 360, 150, 20)
        self.speed_x05.clicked.connect(self.set_speed)
        self.speed_x05.setStyleSheet(btn_style)
        self.speed_x025.setText("x0.25")
        self.speed_x025.setGeometry(10, 380, 150, 20)
        self.speed_x025.clicked.connect(self.set_speed)
        self.speed_x025.setStyleSheet(btn_style)
        self.speed_x0125.setText("x0.125")
        self.speed_x0125.setGeometry(10, 400, 150, 20)
        self.speed_x0125.clicked.connect(self.set_speed)
        self.speed_x0125.setStyleSheet(btn_style)
        self.button_play_pause.setText("Play")
        self.button_play_pause.setGeometry(10, 430, 150, 40)
        self.button_play_pause.clicked.connect(self.play_pause_vid)
        self.button_play_pause.setStyleSheet(btn_style)

    def init_shortcuts(self):
        """
        Connects the shortcuts to their respective methods
        """

        self.ctrlz.activated.connect(self.remove_last_line)
        self.space_bar.activated.connect(self.play_pause_vid)
        self.right_key.activated.connect(self.next_frame)
        self.left_key.activated.connect(self.previous_frame)

    def paintEvent(self, event):
        """
        Paint event, called whenever self.update() is called,
        draw the current frame, the progress bar of the video, all the lines, and if we're selecting
        where to zoom, draw the zooming rectangle zone
        """

        painter = QPainter()
        painter.begin(self)

        painter.drawPixmap(self.pixmap.rect(), self.pixmap)
        if self.compare_vid:
            painter.drawPixmap(
                QRect(self.pixmap.width(), self.vid2_y_pos,
                      self.pixmap_to_compare.width(),
                      self.pixmap_to_compare.height()),
                self.pixmap_to_compare)
        self.draw_progress_bar(painter)
        self.draw_lines(painter)
        self.draw_zooming_rect(painter)

        painter.end()

    def draw_progress_bar(self, painter):
        """
        Display the progress of the video,
        just draw a line under the frame displayed, and draw a cursor on this line corresponding to
        the progress of the video
        :param QPainter painter: the current painter object
        """

        # Draw the progress bar
        painter.setPen(QPen(QColor(WHITE), 3, Qt.SolidLine))
        painter.drawLine(
            QPoint(0, self.frameGeometry().height() - 60),
            QPoint(self.pixmap.width(), self.frameGeometry().height() - 60),
        )

        # Draw the cursor on the progress bar
        painter.setPen(QPen(QColor(WHITE), 3, Qt.SolidLine))
        x_pos = int(self.current_frame * self.pixmap.width() / self.nb_frames)
        painter.drawLine(
            QPoint(x_pos, self.frameGeometry().height()),
            QPoint(x_pos, self.frameGeometry().height() - 80),
        )

        if self.compare_vid:
            # Draw the separation between the video
            painter.drawLine(
                QPoint(self.pixmap.width(), 0),
                QPoint(self.pixmap.width(), self.frameGeometry().height()),
            )

            # Draw the compare vid progress bar
            painter.setPen(QPen(QColor(WHITE), 3, Qt.SolidLine))
            painter.drawLine(
                QPoint(self.pixmap.width(), self.frameGeometry().height() - 60),
                QPoint(
                    self.pixmap.width() + self.pixmap_to_compare.width(),
                    self.frameGeometry().height() - 60,
                ),
            )

            # Draw the cursor on the compare vid progress bar
            x_compare_pos = int(
                self.current_frame_to_compare
                * self.pixmap_to_compare.width()
                / self.nb_frames_to_compare
            )
            painter.drawLine(
                QPoint(
                    x_compare_pos + self.pixmap.width(), self.frameGeometry().height()
                ),
                QPoint(
                    x_compare_pos + self.pixmap.width(),
                    self.frameGeometry().height() - 80,
                ),
            )

    def draw_lines(self, painter):
        """
        draw all the line drawn, and the line we're currently drawing
        :param QPainter painter: the current painter object
        """

        # Draw the finished lines
        for line_group in self.lines:
            painter.setPen(QPen(line_group[0][2], 3, Qt.SolidLine))
            for line in line_group:
                painter.drawLine(line[0], line[1])

        # Draw the line we are currently drawing
        painter.setPen(QPen(self.drawing_color, 3, Qt.SolidLine))
        for line in self.current_line:
            painter.drawLine(line[0], line[1])

    def draw_zooming_rect(self, painter):
        """
        if we are currently selecting where to zoom, draw the rectangle on where we will zoom
        :param QPainter painter: the current painter object
        """
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))

        if self.select_zooming and self.zoom_point != QPoint():
            painter.drawRect(self.zooming_rect)

        if self.compare_vid and self.select_zooming2 and self.zoom_point2 != QPoint():
            painter.drawRect(self.zooming_rect2)

    def mouseMoveEvent(self, event):
        """
        Mouse movement event, called whenever we move our mouse
        if we are currently drawing, append the current position of the mouse to the list of point
        of the current line
        if we are selecting where to zoom, updates the size the zoom rectangle
        if we are playing using the right click of our mouse, updates the current frame to the frame
        corresponding to where we clicked
        updates the window after this
        """

        # Append pos to line if we are drawing
        if event.buttons() and Qt.LeftButton and self.drawing:
            if event.x() < self.pixmap.width() and event.y() < self.pixmap.height():
                self.current_line.append((self.lastPoint, event.pos(), self.drawing_color))
                self.lastPoint = event.pos()

        # Update zooming rectangle if we are selecting the zoom
        if event.buttons() and Qt.LeftButton and self.select_zooming:
            rect_width = event.x() - self.zoom_point.x()
            if rect_width < 20:
                rect_width = 20
            if event.x() >= self.pixmap.width():
                rect_width = self.pixmap.width() - self.zoom_point.x()
            self.zooming_rect = QRect(
                self.zoom_point.x(),
                self.zoom_point.y(),
                rect_width,
                round(rect_width / self.vid_ratio),
            )

        if event.buttons() and Qt.LeftButton and self.select_zooming2:
            rect_width = event.x() - self.zoom_point2.x()
            if rect_width < 20:
                rect_width = 20
            if event.x() - self.pixmap.width() >= self.pixmap_to_compare.width():
                rect_width = (
                    self.pixmap.width()
                    + self.pixmap_to_compare.width()
                    - self.zoom_point2.x()
                )
            if (event.y() >= self.pixmap_to_compare.height() + self.vid2_y_pos) or (rect_width / self.vid_ratio_to_compare + self.zoom_point2.y() > self.pixmap_to_compare.height() + self.vid2_y_pos):
                rect_width = round((self.pixmap_to_compare.height() + self.vid2_y_pos
                              - self.zoom_point2.y())\
                             * self.vid_ratio_to_compare)

            self.zooming_rect2 = QRect(
                self.zoom_point2.x(),
                self.zoom_point2.y(),
                rect_width,
                round(rect_width / self.vid_ratio_to_compare),
            )

        # Update the current frame if we are playing the video using the right click
        if event.buttons() and Qt.RightButton and self.playing_using_mouse:
            self.update_current_frame(event.pos().x())

        self.update()

    def mousePressEvent(self, event):
        """
        Mouse pressed event, called whenever we do press a button on our mouse,
        if we are not selecting where to zoom, if we do a left click we start drawing, and if we do
        a right we can play the video using our mouse
        if we are selecting where to zoom, a left click set up the origin of our zooming rectangle,
        and a right click cancel the zoom
        """

        if event.button() == Qt.LeftButton:
            if self.select_zooming:
                self.zoom_point = event.pos()
                if self.zoom_point.x() > self.pixmap.width() - 20:
                    self.zoom_point = QPoint(self.pixmap.width() - 25, self.zoom_point.y())
            elif self.select_zooming2 and self.compare_vid:
                x_point2, y_point2 = event.pos().x(), event.pos().y()
                if x_point2 < self.pixmap.width():
                    x_point2 = self.pixmap.width()
                if y_point2 < self.vid2_y_pos:
                    y_point2 = self.vid2_y_pos
                if y_point2 > self.fixed_height_vid2 + self.vid2_y_pos - 20:
                    y_point2 = self.fixed_height_vid2 + self.vid2_y_pos - 20
                self.zoom_point2 = QPoint(x_point2, y_point2)
            else:
                self.drawing = True
                self.lastPoint = event.pos()

        if event.button() == Qt.RightButton:
            if self.select_zooming:
                self.unzoom(self.button_zoom)
            elif self.select_zooming2:
                self.unzoom(self.button_zoom2)
            else:
                self.update_current_frame(event.pos().x())
                self.playing_using_mouse = True

    def mouseReleaseEvent(self, event):
        """
        Mouse release event, called whenever we release the click on our mouse
        if we were drawing, releasing the left click will finish the current line and stop drawing
        if we were playing the video with our mouse, releasing the right click will stop playing
        the video with our mouse
        and if we were selecting where to zoom, releasing the left click will validate the current
        zooming rectangle and zoom on the image
        """

        if event.button() == Qt.LeftButton:
            if self.select_zooming:
                rect_width = event.x() - self.zoom_point.x()
                self.zooming_rect = QRect(
                    self.zoom_point.x(),
                    self.zoom_point.y(),
                    rect_width,
                    round(rect_width / self.vid_ratio),
                )
                self.zoom_point = QPoint()
                self.select_zooming = False
                self.zooming = True
                self.load_current_frame()
                self.update()

            elif self.select_zooming2:
                rect_width = event.x() - self.zoom_point2.x()
                self.zooming_rect2 = QRect(
                    self.zoom_point2.x(),
                    self.zoom_point2.y(),
                    rect_width,
                    round(rect_width / self.vid_ratio_to_compare),
                )
                self.zoom_point2 = QPoint()
                self.select_zooming2 = False
                self.zooming2 = True
                self.load_current_frame()
                self.update()

            else:
                if self.current_line:
                    self.lines.append(self.current_line)
                self.current_line = []
                self.drawing = False

        if event.button() == Qt.RightButton:
            self.playing_using_mouse = False

    def update_current_frame(self, x_pos):
        """
        Method called when playing the video by using the right click
        Get the position of the mouse on the frame, find the frame number corresponding to this
        position, check if the frame number is valid, and loads it.
        :param: x_pos: the x position of the mouse
        """

        if self.compare_vid and x_pos >= self.pixmap.width():
            relative_pos = (
                x_pos - self.pixmap.width()
            ) / self.pixmap_to_compare.width()
            self.current_frame_to_compare = int(
                relative_pos * self.nb_frames_to_compare
            )
        else:
            relative_pos = x_pos / self.pixmap.width()
            self.current_frame = int(relative_pos * self.nb_frames)

        self.check_current_frame()
        self.load_current_frame()

    def check_current_frame(self):
        """
        Checks if the current frame number is not greater than the total number of frames
        and that the current frame is not a negative number
        """

        if self.current_frame > self.nb_frames:
            self.current_frame = self.nb_frames
        if self.current_frame < 0:
            self.current_frame = 0

        if self.compare_vid:
            if self.current_frame_to_compare > self.nb_frames_to_compare:
                self.current_frame_to_compare = self.nb_frames_to_compare
            if self.current_frame_to_compare < 0:
                self.current_frame_to_compare = 0

    def load_current_frame(self):
        """
        Load the image corresponding to the current frame,
        if we are zooming, also zoom on the loaded image
        """

        self.pixmap = QPixmap("../videos/" + self.video_name +
                              "/frame" + str(self.current_frame) + ".jpg")
        self.pixmap = self.pixmap.scaledToWidth(self.fixed_width)

        if self.compare_vid:
            self.pixmap = self.pixmap.scaledToWidth(self.fixed_width_vid1)
            self.pixmap_to_compare = QPixmap(
                "../videos/"
                + self.video_to_compare
                + "/frame"
                + str(self.current_frame_to_compare)
                + ".jpg"
            )
            self.pixmap_to_compare = self.pixmap_to_compare.scaledToHeight(self.fixed_height_vid2)
            while self.pixmap_to_compare.width() + self.pixmap.width() + 170 \
                    >= self.screen_size.width():
                self.fixed_height_vid2 = round(self.fixed_height_vid2 / 2)
                self.pixmap_to_compare = self.pixmap_to_compare.scaledToHeight(
                    self.fixed_height_vid2)
                self.vid2_y_pos = round((self.pixmap.height() - self.fixed_height_vid2) / 2)

            if self.zooming:
                copy = self.pixmap.copy(self.zooming_rect)
                self.pixmap = copy
                self.pixmap = copy.scaledToWidth(self.fixed_width_vid1)

            if self.zooming2:
                copy = self.pixmap_to_compare.copy(
                    QRect(
                        self.zooming_rect2.x() - self.pixmap.width(),
                        self.zooming_rect2.y() - self.vid2_y_pos,
                        self.zooming_rect2.width(),
                        self.zooming_rect2.height(),
                    )
                )
                self.pixmap_to_compare = copy.scaledToHeight(self.fixed_height_vid2)

        elif self.zooming:
            copy = self.pixmap.copy(self.zooming_rect)
            self.pixmap = copy.scaledToWidth(self.fixed_width)

    def remove_last_line(self):
        """
        Method called when clicking on 'undo' button or when pressing Ctrl + z
        Remove the last line draw
        """

        if self.lines:
            self.lines.pop()
            self.update()

    def select_color(self):
        """
        Method called when clicking on one of the color buttons
        Get which button was clicked and set the current drawing color to the corresponding color
        """

        sender = self.sender()
        if sender is self.button_green:
            self.drawing_color = QColor(GREEN)
            self.button_green.setStyleSheet(btn_style_green_selected)
            self.button_red.setStyleSheet(btn_style_red)
        if sender is self.button_red:
            self.drawing_color = QColor(RED)
            self.button_green.setStyleSheet(btn_style_green)
            self.button_red.setStyleSheet(btn_style_red_selected)

    def play_pause_vid(self):
        """
        Method called when either clicking on the play/pause button, or pressing the spacebar
        if the video was playing, pause it, and if the video was in pause, plays it
        """

        if self.play_using_button:
            self.button_play_pause.setText("play")
            self.play_using_button = False
        else:
            self.button_play_pause.setText("pause")
            self.play_using_button = True

    def next_frame(self):
        """
        Method called automatically by the timer when playing the video,
        but can also be called by using the right arrow of the keyboard,
        Simply increase the current frame number by one,
        then checks if it is valid, load it and updates the window
        """

        self.current_frame += 1

        if self.compare_vid:
            self.current_frame_to_compare += 1

        self.check_current_frame()
        self.load_current_frame()
        self.update()

    def previous_frame(self):
        """
        Method called by pressing the left arrow of the keyboard,
        does the same as the method next_frame, but instead of increasing the current frame number
        by one, it decreases it by one
        """

        self.current_frame -= 1
        self.check_current_frame()
        self.load_current_frame()
        self.update()

    def set_speed(self):
        """
        Method called when clicking on one of the speed buttons
        Get which button was clicked and set the playing speed to the corresponding value
        """

        sender = self.sender()
        speed = 1
        if sender is self.speed_x05:
            speed = 0.5
        if sender is self.speed_x025:
            speed = 0.25
        if sender is self.speed_x0125:
            speed = 0.125
        self.highlight_selected_speed(sender)
        refresh_rate = round(1000 / (self.fps * speed))
        self.timer.start(refresh_rate)

    def highlight_selected_speed(self, selected_btn):
        """
        Method after a speed button was clicked,
        Set the style sheet of every speed button to the default one,
        then set the style sheet of the selected button to the highlighted one
        :param QPushButton selected_btn: the selected speed button
        """

        self.speed_x1.setStyleSheet(btn_style)
        self.speed_x05.setStyleSheet(btn_style)
        self.speed_x025.setStyleSheet(btn_style)
        self.speed_x0125.setStyleSheet(btn_style)
        selected_btn.setStyleSheet(btn_style_selected)

    def timer_update(self):
        """
        Timer method, is called periodically based on the playing speed
        If we are currently playing the video, call the method next_frame()
        """
        if self.play_using_button:
            self.next_frame()

    def record_video(self):
        """
        Method called when clicking on the start/stop recording button,
        simply start recording if we weren't, and if we were recording then stop recording
        """

        if self.button_record.text() == "start recording":
            self.recorder.start_recording()
            self.button_record.setText("stop recording")
        else:
            self.recorder.stop_recording()
            self.button_record.setText("start recording")

    def zoom_image(self):
        """
        Method called when clicking on the zoom button,
        start zooming if you left click where you want to zoom on the video
        """

        sender = self.sender()

        if sender is self.button_zoom:
            self.select_zooming = True
            self.button_zoom.setText("Unzoom")
            self.button_zoom.clicked.connect(lambda: self.unzoom(self.button_zoom))
        else:
            self.select_zooming2 = True
            self.button_zoom2.setText("Unzoom")
            self.button_zoom2.clicked.connect(lambda: self.unzoom(self.button_zoom2))

    def unzoom(self, zoom_btn):
        """
        Method called when clicking on the unzoom button,
        simply stop zooming, reset the zooming rectangle, reload the frame and updates the window
        """

        if self.compare_vid and zoom_btn == self.button_zoom2:
            zoom_btn.setText("zoom 2")
            self.zooming2 = False
            self.select_zooming2 = False
            self.zoom_point2 = QPoint()

        else:
            if self.compare_vid:
                zoom_btn.setText("zoom 1")
            else:
                zoom_btn.setText("zoom")
            self.zooming = False
            self.select_zooming = False
            self.zoom_point = QPoint()

        zoom_btn.clicked.connect(self.zoom_image)

        self.load_current_frame()
        self.update()

    def help(self):
        """
        Method called when clicking on the help button,
        open the help window, displaying a help on how to use the interface
        """

        self.help_wdw = HelpWindow(self.screen_size)
        self.help_wdw.show()

    def change_video(self):
        """
        Method called when clicking on the "Change video" button,
        return to the select_vid window, and close this one
        """

        # Stop the recording before leaving
        if self.button_record.text() == "stop recording":
            self.record_video()

        # return to the select video windows
        self.parent_window.show()
        self.close()

    def compare_video(self):
        if not self.compare_vid:
            self.unzoom(self.button_zoom)
            self.compare_vid = True
            if self.pixmap.width() * 2 + 170 >= self.screen_size.width():
                self.fixed_width_vid1 = round(self.fixed_width / 2)

            self.load_current_frame()
            self.resize(
                self.pixmap.width() + self.pixmap_to_compare.width() + 170,
                self.pixmap.height() + 50,
            )
            if self.geometry().height() < 560:
                self.resize(self.pixmap.width() + self.pixmap_to_compare.width() + 170, 560)

            self.frame.setGeometry(self.pixmap.width() + self.pixmap_to_compare.width(), 10,
                                   170, self.frameGeometry().height())

            self.button_zoom.setGeometry(10, 150, 75, 40)
            self.button_zoom.setText("zoom 1")
            self.button_zoom2.show()
        else:
            self.compare_vid = False
            self.button_zoom2.hide()
            self.button_zoom.setGeometry(10, 150, 150, 40)
            self.button_zoom.setText("zoom")
            self.adapt_size()


class HelpWindow(QMainWindow):
    """
    Class defining the help window,
    it simply load the text from /resources/help.txt and displays it
    """

    def __init__(self, screen_size):
        super().__init__()
        self.resize(round(screen_size.width() * 0.8), round(screen_size.height() * 0.8))
        self.setWindowTitle("Help")

        self.displayer = QTextEdit(self)
        self.displayer.setGeometry(0, 0,
                                   round(screen_size.width() * 0.8),
                                   round(screen_size.height() * 0.8))
        self.displayer.setStyleSheet(dsply_txt_style)

        text = open("../resources/help.txt").read()
        self.displayer.setPlainText(text)
        self.displayer.setReadOnly(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("../resources/JetBrainsMono-Regular.ttf")
    # print(QFontDatabase().families())
    # main_window = AnalyzeVidWindow("", "VID_20210228_143048_01")
    main_window = AnalyzeVidWindow("", "21-02-28-16-16-22")
    sys.exit(app.exec_())
