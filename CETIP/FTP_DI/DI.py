import pandas as pd
import os
import sys
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from time import localtime, strftime, sleep

#Definindo parâmetros do sistema
pathFILE = os.getcwd()
snowflake = strftime("%d %b %Y", localtime())

#Função Genérica
def regFunc(func):
    return func

#Função geTxt.py - Detalhamento acessar #1 da pasta
def gettxt():
    limit = 0
    while limit <= 10:
        try:
            html = urlopen("ftp://ftp.cetip.com.br/MediaCDI")
            txt_bs = BeautifulSoup(html,"lxml")
            for txt in txt_bs:
                txt_str = txt.get_text()
            txt_lst = txt_str.split("\n")
            txt_lst.reverse()
            txt_lst.remove(txt_lst[0])
            txt_out = []
            for file in txt_lst:
                txt_out.append(file[-13:-1])
                if txt_lst.index(file) == 0:
                    sys.stdout.write('\n')
                    sys.stdout.write('\r')
                    sys.stdout.write("Getting Names [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*20/len(txt_lst)), 5*int((txt_lst.index(file)+1)*20/len(txt_lst))))
                else:
                    sys.stdout.write('\r')
                    sys.stdout.write("Getting Names [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*20/len(txt_lst)), 5*int((txt_lst.index(file)+1)*20/len(txt_lst))))
            return txt_out
        except HTTPError:
            print("\nHTTPError, tentaremos de novo! %r \n %s" %(limit, regFunc(gettxt)))
            sleep(10)
            limit += 1
            continue
        except URLError:
            print("\nURLError, tentaremos de novo! %r \n %s" %(limit, regFunc(gettxt)))
            sleep(10)
            limit += 1
            continue

#Função getValues.py - Detalhamento acessar #2 da pasta
def getvalue(txt_lst):
    limit = 0
    di_lst = []
    for file in txt_lst:
        while limit <= 10:
            try:
                html = urlopen("ftp://ftp.cetip.com.br/MediaCDI/"+file)
                di_bs = BeautifulSoup(html,"lxml")
                di = di_bs.get_text()
                di = di[:9]
                di_lst_temp = [file, file[:-4],int(di)/100]
                di_lst.append(di_lst_temp)
                if txt_lst.index(file) == 0:
                    sys.stdout.write('\n')
                    sys.stdout.write('\r')
                    sys.stdout.write("Getting Values [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*20/len(txt_lst)), 5*int((txt_lst.index(file)+1)*20/len(txt_lst))))
                else:
                    sys.stdout.write('\r')
                    sys.stdout.write("Getting Values [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*20/len(txt_lst)), 5*int((txt_lst.index(file)+1)*20/len(txt_lst))))
                break
            except HTTPError:
                print("\nHTTPError, tentaremos de novo! %r \n %s" %(limit, regFunc(getvalue)))
                sleep(10)
                limit += 1
                continue
            except URLError:
                print("\nURLError, tentaremos de novo! %r \n %s" %(limit, regFunc(getvalue)))
                sleep(10)
                limit += 1
                continue
    return di_lst

#Dando opção de escolha ao usuário
willp = int(input("Escolha uma opção:\n1.Gerar arquivo completo; \n2. Adicionar DI em planilha já existente. "))

#Escolha 1
if willp == 1:
    print("Você escolheu gerar o arquivo completo!")
    
    #Função getAll.py - Detalhamento acessar #3 da pasta
    def getall_di():
        limit = 0
        while limit <= 2:
            try:
                txt_lst = gettxt()
                di_lst = getvalue(txt_lst)
                di_df = pd.DataFrame(di_lst, columns=["Arquivo", "Data", "Taxa x 100"])
                di_df.to_csv(pathFILE+"\\DI"+snowflake+".csv", sep=";",index=False, doublequote=False, decimal=",", mode="a")
                print("\nArquivo salvo em %s, por favor verificar a correta alocação!" %(pathFILE))
                break
            except HTTPError:
                print("\nHTTPError, tentaremos de novo! %r \n %s" %(limit, regFunc(getall_di)))
                sleep(10)
                limit += 1
                continue
            except URLError:
                print("\nURLError, tentaremos de novo! %r \n %s" %(limit, regFunc(getall_di)))
                sleep(10)
                limit += 1
                continue
    getall_di()
    
#Escolha 2
elif willp == 2:
    print("Você escolheu adicionar novas taxas!")
    
    #Função append_DI.py - Detalhamento acessar #4 da pasta
    def append_di():
        limit = 0
        while limit <= 2:
            try:
                if os.path.isfile("DI.csv") == False:
                    print("\nArquivo DI.txt não encontrado na pasta executada!")
                    break
                else:
                    txt_lst = gettxt()
                    txt_df = pd.DataFrame(txt_lst, columns=["Arquivo"])
                    di_csv = pd.read_csv("DI.csv", header=0, sep=";")
                    di_df = pd.DataFrame(di_csv)
                    new_lst = []
                for file in txt_df:
                    if file in di_df["Arquivo"]:
                        new_temp = [file]
                        new_lst.append = [new_temp]
                        if txt_lst.index(file) == 0:
                            sys.stdout.write('\n')
                            sys.stdout.write('\r')
                            sys.stdout.write("Adding Values [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*40/len(txt_lst)), 2.5*int((txt_lst.index(file)+1)*40/len(txt_lst))))
                        else:
                            sys.stdout.write('\r')
                            sys.stdout.write("Adding Values [%-20s] %d%%" % ('='*int((txt_lst.index(file)+1)*40/len(txt_lst)), 2.5*int((txt_lst.index(file)+1)*40/len(txt_lst))))
                    else:
                        continue
                if len(new_lst) == 0:
                    print("\nNão há novas taxas!")
                    break
                else:
                    di_lst = getvalue(new_lst)
                    di_df.append(di_lst, ignore_index=True)
                    print("\n %r taxas adicionas" %(len(new_lst)))
                    break
            except HTTPError:
                print("\n HTTPError, tentaremos de novo! %r \n %s" %(limit, regFunc(append_di)))
                sleep(10)
                limit += 1
                continue
            except URLError:
                print("\nURLError, tentaremos de novo! %r \n %s" %(limit, regFunc(append_di)))
                sleep(10)
                limit += 1
                continue
    append_di()
    
#Escolha Inválida
else:
    print("Opção inválida!")