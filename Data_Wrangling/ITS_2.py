import pandas as pd
import os

pathFILE = os.getcwd()
valid = {"sim": True, "s": True, "si": True,
             "n": False, "nao": False, "não": False}

while True:

    if os.path.isfile(pathFILE+"\\ITS_CVM.csv") == True:
        ans = input("Já existe uma planilha gerada, você deseja substituir [s/n]?")
        if valid[ans] == True:
            try:
                os.remove(pathFILE+"\\ITS_CVM.csv")
                continue
            except FileNotFoundError:
                continue
        else:
            print("So, have a nice day!")
            break

    try:

        nameFILE = str(os.listdir(pathFILE))
        myDate = input("Qual data de Referência? (DD/MM/AAAA) ")
        myDateI = list(map(int, myDate.split("/")))

        if len(myDate) == 10 and myDateI[0] in range(1,32) and myDateI[1] in range(1,13) and myDateI[2] in range(2010, 2100):
            data = pd.DataFrame()
            sheet = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
            try:
                dataTemp = pd.read_excel(pathFILE + "\\"+ nameFILE, converters={"VALOR_CONTA":int},sheetname=sheet)
                frames = [dataTemp, data]
                data = pd.concat(frames)

            except:
                print(i)

            data.insert(4, "DATA_REFERENCIA", myDate)
            data["VALOR_CONTA"] = data["VALOR_CONTA"].astype(int)

            data.to_csv(pathFILE+"\\ITS_CVM.csv", sep=";",
            index=False, doublequote=False, decimal=",", mode="a")
            print("Arquivo txt gerado!")
            break

        else:
            print("Formato da data está errado!")
            continue
