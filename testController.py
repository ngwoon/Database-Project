import sys
import pymysql
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *
import onlyLogin

conn = pymysql.connect(host='localhost', user='supervisor', password='1234', db='db_teamproject')
curs = conn.cursor()

def searchIdPw():
    sql = "select * from user"
    curs.execute(sql)
    rows = curs.fetchall()
    print(id, pw)

    for row in rows:
        if row[0] == id and row[1] == pw:
            loginSuccess = onlyLogin.loginSuccessWindow()
            loginSuccess.exec_()
            return

    loginFail = onlyLogin.loginFailWindow()
    loginFail.exec_()
    return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginWindow = onlyLogin.login()
    loginWindow.getIdPw.connect(searchIdPw)
    loginWindow.show()
    app.exec_()

