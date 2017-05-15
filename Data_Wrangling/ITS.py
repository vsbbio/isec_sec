import pandas as pd
import os

pathFILE = os.getcwd()
valid = {"sim": True, "s": True, "si": True,
             "n": False, "nao": False, "não": False}
data = pd.DataFrame()
nameFILE = os.listdir(pathFILE)
myDate = input("Qual data de Referência? (DD/MM/AAAA) ")
myDateI = list(map(int, myDate.split("/")))

if len(myDate) == 10 and myDateI[0] in range(1,32) and myDateI[1] in range(1,13) and myDateI[2] in range(2010, 2100):

    for i in nameFILE:

        j = 0

        if i.endswith(".xlsx"):

            while j < 50:

                try:
                    dataTemp = pd.read_excel(pathFILE + "\\"+ i, converters={"VALOR_CONTA":int, "EMISSAO":str, "SERIE":str}, sheetname = j)
                    frames = [dataTemp, data]
                    data = pd.concat(frames)
                    j += 1

                except:
                    print("Planilha {0} e sheet {1}".format(i, j))
                    j = 50
        else:
            pass

    data.insert(4, "DATA_REFERENCIA", myDate)
    data.to_csv(pathFILE+"\\ITS_CVM.csv", sep=";", index=False, doublequote=False, decimal=",", mode="a")

    print("Arquivo txt gerado!")

else:
    print("Formato da data está errado!")
