import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot

login_window = uic.loadUiType("login.ui")[0]
loginsuccess_msgbox = uic.loadUiType("loginSuccess.ui")[0]
loginfail_msgbox = uic.loadUiType("loginFail.ui")[0]

@pyqtSlot()
def login_success():
    successWindow = loginSuccessWindow()
    successWindow.exec_()

@pyqtSlot()
def login_fail():
    failWindow = loginFailWindow()
    failWindow.exec_()

class login(QDialog, login_window):
    def __init__(self, parent=None):
        super().__init__()
        self.success = pyqtSignal()
        self.fail = pyqtSignal()
        self.getIdPw = pyqtSignal()

        self.success.connect(login_success())
        self.fail.connect(login_fail())

        self.id = "None"
        self.pw = "None"
        self.setupUi(self)
        self.confirm.setCheckable(True)
        # self.pwLabel.setEchoMode(QLineEdit.Password)
        self.confirm.clicked.connect(self.confirmClicked)
        self.show()

    def alertMsgbox(self, result):
        if result == "success":
            self.success.emit()
        else:
            self.fail.emit()

    def corret_idpw(self):
        self.success.emit()

    def incorret_idpw(self):
        self.fail.emit()

    def confirmClicked(self):
        self.id = self.idLabel.text()
        self.pw = self.pwLabel.text()
        self.idLabel.clear()
        self.pwLabel.clear()
        self.getIdPw.emit()

class loginFailWindow(QDialog, loginfail_msgbox):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.confirm.clicked.connect(self.close)
        print("fail messagebox open")


class loginSuccessWindow(QDialog, loginsuccess_msgbox):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.confirm.clicked.connect(self.close)
        print("success messagebox open")