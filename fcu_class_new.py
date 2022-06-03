import requests
from PIL import Image
from bs4 import BeautifulSoup
from re import search,compile
from time import sleep,strftime
from json import load

class Login:
    def __init__(self,request,NID,PASSWORD):
        self.nid = NID
        self.password = PASSWORD
        self.code = ''
        self.request = request
        self.login_data = {}
    def take_codeimg(self):
        code_url = 'https://course.fcu.edu.tw/validateCode.aspx'
        resp = self.request.get(code_url,timeout = 5)
        with open('validateCode.png','wb') as f:
            f.write(resp.content)
    def code2text(self):
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
        self.code = ''.join(v)
    def grub_url_data(self):
        url = 'https://course.fcu.edu.tw/Login.aspx'
        resp = self.request.get(url,timeout = 5)
        soup = BeautifulSoup(resp.text,'html.parser')
        self.login_data.update({"__EVENTTARGET": "ctl00$Login1$LoginButton"})
        self.login_data.update({"ctl00$Login1$RadioButtonList1": "zh-tw"})
        self.login_data.update({"__VIEWSTATE" : soup.find(id = '__VIEWSTATE')['value']})
        self.login_data.update({"__EVENTVALIDATION" : soup.find(id = '__EVENTVALIDATION')['value']})
        self.login_data.update({"__VIEWSTATEGENERATOR" : soup.find(id = '__VIEWSTATEGENERATOR')['value']})
        self.login_data.update({"ctl00$Login1$UserName" : self.nid})
        self.login_data.update({"ctl00$Login1$Password" : self.password})
        self.login_data.update({"ctl00$Login1$vcode" : self.code})
        self.login_data.update({"__EVENTARGUMENT": ""})
        self.login_data.update({"__LASTFOCUS": ""})
        self.login_data.update({"__VIEWSTATEENCRYPTED": ""})
        self.login_data.update({"ctl00$temp": ""})
    def login(self):
        url = 'https://course.fcu.edu.tw/Login.aspx'
        resp = self.request.post(url,data = self.login_data,timeout = 5)
        return resp
    def run(self):
        self.take_codeimg()
        self.code2text()
        self.grub_url_data()
        return self.login()

class fcuk_fcu:
    def __init__(self,resp,request,classcode = []):
        self.resp = resp
        self.request = request
        self.data = {}
        self.url = ''
        self.classcode = classcode
    def make_data(self,classid):
        soup = BeautifulSoup(self.resp.text,'html.parser')
        self.data.update({"__EVENTTARGET" : classid})
        self.data.update({"__VIEWSTATE" : soup.find(id = '__VIEWSTATE')['value']})
        self.data.update({"__VIEWSTATEGENERATOR" : soup.find(id = '__VIEWSTATEGENERATOR')['value']})
        self.data.update({"__EVENTVALIDATION" : soup.find(id = '__EVENTVALIDATION')['value']})
    def find_classid(self,code):
        soup = BeautifulSoup(self.resp.text, 'html.parser')
        soup_list = soup.find(id = 'ctl00_MainContent_TabContainer1_tabSelected_gvWishList')
        soup_list = soup_list.find_all('tr')
        for c in soup_list[1::2]:
            if c.find('td',{'class':'gvAddWithdrawCellOne'}).string == code:

                return c.find('input')['name']
    def post_class(self):
        self.resp = self.request.post(self.url,data = self.data,timeout = 5)
    def msg(self):
        soup = BeautifulSoup(self.resp.text,'html.parser')
        msg = str(soup.find('span' ,{'class' : compile(r'msg ([A-B])\w+')}).getText())
        if msg == '加選成功':
            return True
        if msg == '本科目名額目前已額滿 !':
            return False
        else:
            return 'Error'
    def geturl(self):
        soup = BeautifulSoup(self.resp.text, 'html.parser')
        url = soup.find(id = 'aspnetForm')['action']
        
        self.url = self.resp.url[:33] +'/'+ url

    def run(self):
        for code in self.classcode:
            self.make_data(self.find_classid(code))
            self.geturl()
            self.post_class()
            if self.msg() == True:
                
                self.classcode.remove(code)
                return True
            elif self.msg() == 'Error':
                return 'Error'
          
if __name__ == '__main__':
    with open("User.json","r") as f:
        TNPC = load(f)
        token = TNPC['token']
        NID = TNPC['NID']
        PASSWORD = TNPC['PASSWORD']
        class_code = TNPC['classcode']
    while True:
        try:
            no = True
            while no:
                request = requests.Session()
                login = Login(request,NID,PASSWORD)
                resp = login.run()
                
                fcuk_class = fcuk_fcu(resp,request,class_code)
                while no:
                    if fcuk_class.run() == 'Error':
                        break
                    if class_code == []:
                        no = False
        except :
            print('確認網路及帳密輸入正確')
            sleep(3)
        


        




