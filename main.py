import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import os
import time

AllLinksFound = 0
counter = 0

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi(self.get_path("UIFiles\\welcomePage.ui"), self)
        self.proceed.clicked.connect(self.goToLogin)

    def goToLogin(self):
        runbot = runBot()
        widget.addWidget(runbot)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def get_path(self, filepath):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filepath)
    

class runBot(QDialog):
    def __init__(self):
        super(runBot, self).__init__()
        loadUi(self.get_path("UIFiles\\runbot.ui"), self)
        self.editArea.setReadOnly(True)
        # self.findfirstlink()
        self.p = None
        self.startButton.clicked.connect(self.findfirstlink)

    def killBot(self):
        
        app.closeAllWindows()
    def get_path(self, filepath):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filepath)

    def findfirstlink(self):
        self.startButton.hide()
        if self.p is None:  # No process running.
            self.message("\n Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            self.p.start("python", [self.get_path('scripts\\whatbot.py')])

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        # Extract progress if it is in the data.
        # progress = simple_percent_parser(stderr)
        # if progress:
        #     self.progress.setValue(progress)
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Task Completed',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        if state_name == 'Running':
            self.message(f"\n State changed to: {state_name}, Please be patient")
        else:
            self.message(f"\n State changed to: {state_name}")

    def process_finished(self):
        self.message("\n Process finished.")
        self.p = None


    def message(self, s):
        self.editArea.appendPlainText(s)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    # widget.setWindowIcon(QIcon(self.get_path('resources/icon/icon.png')))
    widget.addWidget(welcome)
    widget.setFixedHeight(605)
    widget.setFixedWidth(1024)

    title = "Gee Bot"
    widget.setWindowTitle(title)

    # widget.setWindowFlag(Qt.FramelessWindowHint)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")