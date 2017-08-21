#Identificação do Registro
p1 = [0,1]
 
#Identificação da Empresa no Banco 
p2 = [1,17]

#Identificação Título no Banco 
p3 = [17,29]

#Código Para Cálculo do Rateio 30
p4 = [29,30]

#Tipo de Valor Informado 31
p5 = [30,31]

#Filler 43
p6 =[31,43]

#Código do Banco para Crédito do 1º Beneficiário 46
p7 = [43,46]

#Código da Agência para Crédito do 1º Beneficiário 51 
p8 = [46,51]

#Dígito da Agência para Crédito do 1º Beneficiário  52
p9 = [51,52]

#Número da Conta Corrente para Crédito do 1º Beneficiário 64
p10 = [52,64]

#Dígito da Conta Corrente para Crédito do 1º Beneficiário  65
p11 = [64,65]

#Valor, ou Percentual para Rateio 80
p12 = [65, 80]

#Nome do 1º Beneficiário 120
p13 = [80,120]

#Filler 151
p14 = [120,151]

#Parcela 157
p15=[151,157]

#Floating para o 1º Beneficiário 160
p16=[157,160]

#Código do Banco para Credito do 2º Beneficiário  163
p17 = [160,163]

#Código da Agência para Crédito do 2º Beneficiário 168
p18 = [163,168]

#Dígito da Agência para Crédito do 2º Beneficiário 169
p19 = [168,169]

#Número da Conta Corrente para Crédito do 2º Beneficiário 181
p20 = [169,181]

#Dígito da Conta Corrente para Crédito do 2º Beneficiário  182
p21 = [181,182]

#Valor, ou Percentual para Rateio 197
p22 = [182,197]

#Nome do 2º Beneficiário 237
p23 = [197,237]

#Filler 268
p24 = [237,268]

#Parcela 274
p25 = [268,274]

#Floating para o 2º Beneficiário 277
p26 = [274,277]

#Código do Banco para Crédito do 3º Beneficiário 280
p27 = [277,280]

#Código da Agência para Crédito do 3º Beneficiário 285
p28 = [280,285]

#Dígito da Agência para Crédito do 3º Beneficiário 286
p29 = [285,286]

#Número da Conta Corrente para Crédito do 3º Beneficiário  298
p30 = [286,298]

#Dígito da Conta Corrente para Crédito do 3º Beneficiário 299
p31 = [298,299]

#Valor ou Percentual para Rateio 314
p32 = [299,314]

#Nome do 3º Beneficiário 354
p33 = [314,354]

#Filler 385
p34 = [354,385]

#Parcela 391
p35 = [385,391]

#Floating para 3º Beneficiário 394
p36= [391,394]

#Número Seqüencial do Registro 400
p37 = [394,400]


posx = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,
        p12,p13,p14,p15,p16,p17,p18,p19,p20,
        p21,p22,p23,p24,p25,p26,p27,p28,p29,
        p30,p31,p32,p33,p34,p35,p36,p37]

itens = ["Identificação do Registro","Identificação da Empresa no Banco",
         "Identificação Título no Banco", "Código Para Cálculo do Rateio",
         "Tipo de Valor Informado", "Filler", "Código do Banco para Crédito do 1º Beneficiário",
         "Código da Agência para Crédito do 1º Beneficiário", "Dígito da Agência para Crédito do 1º Beneficiário",
         "Número da Conta Corrente para Crédito do 1º Beneficiário", "Dígito da Conta Corrente para Crédito do 1º Beneficiário",
         "Valor, ou Percentual para Rateio", "Nome do 1º Beneficiário", "Filler","Parcela",
         "Floating para o 1º Beneficiário", "Código do Banco para Credito do 2º Beneficiário",
         "Código da Agência para Crédito do 2º Beneficiário", "Dígito da Agência para Crédito do 2º Beneficiário",
         "Número da Conta Corrente para Crédito do 2º Beneficiário", "Dígito da Conta Corrente para Crédito do 2º Beneficiário",
         "Valor, ou Percentual para Rateio", "Nome do 2º Beneficiário", "Filler", "Parcela",
         "Floating para o 2º Beneficiário", "Código do Banco para Crédito do 3º Beneficiário",
         "Código da Agência para Crédito do 3º Beneficiário", "Dígito da Agência para Crédito do 3º Beneficiário",
         "Número da Conta Corrente para Crédito do 3º Beneficiário", "Dígito da Conta Corrente para Crédito do 3º Beneficiário",
         "Valor ou Percentual para Rateio", "Nome do 3º Beneficiário", "Filler", "Parcela",
         "Floating para 3º Beneficiário", "Número Seqüencial do Registro"]

line = str(input("Digite a linha 3 do arquivo:"))

content = []
number = []

for i in posx:
    content.append(line[i[0]:i[1]])
        
for i in posx:
    number.append("(%d caracteres)" %(len(str(line[i[0]:i[1]]))))
    
import pandas as pd

d = {"Count":number,"Fill":content, "Desc": itens}
output = pd.DataFrame(data = d)
