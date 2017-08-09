import time
import pandas as pd
import pymysql
import os
from sqlalchemy import create_engine
from selenium import webdriver
from datetime import datetime

x = datetime.now()
x = str(x.day)+str(x.year)

d = webdriver.Chrome(executable_path='C:\\ProgramData\\Anaconda3\\selenium\\webdriver\\chromedriver.exe')
url = 'www.cetip.com.br/tituloscri'

d.get('https://www.cetip.com.br/tituloscri')
time.sleep(10)

d.find_element_by_name('ctl00$MainContent$btEnviar').click()
time.sleep(10)

d.find_element_by_name('ctl00$MainContent$btExportarCSV').click()
time.sleep(10)

d.close()

os.rename("C:\\Users\\vinicius\\Downloads\\Características de CRI.csv", "C:\\Users\\vinicius\\Downloads\\data.csv")

data = pd.read_csv('C:\\Users\\vinicius\\Downloads\\data.csv', decimal=",",sep=";",thousands=".",
                   skiprows=[0], names=['codigo', 'emissor', 'af', 'emissao', 'serie',
                    'qtde_emitida', 'volume', 'dt_emissao', 'dt_vencimento',
                    'dt_distribuição', 'indexador', 'taxa_float', 'spread', 'base_cal',
                    'amortiza', 'isin'], encoding='latin-1')

os.remove("C:\\Users\\vinicius\\Downloads\\data.csv")

engine = create_engine('mysql+pymysql://root:isec@3320@localhost/cetip')
data.to_sql(con=engine, name='emissoes{0}'.format(x),if_exists='append', index=False)
