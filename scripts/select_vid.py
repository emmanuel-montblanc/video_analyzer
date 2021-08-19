"""
Main script of the project, allows you to select the video you want to analyze (either from your
local disk or from instagram), and then to download and extracts the frames from it, before opening
another window to analyze it.
"""

import sys
from pathlib import Path

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QFrame,
    QProgressBar,
)

import style_sheets
from analyze_vid import AnalyzeVidWindow
from download_vid import DownloadInstaVideoThread
from get_frames_from_vid import ExtractFramesThread


class SelectVidWindow(QMainWindow):
    """
    Main window, to select the video you want to analyze and prepare it for the analysis (download
    and extract the frames)3
    """

    def __init__(self):
        super().__init__()
        self.resize(720, 480)
        self.setWindowTitle("Video analyzer")
        self.setWindowIcon(QIcon("../resources/diamond_twist.png"))
        self.setStyleSheet(style_sheets.wndw_style)

        self.analyze_window = QMainWindow()
        self.extracting_thread = QThread()
        self.downloading_thread = QThread()

        self.video_path = Path()

        # Frame for the 2 main buttons
        self.frame_main_buttons = QFrame(self)
        self.frame_main_buttons.setGeometry(
            0, 0, self.geometry().width(), self.geometry().height()
        )

        # Select local video button
        self.local_vid_btn = QPushButton(self.frame_main_buttons)
        self.local_vid_btn.setText("Analyze local\n video")
        self.local_vid_btn.setGeometry(
            150, round(self.frameGeometry().height() / 2), 150, 50
        )
        self.local_vid_btn.clicked.connect(self.select_local_vid)
        self.local_vid_btn.setStyleSheet(style_sheets.btn_style)

        # Select instagram video button
        self.insta_vid_btn = QPushButton(self.frame_main_buttons)
        self.insta_vid_btn.setText("Analyze instagram\n video")
        self.insta_vid_btn.setGeometry(
            self.frameGeometry().width() - 300,
            round(self.frameGeometry().height() / 2),
            150,
            50,
        )
        self.insta_vid_btn.clicked.connect(self.select_insta_vid)
        self.insta_vid_btn.setStyleSheet(style_sheets.btn_style)

        # Frame for selecting insta video
        self.frame_select_insta = QFrame(self)
        self.frame_select_insta.setGeometry(
            0, 0, self.geometry().width(), self.geometry().height()
        )

        # enter url label
        self.insta_lbl = QLabel(self.frame_select_insta)
        self.insta_lbl.setText("Enter the instagram post URL")
        self.insta_lbl.setGeometry(
            round(self.frameGeometry().width() / 2) - 100,
            round(self.frameGeometry().height() / 2) - 40,
            200,
            40,
        )
        self.insta_lbl.setStyleSheet(style_sheets.lbl_style)

        # Download button
        self.download_btn = QPushButton(self.frame_select_insta)
        self.download_btn.setText("Ok")
        self.download_btn.setGeometry(
            185, round(self.frameGeometry().height() / 2) + 45, 150, 40
        )
        self.download_btn.clicked.connect(self.download_vid)
        self.download_btn.setStyleSheet(style_sheets.btn_style)

        # Return button
        self.return_btn = QPushButton(self.frame_select_insta)
        self.return_btn.setText("Return")
        self.return_btn.setGeometry(
            385, round(self.frameGeometry().height() / 2) + 45, 150, 40
        )
        self.return_btn.clicked.connect(self.return_home_page)
        self.return_btn.setStyleSheet(style_sheets.btn_style)

        # url entry
        self.url_entry = QLineEdit(self.frame_select_insta)
        self.url_entry.setGeometry(
            185, round(self.frameGeometry().height() / 2), 350, 40
        )
        self.url_entry.setStyleSheet(style_sheets.entry_style)
        self.frame_select_insta.hide()

        # info state label
        self.info_state_lbl = QLabel(self)
        self.info_state_lbl.setText("")
        self.info_state_lbl.setGeometry(
            0,
            round(self.frameGeometry().height() / 2) - 200,
            self.frameGeometry().width(),
            100,
        )
        self.info_state_lbl.setStyleSheet(style_sheets.lbl_state_style)

        # progress label
        self.progress_lbl = QLabel(self)
        self.progress_lbl.setText("")
        self.progress_lbl.setGeometry(
            0, self.frameGeometry().height() - 200, self.frameGeometry().width(), 100
        )
        self.progress_lbl.setStyleSheet(style_sheets.lbl_state_style)
        self.progress_lbl.hide()

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(
            100, self.geometry().height() - 100, self.geometry().width() - 200, 50
        )
        self.progress_bar.setStyleSheet(style_sheets.progress_bar_style)
        self.progress_bar.hide()

        self.show()

    def select_local_vid(self):
        """
        Method called when clicking on the "Analyze local vid" button,
        open a dialog for you to select the local video you want to analyze,
        then if you chose a video, extracts the frames from it and start the analysis window
        """

        dialog_result = QFileDialog.getOpenFileName(
            self, "Select video", "c:\\", "Video files (*.mp4 *.vid *.raw)"
        )
        video_path = Path(dialog_result[0])

        if video_path != Path("."):
            self.video_path = video_path
            self.start_analyze()

    def select_insta_vid(self):
        """
        Method called when clicking on the "Analyze insta vid" button,
        hide the main frame ("Analyze insta vid" and "Analyze local vid" buttons),
        and show the select_insta frame (url entry, url label, "ok" button and "Return" button)
        """

        self.frame_select_insta.show()
        self.frame_main_buttons.hide()

    def return_home_page(self):
        """
        Method called when clicking on the "Return" button,
        show the main frame ("Analyze insta vid" and "Analyze local vid" buttons),
        and hide the select_insta frame (url entry, url label, "ok" button and "return" button)
        """

        self.frame_select_insta.hide()
        self.frame_main_buttons.show()

    def download_vid(self):
        """
        Method called when clicking on the "Ok" button,
        if a url was entered, hide the select_insta frame, displays info_state and progress labels,
        then start the downloading thread and connects the different signals to the corresponding
        methods
        """

        url = self.url_entry.text()
        if url:
            self.frame_select_insta.hide()
            self.info_state_lbl.setText("Downloading the video from : \n" + url)
            self.progress_lbl.setText("Requesting the url")
            self.progress_lbl.show()

            self.downloading_thread = DownloadInstaVideoThread(url)
            self.downloading_thread.start()
            self.downloading_thread.finished_request.connect(
                lambda: self.progress_lbl.setText("Getting the url of the video")
            )
            self.downloading_thread.found_url.connect(
                lambda: self.progress_lbl.setText("Now downloading the video")
            )
            self.downloading_thread.error.connect(self._url_error)
            self.downloading_thread.finished.connect(self._finished_downloading)

    def _url_error(self, err):
        """
        Method called if a error signal was emitted by the downloading thread,
        creates a pop up displaying the error
        """

        self.info_state_lbl.setText("")
        self.progress_lbl.hide()
        self.frame_select_insta.show()

        error_pop_up = QMessageBox(self)
        error_pop_up.setIcon(QMessageBox.Critical)
        error_pop_up.setStyleSheet(style_sheets.qmsg_box_style)
        if err == "url":
            error_pop_up.setText("Invalid instagram post url")
        if err == "timeout":
            error_pop_up.setText("Timeout, couldn't get a response for this url")
        if err == "connection":
            error_pop_up.setText(
                "Can't establish a connection to the requested url,"
                "\ncheck your connection"
            )
        error_pop_up.show()

    def _finished_downloading(self, file_name):
        """
        Method called when a "finished" signal is emitted by the downloading thread,
        get the path of the video based on the file_name received, and start extracting the frames
        :param file_name: name of the video
        """

        self.video_path = Path.cwd().parent / "insta_videos" / file_name
        self.start_analyze()

    def start_analyze(self):
        """
        Method called either after selecting a local path, or after finished downloading a
        instagram video,
        hide the main frame, displays info_state_lbl, progress_lbl and the progress_bar
        Start the extracting frame thread and link its different signal to the corresponding methods
        """

        self.info_state_lbl.setText("Extracting frames from the video," "\nplease wait")
        self.frame_main_buttons.hide()
        self.progress_lbl.show()
        self.progress_bar.show()

        self.extracting_thread = ExtractFramesThread(self.video_path)
        self.extracting_thread.start()
        self.extracting_thread.progression.connect(self.update_extraction_progress)
        self.extracting_thread.finished.connect(self.finished_getting_frames)

    def update_extraction_progress(self, current, total):
        """
        Method called when the extracting thread emits a "progression" signal,
        updates the progress_lbl and the progress bar
        :param current: the number of frame we have extracted
        :param total: the total nb of frame we have to extract
        """

        self.progress_lbl.setText(
            "Extracting frame " + str(current) + " / " + str(total)
        )
        self.progress_bar.setValue(int(current * 100 / total))

    def finished_getting_frames(self):
        """
        Method called when the extracting thread emits a "finished" signal,
        hide the progress widgets, and show the main button frames (in case we want to go back to
        this window later to change video)
        Then start the analysis window and hide the select_vid window
        """

        self.info_state_lbl.setText("")
        self.progress_lbl.hide()
        self.progress_bar.hide()
        self.frame_main_buttons.show()
        self.analyze_window = AnalyzeVidWindow(self, self.video_path.stem)
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("../resources/JetBrainsMono-Regular.ttf")
    main_window = SelectVidWindow()
    sys.exit(app.exec_())
