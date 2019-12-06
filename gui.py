import controller
import sys
import os
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView

login_window = uic.loadUiType("login.ui")[0]
board_window = uic.loadUiType("board2.ui")[0]
loginsuccess_msgbox = uic.loadUiType("loginSuccess.ui")[0]
loginfail_msgbox = uic.loadUiType("loginFail.ui")[0]
writeboard_window = uic.loadUiType("writeboard.ui")[0]
showboard_window = uic.loadUiType("showBoard.ui")[0]

global user_id
global nickname
global loc

class login(QDialog, login_window):
    def __init__(self, parent=None):
        super().__init__()
        self.id = "None"
        self.pw = "None"
        self.setupUi(self)
        self.show()
        #self.confirm.setCheckable(True)
        #self.pwLabel.setEchoMode(QLineEdit.Password)
        self.confirm.clicked.connect(self.confirmClicked)

    def confirmClicked(self):
        self.id = self.idLabel.text()
        self.pw = self.pwLabel.text()
        self.idLabel.clear()
        self.pwLabel.clear()

        self.result = controller.search(self.id, self.pw)

        if self.result['result'] == "success":
            self.loginSuccess = loginSuccessWindow()
            self.loginSuccess.label.setText("환영합니다. " + self.id + "님")
            self.loginSuccess.show()
            self.loginSuccess.exec_()

            global user_id
            global nickname
            user_id = self.result['user_id']
            nickname = self.result['nickname']
            loginWindow.hide()

            self.mainWindow = MainDisplay()

        else:
            self.loginFail = loginFailWindow()
            self.loginFail.label.setText("로그인 실패!")
            self.loginFail.show()
            self.loginFail.exec_()

class MainDisplay(QMainWindow, QObject, board_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showlist.clicked.connect(self.showClicked)
        self.write.clicked.connect(self.writeClicked)
        self.refresh.clicked.connect(self.refreshClicked)
        self.signals = controller.Signals()
        self.signals.map_refreshed.connect(self.load)

        #이 부분에 처음 html화면 띄우는 init 코드가 와야함
        global loc
        loc= {"latitude" : 0.0, "longitude" : 0.0}
        self.getLocThread = threading.Thread(target=controller.getLocation, args=(loc, self.signals))
        self.getLocThread.start()
        self.show()

    @pyqtSlot()
    def load(self):
        print("dfsf")
        self.map.load(QUrl.fromLocalFile(
            os.path.split(os.path.abspath(__file__))[0] + r'\map.html'
        ))
        self.map.show()
    def showClicked(self):
        self.showBoardWindow = showBoard()
    def writeClicked(self):
        self.writeBoardWindow = WriteBoard()
    def refreshClicked(self):
        global loc
        self.getLocThread = threading.Thread(target=controller.getLocation, args=(loc, self.signals))
        self.getLocThread.start()


class WriteBoard(QWidget, writeboard_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.locInfoCheckBox.stateChanged.connect(self.checkBoxClicked)
        self.submitButton.clicked.connect(self.submitButtonClicked)
        self.show()

    def submitButtonClicked(self):
        global user_id, nickname, loc
        
        #문제 해결 필요
        enrollthread = threading.Thread(target=controller.enrollBoard, args=(user_id, self.titleTextLabel.text(), self.contentTextLabel.toPlainText(), self.categoryComboBox.currentText(), loc['longitude'], loc['latitude'],))
        enrollthread.start()
        self.hide()

    def checkBoxClicked(self):
        if self.locInfoCheckBox.isChecked():
            self.submitButton.setEnabled(True)
        else:
            self.submitButton.setEnabled(False)

class showBoard(QWidget, showboard_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.show()

    def searchButtonClicked(self):
        global loc
        self.content = self.searchTextLabel.text()
        self.category = self.categoryComboBox.currentText()
        self.distance = self.distanceComboBox.currentText()
        self.boundary = self.boundaryComboBox.currentText()

        self.searchTextLabel.clear()

        # self.searchThread = threading.Thread(target=controller.searchBoard, args=(self.content, self.category, self.distance, self.boundary, loc['latitude'], loc['longitude']))
        # self.searchThread.start()

class loginFailWindow(QDialog, loginfail_msgbox):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.confirm.clicked.connect(self.hide)
        print("fail messagebox open")

class loginSuccessWindow(QDialog, loginsuccess_msgbox):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.confirm.clicked.connect(self.hide)
        print("success messagebox open")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginWindow = login()
    app.exec_()
