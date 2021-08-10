import sys
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QLabel, QLineEdit, QMessageBox

from analyze_vid import AnalyzeVidWindow
from get_frames_from_vid import get_frames
from download_vid import download_from_instagram

import requests


class SelectVidWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(720, 480)

        self.video_path = Path()

        # Select local video button
        self.local_vid_btn = QPushButton(self)
        self.local_vid_btn.setText("Analyze local video")
        self.local_vid_btn.setGeometry(150, round(self.frameGeometry().height()/2), 150, 40)
        self.local_vid_btn.clicked.connect(self.select_local_vid)

        # Select instagram video button
        self.insta_vid_btn = QPushButton(self)
        self.insta_vid_btn.setText("Analyze instagram video")
        self.insta_vid_btn.setGeometry(self.frameGeometry().width() - 300,
                                       round(self.frameGeometry().height()/2), 150, 40)
        self.insta_vid_btn.clicked.connect(self.select_insta_vid)

        # info label
        self.insta_label = QLabel(self)
        self.insta_label.setText("Enter the instagram post URL")
        self.insta_label.setGeometry(round(self.frameGeometry().width()/2) - 100,
                                     round(self.frameGeometry().height() / 2) - 40,
                                     200, 40)
        self.insta_label.hide()

        # Download button
        self.download_btn = QPushButton(self)
        self.download_btn.setText("Ok")
        self.download_btn.setGeometry(200,
                                    round(self.frameGeometry().height()/2) + 40, 100, 40)
        self.download_btn.clicked.connect(self.download_vid)
        self.download_btn.hide()

        # Return button
        self.return_btn = QPushButton(self)
        self.return_btn.setText("return")
        self.return_btn.setGeometry(self.frameGeometry().width() - 200,
                                    round(self.frameGeometry().height()/2) + 40, 100, 40)
        self.return_btn.clicked.connect(self.return_home_page)
        self.return_btn.hide()

        # url entry
        self.url_entry = QLineEdit(self)
        self.url_entry.setGeometry(210, round(self.frameGeometry().height()/2), 300, 40)
        self.url_entry.hide()

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
        self.insta_label.show()
        self.url_entry.show()
        self.return_btn.show()
        self.download_btn.show()

        self.local_vid_btn.hide()
        self.insta_vid_btn.hide()

    def return_home_page(self):
        self.insta_label.hide()
        self.url_entry.hide()
        self.download_btn.hide()
        self.return_btn.hide()

        self.local_vid_btn.show()
        self.insta_vid_btn.show()

    def download_vid(self):
        url = self.url_entry.text()
        if url:
            try:
                file_name = download_from_instagram(url)
                self.video_path = Path.cwd() / "insta_videos" / file_name
                self.start_analyze()
            except requests.exceptions.MissingSchema:
                error_pop_up = QMessageBox(self)
                error_pop_up.setIcon(QMessageBox.Critical)
                error_pop_up.setText('Invalid instagram post url')
                error_pop_up.show()

    def start_analyze(self):
        get_frames(self.video_path)
        AnalyzeVidWindow(self, self.video_path.stem)
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SelectVidWindow()
    sys.exit(app.exec_())
