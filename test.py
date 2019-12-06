'''
import geocoder

g = geocoder.ip('me')

print(g.latlng)
# print(g.city)
'''

'''
import requests
import json

req = requests.get('http://ipinfo.io')
print(req.text)
'''

'''
import googlemaps
import requests
import urllib
import json

key = '&key=AIzaSyDm7BEC3UsYjoFSZEzyNGmURc9yS4WJURU'

# 지명 주소를 위/경도 주소로,
base_url ='https://maps.googleapis.com/maps/api/geocode/json?language=ko'+\
                '&address='
# 부분 주소를 통해서 찾기
address = urllib.parse.quote('강남구 역삼1동 736-36')
addr = json.loads(urllib.request.urlopen(base_url+address+key).read().decode('utf-8'))
# 위치 정보만 뽑기
print(addr)
for i in addr['results']:
    print(i['geometry']['location'])
'''

'''
import googlemaps
import json

gmaps_key = 'AIzaSyDm7BEC3UsYjoFSZEzyNGmURc9yS4WJURU'
gmaps = googlemaps.Client(key=gmaps_key)

g = gmaps.geocode('건국대학교', language='ko')
print(json.dumps(g))
'''

# chromedriver.exe 78버전 + selenium 패키지 필요
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# import time
#
# def getLocation():
#     start = time.time()
#     options = Options()
#     #options.add_argument('headless')
#     options.add_argument("--use--fake-ui-for-media-stream")
#     driver = webdriver.Chrome(executable_path = './chromedriver.exe',options=options) #Edit path of chromedriver accordingly
#     timeout = 20
#     driver.get("https://mycurrentlocation.net/")
#     wait = WebDriverWait(driver, timeout)
#     longitude = driver.find_elements_by_xpath('//*[@id="longitude"]') #Replace with any XPath
#     print(longitude)
#     longitude = [x.text for x in longitude]
#     print(longitude)
#     longitude = str(longitude[0])
#     latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
#     latitude = [x.text for x in latitude]
#     latitude = str(latitude[0])
#     driver.quit()
#     end = time.time()
#     return (latitude,longitude, end - start)
#
# print(getLocation())

# from selenium import webdriver
#
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
# # 혹은 options.add_argument("--disable-gpu")
#
# driver = webdriver.Chrome('chromedriver', options=options)
#
# driver.get('http://naver.com')
# driver.implicitly_wait(3)
# driver.get_screenshot_as_file('naver_main_headless.png')
#
# driver.quit()

def render(url):
    """Fully render HTML, JavaScript and all."""

    import sys
    from PyQt5.QtCore import QEventLoop,QUrl
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebEngineWidgets import QWebEngineView

    class Render(QWebEngineView):
        def __init__(self, url):
            self.html = None
            self.app = QApplication(sys.argv)
            QWebEngineView.__init__(self)
            self.loadFinished.connect(self._loadFinished)
            self.load(QUrl(url))
            self.show()
            self.app.exec_()
            while self.html is None:
                self.app.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)

        def _callable(self, data):
            self.html = data

        def _loadFinished(self, result):
            self.page().toHtml(self._callable)

    return Render(url).html


print(render("http://www.naver.com"))