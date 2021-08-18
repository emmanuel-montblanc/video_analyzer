import sys
from pathlib import Path

import requests
from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QLabel, QLineEdit, \
    QMessageBox, QFrame

from analyze_vid import AnalyzeVidWindow
from download_vid import download_from_instagram
from get_frames_from_vid import get_frames
from style_sheets import wndw_style, btn_style, lbl_style, entry_style


class SelectVidWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(720, 480)
        self.setWindowTitle("Video analyzer")
        self.setWindowIcon(QIcon("../resources/diamond_twist.png"))
        self.setStyleSheet(wndw_style)

        self.analyze_window = QMainWindow()

        self.video_path = Path()

        # Frame for the 2 main buttons
        self.frame_main_buttons = QFrame(self)
        self.frame_main_buttons.setGeometry(0, 0, self.geometry().width(), self.geometry().height())

        # Select local video button
        self.local_vid_btn = QPushButton(self.frame_main_buttons)
        self.local_vid_btn.setText("Analyze local\n video")
        self.local_vid_btn.setGeometry(150, round(self.frameGeometry().height()/2), 150, 50)
        self.local_vid_btn.clicked.connect(self.select_local_vid)
        self.local_vid_btn.setStyleSheet(btn_style)

        # Select instagram video button
        self.insta_vid_btn = QPushButton(self.frame_main_buttons)
        self.insta_vid_btn.setText("Analyze instagram\n video")
        self.insta_vid_btn.setGeometry(self.frameGeometry().width() - 300,
                                       round(self.frameGeometry().height()/2), 150, 50)
        self.insta_vid_btn.clicked.connect(self.select_insta_vid)
        self.insta_vid_btn.setStyleSheet(btn_style)

        # Frame for selecting insta video
        self.frame_select_insta = QFrame(self)
        self.frame_select_insta.setGeometry(0, 0, self.geometry().width(), self.geometry().height())

        # info label
        self.insta_label = QLabel(self.frame_select_insta)
        self.insta_label.setText("Enter the instagram post URL")
        self.insta_label.setGeometry(round(self.frameGeometry().width()/2) - 100,
                                     round(self.frameGeometry().height() / 2) - 40,
                                     200, 40)
        self.insta_label.setStyleSheet(lbl_style)

        # Download button
        self.download_btn = QPushButton(self.frame_select_insta)
        self.download_btn.setText("Ok")
        self.download_btn.setGeometry(210,
                                    round(self.frameGeometry().height()/2) + 45, 100, 40)
        self.download_btn.clicked.connect(self.download_vid)
        self.download_btn.setStyleSheet(btn_style)

        # Return button
        self.return_btn = QPushButton(self.frame_select_insta)
        self.return_btn.setText("return")
        self.return_btn.setGeometry(410,
                                    round(self.frameGeometry().height()/2) + 45, 100, 40)
        self.return_btn.clicked.connect(self.return_home_page)
        self.return_btn.setStyleSheet(btn_style)

        # url entry
        self.url_entry = QLineEdit(self.frame_select_insta)
        self.url_entry.setGeometry(210, round(self.frameGeometry().height()/2), 300, 40)
        self.url_entry.setStyleSheet(entry_style)
        self.frame_select_insta.hide()

        self.show()

    def select_local_vid(self):
        dialog_result = QFileDialog.getOpenFileName(self, 'Select video',
                                                    'c:\\', "Video files (*.mp4 *.vid *.raw)")
        video_path = Path(dialog_result[0])
        print(video_path)

        if video_path != Path("."):
            self.video_path = video_path
            self.start_analyze()

    def select_insta_vid(self):
        self.frame_select_insta.show()
        self.frame_main_buttons.hide()

    def return_home_page(self):
        self.frame_select_insta.hide()
        self.frame_main_buttons.show()

    def download_vid(self):
        url = self.url_entry.text()
        if url:
            try:
                file_name = download_from_instagram(url)
                self.video_path = Path.cwd().parent / "insta_videos" / file_name
                self.start_analyze()
            except requests.exceptions.MissingSchema:
                error_pop_up = QMessageBox(self)
                error_pop_up.setIcon(QMessageBox.Critical)
                error_pop_up.setText('Invalid instagram post url')
                error_pop_up.show()

    def start_analyze(self):
        get_frames(self.video_path)
        self.analyze_window = AnalyzeVidWindow(self, self.video_path.stem)
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("../resources/JetBrainsMono-Regular.ttf")
    main_window = SelectVidWindow()
    sys.exit(app.exec_())
