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
signup_window = uic.loadUiType("signUp.ui")[0]

msgbox = uic.loadUiType("msgbox.ui")[0]
checksignout_window = uic.loadUiType("checkSignOut.ui")[0]

idorpw_window = uic.loadUiType("idorpw.ui")[0]
findidpw_window = uic.loadUiType("findIdPw.ui")[0]

board_window = uic.loadUiType("board.ui")[0]
writeboard_window = uic.loadUiType("writeboard.ui")[0]
showboard_window = uic.loadUiType("showBoard.ui")[0]


# QT Designer에서 Application Modal로 설정하면 해당 창이 종료될 때 까지 다른 창에 접근 불가
# .exec_()의 역할은 창이 꺼질 때까지 뒤의 코드가 실행되지 않기를 바랄 때 사용


global user_id
global nickname
global loc

class LoginWindow(QDialog, login_window):
    def __init__(self, parent=None):
        super().__init__()
        self.id = "None"
        self.pw = "None"
        self.setupUi(self)
        self.show()
        self.confirm.clicked.connect(self.confirmClicked)
        self.signUpCheckbox.clicked.connect(self.signUpClicked)
        self.signOutCheckbox.clicked.connect(self.signOutClicked)
        self.findCheckbox.clicked.connect(self.findClicked)

    def confirmClicked(self):
        self.id = self.idLabel.text()
        self.pw = self.pwLabel.text()
        self.idLabel.clear()
        self.pwLabel.clear()

        self.result = controller.loginSearch(self.id, self.pw)

        if self.result['result'] == "success":
            self.loginSuccess = Msgbox()
            self.loginSuccess.label.setText("환영합니다. " + self.id + "님")
            self.loginSuccess.exec_()

            global user_id
            global nickname
            user_id = self.id
            nickname = self.result
            self.hide()

            self.mainWindow = MainDisplay()

        else:
            self.loginFail = Msgbox()
            self.loginFail.label.setText("로그인 실패")
            self.loginFail.exec_()

    def signUpClicked(self):
        self.signUpCheckbox.setCheckState(False)
        self.signup = SignUpWindow()

    def signOutClicked(self):
        self.signOutCheckbox.setCheckState(False)
        self.id = self.idLabel.text()
        self.pw = self.pwLabel.text()
        self.idLabel.clear()
        self.pwLabel.clear()
        self.result = controller.loginSearch(self.id, self.pw)

        # 탈퇴할 아이디 및 비밀번호 일치 시
        if self.result['result'] == "success":
            global user_id
            user_id = self.id
            self.warning = CheckSignOutWindow()

        # 탈퇴할 이이디 및 비밀번호 잘못 입력 시
        else:
            self.wrongidpw = Msgbox()
            self.wrongidpw.setWindowTitle("Wrong input")
            self.wrongidpw.label.setText("일치하는 로그인 정보가 없습니다")

    def findClicked(self):
        self.findCheckbox.setCheckState(False)
        self.idorpw = IdOrPw()


