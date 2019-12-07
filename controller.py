import pymysql
import folium
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread, QUrl
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#비밀번호 문자열 검사 시 사용. 정규표현식
import re

conn = pymysql.connect(host='localhost', user='supervisor', password='1234', db='db_teamproject')
curs = conn.cursor()

class Signals(QObject):
    map_refreshed = pyqtSignal()

#쿼리를 DB에 날려 원하는 투플만 뽑아오는 것이 모든 투플을 뽑아 파이썬에서 탐색하는 것 보다 성능이 훨씬 좋다. (log(n) 과 n 타임 차이)
def search(id, pw):
    sql = "select * from user where user_id=%s and password=%s"
    curs.execute(sql, (id, pw))
    user_rows = curs.fetchone()

    if user_rows == None:
        return {"result" : "fail", "user_id" : "", "nickname" : ""}
    else:
        sql = "select user_id, nickname from userinfo where user_id = %s"
        curs.execute(sql, (user_rows[0]))
        userinfo_rows = curs.fetchone()

        return {"result" : "success", "user_id" : userinfo_rows[0], "nickname" : userinfo_rows[1]}


#flag는 id 검사인지, nickname 검사인지를 구별하기 위해 사용됨
#flag == 0이면 id검사, 1이면 nickname 검사
def checkDuplication(userstr, flag):

    if flag == 0:
        sql = "select * from user where user_id=%s"
        curs.execute(sql, (userstr))
        userinfo_rows = curs.fetchone()

    else:
        sql = "select * from userinfo where nickname=%s"
        curs.execute(sql, (userstr))
        userinfo_rows = curs.fetchone()

    if userinfo_rows == None:
        return True
    else:
        return False

#id, password, email, phone_number 유효한 형태인지 확인
# -1 : id 길이 오류
# -2 : pw 길이 오류
# -3 : pw 조합 오류
# -4 : email 형식 오류
# -5 : 전화번호 길이 오류
# -6 : 전화번호 형식 오류
def checkUserInfo(id, password, email, phone_number):
    #id확인
    if len(id) > 15 or len(id) == 0:
        return (False, -1)

    #password길이 확인
    if len(password) > 16 or len(password) == 0:
        return (False, -2)

    #password문자 + 숫자 조합인지 확인
    if not re.search(r'\d', password) or not re.search(r'\D', password):
        return (False, -3)

    #이메일 형식 확인
    if '@' not in email:
        return (False, -4)

    #전화번호 길이 확인
    if len(phone_number) != 11:
        return (False, -5)

    #전화번호 형식 확인
    if not re.search(r'\d', phone_number):
        return (False, -6)

    return (True, 0)

def signUp(user_id, password, nickname, name, email, phone_number):
    sql = "insert into user(user_id, password)" \
          "values(%s, %s)"

    curs.execute(sql, (user_id, password))

    sql = "insert into userinfo(user_id, nickname, name, email)" \
          "values(%s, %s, %s, %s)"

    curs.execute(sql, (user_id, nickname, name, email))

    sql = "insert into phonenumber(user_id, phone_number)" \
          "values(%s, %s)"

    curs.execute(sql, (user_id, phone_number))

    conn.commit()


def getLocation(loc, signals):

    options = Options()
    # options.add_argument("start-maximized")
    # options.add_argument("--disable-infobars")
    # options.add_argument("--disable-extensions")
    # options.add_argument('--headless')

    options.add_argument("--use--fake-ui-for-media-stream")
    options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)  # Edit path of chromedriver accordingly
    timeout = 20
    driver.get("https://mycurrentlocation.net/")

    wait = WebDriverWait(driver, timeout)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #parsed[0] = latitude, parsed[1] = longitude
    parsed = soup.find_all('td')

    driver.quit()

    map_osm = folium.Map(location=[parsed[0].text, parsed[1].text], zoom_start=17)
    folium.Marker([parsed[0].text, parsed[1].text]).add_to(map_osm)
    map_osm.save("./map.html")

    signals.map_refreshed.emit()

def enrollBoard(user_id, title, contents, category, longitude, latitude):
    sql = "insert `db_teamproject`.`board`(`user_id`, `title`, `category`, `contents`, `recommends`, `longitude`, `latitude`)" \
          "values(%s, %s, %s, %s, %s, %s, %s)"

    try:
        curs.execute(sql, (user_id, title, category, contents, 0, longitude, latitude))
        conn.commit()

    except Exception as ex:
        print("에러 발생", ex)


#검색 순서
#distance를 통해 게시글 투플들을 우선 뽑아냄
#category, boundary를 통해 추려진 게시글을 한 번더 추려냄

def searchBoard(content, category, distance, boundary, latitude, longitude):
    
    #distance와 category를 사용해 투플 뽑아냄
    #boundary에 따라 제목, 작성자, 혹은 내용 검색으로 바뀌기 때문에 동적인 검색은 파이썬 코드에서 진행
    sql = "select board_id, title, content, nickname, recommends" \
          "from (select * from board where (SELECT SQRT(POW(latitude - %s, 2) + POW(longitude - %s, 2)) <= %s) and (category = %s)) b, userinfo u" \
          "where u.user_id == b.user_id"

    curs.execute(sql, (latitude, longitude, distance, category))
    boards = curs.fetchall()





