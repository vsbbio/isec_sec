import pandas as pd
import sqlite3 as sq3

from os import getcwd
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from time import sleep

def wsName():
    limit = 0
    while limit <= 10:
        try:
            #Capturando o conteúdo da página
            html = urlopen("ftp://ftp.cetip.com.br/MediaCDI")
            Bso = BeautifulSoup(html,"lxml")

            #Extraindo a listagem com o nome e extensão dos arquivos
            for txt in Bso:
                txt_temp = txt.get_text()

            #Convertendo a string em lista
            txt_temp = txt_temp.split("\r")

            #Removendo valores em branco e Criando listagem em de branco
            try:

                try:
                    txt_temp.remove("")
                    txt_temp.remove("\n")
                except:
                    txt_temp.remove("\n")

            except:
                    txt_temp.remove("")

            finally:
                txt = []

            #Editando os registros para excluir espaços e outros caracteres
            for item in txt_temp:
                txt.append(int(item[-12:-4]))

            #Retornando o resultado à uma variável
            return txt

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

def wsValue(names):

    #Criando uma variável vázia para preenchimento posterior
    data = []

    #Loop para leitura e captura do conteúdo dos arquivos contidos no diretório
    for file in names:
        try:                
            #Capturando o conteúdo de cada arquivo contido no diretório
            html = urlopen("ftp://ftp.cetip.com.br/MediaCDI/"+str(file)+".txt")
            Bso = BeautifulSoup(html,"lxml")
            value = Bso.get_text()
                
            #Editando o conteúdo, excluindo espaços e outros caracteres
            value = float(value[:9])
            data_temp = [int(file), float(value/100)]
            data.append(data_temp)
        except:
            print("Erro link: %s" %(html))
            continue

    #Retornando o resultado do tratamento
    return data

def criar(table_name="CDI"):
    c1 = sq3.connect("INDEX.db")
    c2 = c1.cursor()

    sql_create = "CREATE TABLE IF NOT EXISTS %s(date datetime primary key, VAR INTEGER)" %(table_name)
    c2.execute(sql_create)

    c2.close()
    c1.close()

def inserir(table_name="CDI", data_insert="DATA"):
    c1 = sq3.connect("INDEX.db")
    c2 = c1.cursor()

    sql_insert = "insert into %s VALUES(?, ?)" %(table_name)

    for item in data_insert:
        c2.execute(sql_insert, item)

    c1.commit()
    c2.close()
    c1.close()

def select_date(table_name="CDI", select="*"):
    c1 = sq3.connect("INDEX.db")
    c2 = c1.cursor()
    dates = []

    sql_select = "SELECT %s FROM %s" %(select, table_name)

    c2.execute(sql_select)

    for item in c2.fetchall():
        date_temp = item[0]
        dates.append(date_temp)

    return dates

def export_csv(table_name="CDI", select="*"):
    c1 = sq3.connect("INDEX.db")
    c2 = c1.cursor()
    dates = []

    sql_select = "SELECT %s FROM %s" %(select, table_name)

    c2.execute(sql_select)

    data = c2.fetchall()
    data = pd.DataFrame(data, columns=["Date","VAR"])

    data.to_csv(getcwd()+"\CDI.csv", sep=";",index=False, doublequote=False, decimal=",")


#Criando a tabela do CDI no db
criar(table_name="CDI")

#Selecionando as datas que já estão inseridas no db
date = select_date(table_name="CDI", select="date")

#Coletando todos os nomes dos arquivos disponíveis no diretório FTP da CETIP
names = wsName()

#Criando listagem em de branco
new = []

#Comparando e criando a listagem dos arquivos novos
for item in names:
    if item not in date:
        new_temp = item
        new.append(new_temp)
    else:
        pass

if len(new) > 0:

    #Executando função GetValue e convertendo em Data Frame
    data = wsValue(new)

    #Convertendo a Coluna "Taxa x 100" em numerico
    inserir(data_insert=data,table_name="CDI")
    print("\n %r taxas adicionas" %(len(new)))

else:
    print("\nNão há novas taxas!")

answer = input("Você deseja exportar o arquivo para CSV?")

if answer.upper() == "SIM":
    export_csv(table_name="CDI")