class IdOrPw(QWidget, idorpw_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.idCheckbox.clicked.connect(self.idClicked)
        self.pwCheckbox.clicked.connect(self.pwClicked)
        self.show()

    def idClicked(self):
        self.hide()
        self.findId = FindIdPw('id')
    def pwClicked(self):
        self.hide()
        self.findPw = FindIdPw('pw')

class FindIdPw(QWidget, findidpw_window):
    def __init__(self, target):
        super().__init__()
        self.setupUi(self)
        self.findButton.clicked.connect(self.findBtnClicked)
        self.target = target

        if target == 'id':
            self.label1.setText("이메일")
            self.label2.setText("닉네임")
        else:
            self.label1.setText("아이디")
            self.label2.setText("전화번호")

        self.show()

    def findBtnClicked(self):
        self.hide()

        if self.target == 'id':
            self.result = controller.findIdSearch(self.lineEdit1.text(), self.lineEdit2.text())

            self.idInfo = Msgbox()
            if self.result['result'] == "success":
                self.idInfo.setWindowTitle("ID Found")
                self.idInfo.label.setText("고객님의 아이디는 " + self.result['data'] + " 입니다")
            else:
                self.idInfo.setWindowTitle("Fail")
                self.idInfo.label.setText("정보와 일치하는 아이디가 없습니다")
        else:
            self.result = controller.findPwSearch(self.lineEdit1.text(), self.lineEdit2.text())

            self.pwInfo = Msgbox()
            if self.result['result'] == "success":
                self.pwInfo.setWindowTitle("PW Found")
                self.pwInfo.label.setText("고객님의 비밀번호는 " + self.result['data'] + " 입니다")

            else:
                self.pwInfo.setWindowTitle("Fail")
                self.pwInfo.label.setText("정보와 일치하는 비밀번호가 없습니다")


class SignUpWindow(QWidget, signup_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 중복검사 체크하는 변수
        self.idChecked = False
        self.nickChecked = False

        self.idCheckButton.clicked.connect(self.idBtnClicked)
        self.nickCheckButton.clicked.connect(self.nickBtnClicked)
        self.signUpButton.clicked.connect(self.signUpBtnClicked)
        self.show()

    def idBtnClicked(self):
        if controller.checkDuplication(self.idLineEdit.text(), 0):
            self.idChecked = True
            if self.idChecked and self.nickChecked:
                self.signUpButton.setEnabled(True)

            self.nodup = Msgbox()
            self.nodup.setWindowTitle("Success")
            self.nodup.label.setText("사용 가능한 ID입니다!")
        else:
            self.idChecked = False
            self.signUpButton.setEnabled(False)

            self.dup = Msgbox()
            self.dup.setWindowTitle("Fail")
            self.dup.label.setText("이미 사용 중인 ID입니다")

    def nickBtnClicked(self):
        if controller.checkDuplication(self.nickLineEdit.text(), 1):
            self.nickChecked = True
            if self.idChecked and self.nickChecked:
                self.signUpButton.setEnabled(True)

            self.nodup = Msgbox()
            self.nodup.setWindowTitle("Success")
            self.nodup.label.setText("사용 가능한 닉네임입니다!")
        else:
            self.nickChecked = False
            self.signUpButton.setEnabled(False)

            self.dup = Msgbox()
            self.dup.setWindowTitle("Fail")
            self.dup.label.setText("이미 사용 중인 닉네임입니다")

    def signUpBtnClicked(self):
        self.result = controller.checkUserInfo(self.idLineEdit.text(), self.pwLineEdit.text(), self.emailLineEdit.text(), self.phoneLineEdit.text())
        self.infoMsgbox = Msgbox()
        if self.result[0] == False:
            self.infoMsgbox.setWindowTitle("Fail")
            if self.result[1] == -1:
                self.infoMsgbox.label.setText("아이디가 너무 길거나 짧습니다")
            elif self.result[1] == -2:
                self.infoMsgbox.label.setText("비밀번호가 너무 길거나 짧습니다")
            elif self.result[1] == -3:
                self.infoMsgbox.label.setText("비밀번호는 영문과 숫자를 혼용해 주세요")
            elif self.result[1] == -4:
                self.infoMsgbox.label.setText("잘못된 이메일 형식")
            elif self.result[1] == -5:
                self.infoMsgbox.label.setText("잘못된 전화번호 길이")
            else:
                self.infoMsgbox.label.setText("잘못된 전화번호 형식")

        else:
            self.infoMsgbox.setWindowTitle("Success")
            self.infoMsgbox.label.setText("회원가입 성공")
            controller.signUp(self.idLineEdit.text(), self.pwLineEdit.text(), self.nickLineEdit.text(), self.nameLineEdit.text(), self.emailLineEdit.text(), self.phoneLineEdit.text())

            self.hide()

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


    #폴더 내 html파일을 webEngineView에 등록하고 show
    @pyqtSlot()
    def load(self):
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

class Msgbox(QDialog, msgbox):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.confirm.clicked.connect(self.hide)
        self.show()

class CheckSignOutWindow(QWidget, checksignout_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.confirm.clicked.connect(self.confirmClicked)
        self.cancel.clicked.connect(self.cancelClicked)
        self.show()

    def confirmClicked(self):
        self.hide()

        global user_id
        controller.signOut(user_id)

        self.confirmSignOut = Msgbox()
        self.confirmSignOut.setWindowTitle("Good Bye")
        self.confirmSignOut.label.setText("정상적으로 탈퇴 되었습니다")

    def cancelClicked(self):
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    app.exec_()
