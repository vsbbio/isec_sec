import pandas as pd
import os

while True:
    
    try:
        myDate = input("Qual data de Referência? (DD/MM/AAAA) ")
        myDateI = list(map(int, myDate.split("/")))
    
        if len(myDate) == 10 and myDateI[0] in range(1,32) and myDateI[1] in range(1,13) and myDateI[2] in range(2010, 2100):  
    
            pathFILE = os.getcwd()
            nameFILE = os.listdir(pathFILE)
            data = pd.DataFrame()
            for i in nameFILE:
                dataTemp = pd.read_excel(pathFILE + "\\"+ i, \
                converters={"VALOR_CONTA":int})
    
                frames = [dataTemp, data]
                data = pd.concat(frames)
    
            data.insert(4, "DATA_REFERENCIA", myDate)
            data["VALOR_CONTA"] = data["VALOR_CONTA"].astype(int)
    
            data.to_csv(pathFILE+"\\ITS_CVM.csv", sep=";", 
            index=False, doublequote=False, decimal=",")
            print("Arquivo txt gerado!")
        
        else:
            print("Formato da data está errado!")
            continue
    
    except ValueError:
        print("Formato da data está errado!")
        continue