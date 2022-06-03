from this import d
from core.login import Login
from bs4 import BeautifulSoup
from utils.msg import msg

class FCU_toolkit(Login):
    def __init__(self):
        super().__init__()
        self.login()  #登入 
        self.response.url = f"{'/'.join(self.response.url.split('/')[:3])}/{BeautifulSoup(self.response.text,'lxml').find(id = 'aspnetForm')['action']}"
    #加選課程
    def ADD_class(self,classcode):
        soup = BeautifulSoup(self.response.text,'lxml')
        data = {
            "__EVENTTARGET" : classcode,
            "__VIEWSTATE" : soup.find(id = '__VIEWSTATE')['value'],
            "__VIEWSTATEGENERATOR" : soup.find(id = '__VIEWSTATEGENERATOR')['value'],
            "__EVENTVALIDATION" : soup.find(id = '__EVENTVALIDATION')['value']
        }
        self.response = self.request.post(self.response.url,data=data)
    #搜尋課程
    def search_class(self,classcode):
        soup = BeautifulSoup(self.response.text,'lxml')
        data = {
            '__VIEWSTATE': soup.find(id = '__VIEWSTATE')['value'],
            '__VIEWSTATEGENERATOR': soup.find(id = '__VIEWSTATEGENERATOR')['value'],
            '__VIEWSTATEENCRYPTED': '',
            '__EVENTVALIDATION': soup.find(id = '__EVENTVALIDATION')['value'],
            'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbSubID': classcode,
        }
        self.response = self.request.post(self.response.url,data=data)
    #新增關注課程
    def add_focus_class(self,classcode):
        '''
        新增關注課程
        '''
        self.search_class(classcode)
        soup = BeautifulSoup(self.response.text,'lxml')
        data = {
            "__VIEWSTATE": soup.find(id = '__VIEWSTATE')['value'],
            "__VIEWSTATEGENERATOR": soup.find(id = '__VIEWSTATEGENERATOR')['value'],
            "__EVENTVALIDATION": soup.find(id = '__EVENTVALIDATION')['value'],
            '__VIEWSTATEENCRYPTED': '',
            "ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbSubID": classcode,
            "ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$gvSearchResult$ctl02$btnAdd": "關注",
            "ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDegree": "1"

        }
        self.response = self.request.post(self.response.url,data=data)
def start():
    FCU_toolkit().add_focus_class('3089')
    
    
