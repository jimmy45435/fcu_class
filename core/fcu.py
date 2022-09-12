from settings import CLASSCODE
from utils.log import logger
from core.login import Login
from bs4 import BeautifulSoup
import sys
import threading
class FCU_toolkit(Login):
    def __init__(self):
        super().__init__()
        self.login()  #登入 
        self.response.url = f"{'/'.join(self.response.url.split('/')[:3])}/{BeautifulSoup(self.response.text,'lxml').find(id = 'aspnetForm')['action']}"
        
    #加選課程
    def ADD_class(self,classcode):
        soup = BeautifulSoup(self.response.text,'lxml')
        try:
            soup_list = soup.find(id = 'ctl00_MainContent_TabContainer1_tabSelected_gvWishList').find_all('tr')
            for c in soup_list[1::2]:
                if c.find('td',{'class':'gvAddWithdrawCellOne'}).string == classcode:
                    classname =  c.find('input')['name']
                    break
            if classname == '':
                self.add_focus_class(classcode)
                logger.warning(f"{classcode}課程未關注")
                return 'FOCUS'
        except:
            self.add_focus_class(classcode)
            logger.warning(f"{classcode}課程未關注")
            return 'FOCUS'
            
        
        data = {
            "__EVENTTARGET" : classname,
            "__VIEWSTATE" : soup.find(id = '__VIEWSTATE')['value'],
            "__VIEWSTATEGENERATOR" : soup.find(id = '__VIEWSTATEGENERATOR')['value'],
            "__EVENTVALIDATION" : soup.find(id = '__EVENTVALIDATION')['value'],
            "__VIEWSTATEENCRYPTED": ''
        }

        self.response = self.request.post(self.response.url,data=data)
        soup = BeautifulSoup(self.response.text,'lxml')
        msg2 = soup.find('span', id='ctl00_MainContent_TabContainer1_tabSelected_lblMsgBlock').getText()
        
        if msg2[0:4] == '加選成功':
            logger.info(f'{msg2}({classcode})')
            return True
        elif msg2[0:6] == '系統偵測異常':
            logger.warning(f'{msg2[0:6]}({classcode})')
            return 'ERROR'
        else:
            logger.info(msg2)
        return False
    #搜尋課程
    def search_class(self,classcode):
        soup = BeautifulSoup(self.response.text,'lxml')
        data = {
            '__VIEWSTATE': soup.find(id = '__VIEWSTATE')['value'],
            '__VIEWSTATEGENERATOR': soup.find(id = '__VIEWSTATEGENERATOR')['value'],
            '__VIEWSTATEENCRYPTED': '',
            '__EVENTVALIDATION': soup.find(id = '__EVENTVALIDATION')['value'],
            'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbSubID': classcode,

            "__EVENTTARGET": "ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$btnSearchOther",
            "ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDegree": "1",
            "ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$cbOtherCondition1": "on"
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

        }
        self.response = self.request.post(self.response.url,data=data)
        logger.info(f"{classcode}課程已關注")

def for_in_add_class(f,code):
    while len(CLASSCODE) > 0:
        k = f.ADD_class(code)
        if k is True:
            CLASSCODE.remove(code)
            break
        elif k is False:
            continue
        elif k == 'ERROR':
            break
        elif k == 'FOCUS':
            continue

def start():
    try:
        while len(CLASSCODE) > 0:
            f = FCU_toolkit()
            task = []
            for code in CLASSCODE:
                # for i in range(3):
                task.append(threading.Thread(target=for_in_add_class,args=(f,code,),name=f'{code}'))
            for i in range(len(task)):
                task[i].start()
            for i in range(len(task)):
                task[i].join()
            
        # while len(CLASSCODE) > 0:
        #     f = FCU_toolkit()
        #     for i in range(15):
        #         for code in CLASSCODE: 
        #             if f.ADD_class(code):
        #                 CLASSCODE.remove(code)
        #             if len(CLASSCODE)==0:
        #                 sys.exit()

    except:
        start()

    
    
