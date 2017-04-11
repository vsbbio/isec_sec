import pandas as pd
from os import getcwd
from urllib.request import urlopen
from bs4 import BeautifulSoup

pathFILE = getcwd()
date_lst = []
ni_lst = []
limit = 0

while limit <= 10:
    try:
        html = urlopen("http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=33593&module=M")
        bsObj = BeautifulSoup(html,"lxml")
        ipca = bsObj.find_all("td", {"class":"dxgv"})
        break
        
    except HTTPError:
            print("\nHTTPError, tentaremos de novo! %r \n %s" %(limit))
            sleep(10)
            limit += 1
            continue
        
    except URLError:
            print("\nURLError, tentaremos de novo! %r \n %s" %(limit))
            sleep(10)
            limit += 1
            continue

for file in ipca:
    if ipca.index(file)%2 == 0:
        if_temp = file.get_text()
        date_lst.append(if_temp)
    else:
        else_temp = file.get_text()
        ni_lst.append(else_temp)
    
    df = pd.DataFrame(date_lst, columns=["Data"])
    df2 = pd.DataFrame(ni_lst, columns=["Ni"])
    df.insert(1, "NI", df2)
    df.drop(len(df)-1)

df.to_csv(pathFILE+"\\IGPDI.csv", sep=";", index=False, doublequote=False, decimal=",", mode="a")
print("Arquivo gerado com sucesso em %s" %(pathFILE))