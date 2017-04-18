import os
import pandas as pd
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from time import sleep
from bs4 import BeautifulSoup

#Definindo parâmetros do sistema
pathFILE = os.getcwd()

def getGen():
    limit = 0
    while limit <= 10:
        try:
            html = urlopen("http://indiceseconomicos.secovi.com.br/indicadormensal.php?idindicador=60")
            bso = BeautifulSoup(html, "lxml")

            month1 = bso.find_all("td", {"class":"borderLeft "})
            month2 = bso.find_all("td", {"class":"borderLeft borderBottom "})
            bowl = bso.find_all("td")

            lst_b = []
    
            for item in bowl:
                lstt = item.get_text()
                lst_b.append(lstt)

            lst_m1 = []
            for item in month1:
                lstt = item.get_text()
                lst_m1.append(lstt)

            lst_m2 = []
            for item in month2:
                lstt = item.get_text()
                lst_m2.append(lstt)
    
            index_t = []
            y = 1995
            j = 0
            month = {"JAN":"01","FEV":"02","MAR":"03","ABR":"04","MAI":"05","JUN":"06","JUL":"07","AGO":"08","SET":"09","OUT":"10","NOV":"11","DEZ":"12",} 
    
            for item in lst_b:
                if item in lst_m1:
                    indext = [str(y) + "." + month[item], str(lst_b[j+1]).replace(" ","").replace("\n","")]
                    index_t.append(indext)
                elif item in lst_m2:
                    indext = [str(y) + "." + str(month[item]), str(lst_b[j+1]).replace(" ","").replace("\n", "")]
                    index_t.append(indext)
                    y += 1
                else:
                    pass
                j += 1

            return index_t
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
        
        
df_new = pd.DataFrame(getGen(), columns=["Data", "NI"])

if os.path.isfile("INPC.csv") == False:
    df_new.to_csv(pathFILE+"\\INPC.csv", sep=";",index=False, doublequote=False, decimal=",")
    print("\nGerado arquivo completo com sucesso!")

else:
    df_old = pd.read_csv("INPC.csv", sep=";", decimal=",")
    delta = len(df_new)-len(df_old)
    if  delta > 0:
        lst_temp = [[""]*2, [""]*2]
        df_temp = pd.DataFrame(lst_temp*delta, columns=["Data", "NI"])
        df_old = df_old.append(df_temp,ignore_index=True)
        df_old.update(df_new)
        df_old.to_csv(pathFILE+"\\INPC.csv", sep=";",index=False, doublequote=False, decimal=",")
        print("Arquivo atualizado e salvo com sucesso! %r nova(s) taxa(s)!" %(delta))
    else:
        print("Não há novas taxas!")