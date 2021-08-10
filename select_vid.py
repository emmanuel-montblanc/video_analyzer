import sys
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog

from analyze_vid import AnalyzeVidWindow
from get_frames_from_vid import get_frames


class SelectVidWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(720, 480)

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
        self.insta_vid_btn.clicked.connect(self.select_local_vid)

        self.show()

    def select_local_vid(self):
        dialog_result = QFileDialog.getOpenFileName(self, 'Select video',
                                                    'c:\\', "Video files (*.mp4 *.vid *.raw)")
        video_path = Path(dialog_result[0])
        print(video_path)

        if video_path != Path("."):
            get_frames(video_path)
            analyze_window = AnalyzeVidWindow(self, video_path.stem)
            self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SelectVidWindow()
    sys.exit(app.exec_())
