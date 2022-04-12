import os
import random
import shlex
import sys

from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    app_version = 0.1

    def __init__(self):
        super(MainWindow, self).__init__()

        self.character_movie = QMovie("senko-the-helpful-fox-senko-san.gif")

        self.setup_ui()
        self.setup_events()
        self.show()

    def setup_ui(self):
        loadUi(os.path.join("MainWindow.ui"), self)
        self.setFixedSize(self.size())

        window_title = "Animate my Draws - seigneurfuo - v{0}".format(self.app_version)
        self.setWindowTitle(window_title)

        # Senko Gif
        self.character.setMovie(self.character_movie)
        self.character_movie.start()

    def setup_events(self):
        self.pushButton_2.clicked.connect(self.run_ffmpeg)
        self.character.mousePressEvent = self.character_mouse_press_event

    def character_mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            # paused = True if self.character_movie.state() == 2 else False
            # self.character_movie.setPaused(paused)

            self.character_movie.setSpeed(random.randint(100, 2000))

        elif event.button() == Qt.RightButton:
            self.character_movie.setSpeed(100)

    def run_ffmpeg(self):
        cmd = ["ffplay"]
        if self.checkBox.isChecked():
            loop_nb = str(self.spinBox_2.value())
            cmd += ["-loop", loop_nb]

        folderpath = self.lineEdit.text()
        frames_folder = shlex.quote(os.path.join(folderpath, self.lineEdit_2.text()))
        fps = str(self.spinBox.value())

        cmd += ["-framerate", fps, "-i", frames_folder]
        cmd_string = " ".join(cmd)

        print(cmd_string)
        os.system(cmd_string)


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
