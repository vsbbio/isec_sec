import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_IF():
    html = urlopen("https://www.cetip.com.br/tituloscri")
    bsObj = BeautifulSoup(html,"lxml")
    if_bs = bsObj.find_all("select", attrs={"class":"select-padrao", "id":"ctl00_MainContent_ddlCodigoIF"})
    
    for i in if_bs:
        if_table = i.get_text()
        
    if_table = if_table.split("\n\t")
    if_table.remove(if_table[0])
    if_table.remove(if_table[0])
    
    return if_table