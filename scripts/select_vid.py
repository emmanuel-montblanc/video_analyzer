import sys
from pathlib import Path

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QLabel, QLineEdit, \
    QMessageBox, QFrame, QProgressBar

from analyze_vid import AnalyzeVidWindow
from download_vid import download_from_instagram
from get_frames_from_vid import ExtractFramesThread
from style_sheets import wndw_style, btn_style, lbl_style, lbl_state_style, entry_style


# TODO: add a loading bar, when extracting the frames


class SelectVidWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(720, 480)
        self.setWindowTitle("Video analyzer")
        self.setWindowIcon(QIcon("../resources/diamond_twist.png"))
        self.setStyleSheet(wndw_style)

        self.analyze_window = QMainWindow()
        self.thread = QThread()

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

        # enter url label
        self.insta_lbl = QLabel(self.frame_select_insta)
        self.insta_lbl.setText("Enter the instagram post URL")
        self.insta_lbl.setGeometry(round(self.frameGeometry().width() / 2) - 100,
                                   round(self.frameGeometry().height() / 2) - 40,
                                   200, 40)
        self.insta_lbl.setStyleSheet(lbl_style)

        # Download button
        self.download_btn = QPushButton(self.frame_select_insta)
        self.download_btn.setText("Ok")
        self.download_btn.setGeometry(185,
                                    round(self.frameGeometry().height()/2) + 45, 150, 40)
        self.download_btn.clicked.connect(self.download_vid)
        self.download_btn.setStyleSheet(btn_style)

        # Return button
        self.return_btn = QPushButton(self.frame_select_insta)
        self.return_btn.setText("return")
        self.return_btn.setGeometry(385,
                                    round(self.frameGeometry().height()/2) + 45, 150, 40)
        self.return_btn.clicked.connect(self.return_home_page)
        self.return_btn.setStyleSheet(btn_style)

        # url entry
        self.url_entry = QLineEdit(self.frame_select_insta)
        self.url_entry.setGeometry(185, round(self.frameGeometry().height()/2), 350, 40)
        self.url_entry.setStyleSheet(entry_style)
        self.frame_select_insta.hide()

        # info state label
        self.info_state_lbl = QLabel(self)
        self.info_state_lbl.setText("")
        self.info_state_lbl.setGeometry(0, round(self.frameGeometry().height() / 2) - 200,
                                        self.frameGeometry().width(), 100)
        self.info_state_lbl.setStyleSheet(lbl_state_style)

        # progress label
        self.progress_lbl = QLabel(self)
        self.progress_lbl.setText("")
        self.progress_lbl.setGeometry(0, self.frameGeometry().height() - 200,
                                        self.frameGeometry().width(), 100)
        self.progress_lbl.setStyleSheet(lbl_state_style)
        self.progress_lbl.hide()

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(100, self.geometry().height() - 100,
                                      self.geometry().width() - 200, 50)
        self.progress_bar.hide()

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
                self.info_state_lbl.setText("Downloading the video from : " + url)
                file_name = download_from_instagram(url)
                self.video_path = Path.cwd().parent / "insta_videos" / file_name

                self.start_analyze()
            except requests.exceptions.MissingSchema:
                self.info_state_lbl.setText("")
                error_pop_up = QMessageBox(self)
                error_pop_up.setIcon(QMessageBox.Critical)
                error_pop_up.setText('Invalid instagram post url')
                error_pop_up.show()

    def start_analyze(self):
        self.info_state_lbl.setText("Extracting frames from the video,"
                                    "\nplease wait")
        self.frame_main_buttons.hide()
        self.progress_lbl.show()
        self.progress_bar.show()
        self.thread = ExtractFramesThread(self.video_path)
        self.thread.start()
        self.thread.progression.connect(self.update_extraction_progress)
        self.thread.finished.connect(self.finished_getting_frames)

    def finished_getting_frames(self):
        self.analyze_window = AnalyzeVidWindow(self, self.video_path.stem)
        self.hide()

    def update_extraction_progress(self, current, total):
        self.progress_lbl.setText("Extracting frame " + str(current) + " / " + str(total))
        self.progress_bar.setValue(int(current*100/total))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("../resources/JetBrainsMono-Regular.ttf")
    main_window = SelectVidWindow()
    sys.exit(app.exec_())
