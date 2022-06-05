# Script que scrapea la web PTE para obtener los documentos y links del apartado 'PLANES Y POLÍTICAS' de la pestaña 'Planeamiento y Organización'

import requests
import time
import pandas as pd
import re

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
FILE_OUTPUT = 'PLANES_POLITICAS_{}.xlsx'.format(d1)
#
# ----------------- MODIFICABLE

BBDD = pd.DataFrame()

entidades = ['133','10006','10130','10058','12193','10428']
for entidad in entidades:
    urls = []
    links = []
    web1 = "https://www.transparencia.gob.pe/enlaces/pte_transparencia_enlaces.aspx?id_entidad="
    web2 = "&id_tema=5"
    URL = web1+entidad+web2
    reqs = requests.get(URL)
    content = reqs.text
    soup = BeautifulSoup(content, 'html.parser')
    nameInstSucio = soup.find_all("h2", {"class": "esp-title-00"})
    nameInst = nameInstSucio[0].get_text()
    for h in soup.findAll('li'):
        a = h.find('a')
        try:
            if 'onmouseover' in a.attrs:
                titulo1 = a.get('onmouseover')
                if ('Instrumentos de Gestión' in titulo1) or ('Planes y Políticas' in titulo1):
                    titulo1 = titulo1[22:]
                    listaTitulo1 = titulo1.split("</b>")
                    titulo1 = listaTitulo1[0]
                    urls.append(titulo1)
                    links.append('')
            if ('Auditoría' in a.get_text()) or ('Información Adicional' in a.get_text()) or ('AUDITORÍA' in a.get_text()) or ('INFORMACIÓN ADICIONAL' in a.get_text()):
                titulo2 = a.get_text()
                titulo2 = re.sub(' +',' ',titulo2)
                urls.append(titulo2)
                links.append('')
            if 'href' in a.attrs:
                url = a.get('href')
                if 'Javascript: pte_js_enviar_Link' in url:
                    listaURL = url.split(",'")
                    url = listaURL[1]
                    url = url.replace("'", "")
                    url_link = listaURL[2]
                    url_link = url_link.replace("'", "")
                    urls.append(url)
                    links.append(url_link)
        except:
            pass
    df1 = pd.DataFrame(list(zip(urls, links)),columns =['Instrumento', 'Link'])
    df1['Tipo_de_Instrumento'] = None
    df1.loc[df1['Instrumento'] == 'Instrumentos de Gestión', 'Tipo_de_Instrumento'] = df1['Instrumento']
    df1.loc[df1['Instrumento'] == 'Planes y Políticas', 'Tipo_de_Instrumento'] = df1['Instrumento']
    df1.loc[df1['Instrumento'] == 'Recomendaciones de Auditoría', 'Tipo_de_Instrumento'] = df1['Instrumento']
    df1.loc[df1['Instrumento'] == 'RECOMENDACIONES DE AUDITORÍA', 'Tipo_de_Instrumento'] = df1['Instrumento']
    df1.loc[df1['Instrumento'] == 'Información Adicional', 'Tipo_de_Instrumento'] = df1['Instrumento']
    df1.loc[df1['Instrumento'] == 'INFORMACIÓN ADICIONAL', 'Tipo_de_Instrumento'] = df1['Instrumento']
    df1['Tipo_de_Instrumento'] = df1['Tipo_de_Instrumento'].mask(df1['Tipo_de_Instrumento'].eq('')).ffill()
    df1 = df1[df1['Tipo_de_Instrumento'] == 'Planes y Políticas']
    df1 = df1[df1['Tipo_de_Instrumento'] != df1['Instrumento']]
    df1['Institución'] = nameInst
    BBDD = BBDD.append(df1)
    BBDD = BBDD[["Institución", "Tipo_de_Instrumento", "Instrumento", "Link"]]
BBDD.to_excel('{}{}'.format(PATH_OUTPUT,FILE_OUTPUT),index=False,sheet_name='BD')

end = time.time()
print('Elapsed time:',end-start)