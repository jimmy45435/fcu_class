from bs4 import BeautifulSoup
def data(resp,username,password,code):
    resp_soup = BeautifulSoup(resp,'lxml')
    data = {
        "__EVENTTARGET": "ctl00$Login1$LoginButton",
        "__EVENTARGUMENT": resp_soup.find(id = '__EVENTARGUMENT')['value'],
        "__LASTFOCUS": resp_soup.find(id = '__LASTFOCUS')['value'],
        "__VIEWSTATE": resp_soup.find(id = '__VIEWSTATE')['value'],
        "__VIEWSTATEGENERATOR": resp_soup.find(id = '__VIEWSTATEGENERATOR')['value'],
        "__VIEWSTATEENCRYPTED": resp_soup.find(id = '__VIEWSTATEENCRYPTED')['value'],
        "__EVENTVALIDATION": resp_soup.find(id = '__EVENTVALIDATION')['value'],
        "ctl00$Login1$RadioButtonList1": "zh-tw",
        "ctl00$Login1$UserName": username,
        "ctl00$Login1$Password": password,
        "ctl00$Login1$vcode": code,
        "ctl00$temp": "",
    }
    return data