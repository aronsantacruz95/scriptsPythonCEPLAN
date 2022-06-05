import requests
import time
import pandas as pd

from bs4 import BeautifulSoup
from datetime import date

start = time.time()
today = date.today()
d1 = today.strftime("%d_%m_%Y")


# ----------------- MODIFICABLE
#
# ruta de salida
PATH_OUTPUT = 'C:/Users/ARON SANTA CRUZ/Documents/ceplan/bases/'
# nombre del archivo
FILE_OUTPUT = 'ID_ENTIDAD_{}.xlsx'.format(d1)
#
# ----------------- MODIFICABLE

BBDD = pd.DataFrame()
for entidad in range(100, 111):
    print(entidad)
    id_entidad = []
    name_entidad = []
    web1 = "https://www.transparencia.gob.pe/enlaces/pte_transparencia_enlaces.aspx?id_entidad="
    URL = web1+str(entidad)
    try:
        reqs = requests.get(URL)    
        content = reqs.text
        soup = BeautifulSoup(content, 'html.parser')
        nameInstSucio = soup.find_all("h2", {"class": "esp-title-00"})
        nameInst = nameInstSucio[0].get_text()
    except:
        nameInst = 'No existe ID'
        pass
    id_entidad.append(entidad)
    name_entidad.append(nameInst)
    df1 = pd.DataFrame(list(zip(id_entidad,name_entidad)),columns =['id_entidad','name_entidad'])
    BBDD = BBDD.append(df1)
BBDD.to_excel('{}{}'.format(PATH_OUTPUT,FILE_OUTPUT),index=False,sheet_name='BD')

end = time.time()
print('Elapsed time:',end-start)