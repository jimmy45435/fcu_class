from settings import *
from utils import http
from core.login.getcode import getcode
from core.login.data import data
from utils.log import logger


class Login():
    def __init__(self,request):
        self.request = request
        self.headers = http.get_requests_headers()

    def get(self):    #get取得該網站資訊
        url = 'https://course.fcu.edu.tw/Login.aspx'
        resp = self.request.get(url,headers = self.headers)
        if resp.status_code != 200:
            return
        return resp.text
    def code(self):  #GET驗證碼圖片
        url = 'https://course.fcu.edu.tw/validateCode.aspx'
        resp = self.request.get(url,headers = self.headers)
        if resp.status_code != 200:
            return
        with open('validateCode.png','wb') as f:
            f.write(resp.content)
        return getcode()    #將圖片轉成文字

    def login(self,data):
        url = 'https://course.fcu.edu.tw/Login.aspx'
        resp = self.request.post(url,data=data,headers = self.headers)
        if resp.status_code != 200:
            logger.warning('登入失敗')
            return
        logger.info('登入成功')
        return resp.text,resp.url

    def start(self):
        return self.login(data(self.get(),USERNAME,PASSWORD,self.code()))



        
        

