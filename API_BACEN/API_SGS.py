import os
import pandas as pd

#Dicionário com o código dos índices no sistema do Banco Central

ind     =   {"IGPM":[189,"30/06/1989","FGV","M","PER"],"IGPDI":[190,"30/06/1989","FGV","M","PER"], "INPC":[188,"30/04/1979","IBGE","M","PER"],
            "INCC":[192,"29/02/1944","FGV","M","PER"],"TR":[226,"01/02/1991","BC","D","PER"],
            "IPCA":[433,"02/01/1980","IBGE","M","PER"],"INCCM":[7456,"30/09/1994","FGV","M","PER"]}

source  =    {"FGV":["IGPM","IGPDI","INCC","INCCM"],"IBGE":["INPC", "IPCA"],"BC":["TR"]}

per     =    {"D":["TR"],"M":["IGPM","IGPDI","INCC","INCCM","INPC","IPCA"], "Y":[]}

typex   =    {"PER":["IGPM","IGPDI","INCC","INCCM","INPC","IPCA","TR"],"NI":[]}


API_SGS = "http://api.bcb.gov.br/dados/serie/bcdata.sgs." + indices[index] + "/dados?formato=csv&dataInicial=" + dt_ini + "&dataFinal=" + dt_end
