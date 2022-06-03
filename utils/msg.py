from bs4 import BeautifulSoup
def msg(resp):
    soup = BeautifulSoup(resp.text,'html.parser')
    msg = str(soup.find('span' ,{'class' : compile(r'msg ([A-B])\w+')}).getText())
    print(msg)