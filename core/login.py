from email import header
from wsgiref import headers
from utils.log import logger
from utils.http import get_requests_headers
import requests
from settings import USERNAME,PASSWORD
from bs4 import BeautifulSoup

class Login():
    
    def __init__(self):
        self.initurl = 'https://course.fcu.edu.tw/Login.aspx'
        self.request = requests.Session()
        self.request.headers = get_requests_headers()
        self.response = self.request.get(self.initurl)
        self.username,self.password = USERNAME,PASSWORD

    def save_validateCode(self):
        code_url = 'https://course.fcu.edu.tw/validateCode.aspx'
        resp = self.request.get(code_url,timeout = 5)
        with open('validateCode.png','wb') as f:
            f.write(resp.content)

    def getdata(self):
        resp_soup = BeautifulSoup(self.response.text,'lxml')
        data={
            "__EVENTTARGET": "ctl00$Login1$LoginButton",
            "__EVENTARGUMENT": resp_soup.find(id = '__EVENTARGUMENT')['value'],
            "__LASTFOCUS": resp_soup.find(id = '__LASTFOCUS')['value'],
            "__VIEWSTATE": resp_soup.find(id = '__VIEWSTATE')['value'],
            "__VIEWSTATEGENERATOR": resp_soup.find(id = '__VIEWSTATEGENERATOR')['value'],
            "__VIEWSTATEENCRYPTED": resp_soup.find(id = '__VIEWSTATEENCRYPTED')['value'],
            "__EVENTVALIDATION": resp_soup.find(id = '__EVENTVALIDATION')['value'],
            "ctl00$Login1$RadioButtonList1": "zh-tw",
            "ctl00$Login1$UserName": self.username,
            "ctl00$Login1$Password": self.password,
            "ctl00$Login1$vcode": getcode(),
            "ctl00$temp": "",
        }
        return data
    
    def login(self):
        self.save_validateCode()
        self.response = self.request.post("https://course.fcu.edu.tw/Login.aspx",data=self.getdata())
        if self.response.url == self.initurl:
            logger.info('登入失敗')
            self.response = self.request.get(self.initurl)
            self.login()
        logger.info('登入成功')


from PIL import Image
def getcode():
    m=[
        [1,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0,1,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1],
        [1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,1],
        [1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
        [1,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,0,0,1,0,1,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1],
        [1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,1,0,1,1,1,0,0,1,1,0,1,1,1,0,1,1,0,0,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1],
        [1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1],
        [1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,1,1,0,0,0,1,0,0,1,1,0,0,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1],
        [1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1],
        [1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,1,1,0,0,1,0,0,1,1,1,0,0,1,0,0,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,1,0,0,0,1,1,0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1],
    ]
    im  = Image.open("validateCode.png").convert('RGBA')
    pix = im.load()
    
    v = []
    for i in range(4):
        image_p = []
        for y in range(5,17):
            for x in range(6+9*i,14+9*i):
                for rgba in range(0,4):
                    image_p.append(pix[x,y][rgba])
        r = 0
        t = 255
        n = []
        for j in range(0,len(image_p),4):
            n.append(image_p[j+0] + image_p[j+2]>350)
        for j in range(0,len(m)):
            d = m[j]
            s = 0
            for k in range(len(d)):
                s+=n[k]^d[k]
            if s<t:
                t = s
                r = j
        v.append(str(r))
    return ''.join(v)



        
        

