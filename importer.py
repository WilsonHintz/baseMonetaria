import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto3

payload = {
'fecha_desde':'2000-01-01',
'fecha_hasta':'2020-04-30',
'B1':'Enviar',
'primeravez':'1',
'serie':'250',
'serie1':'0',
'serie2':'0',
'serie3':'0',
'serie4':'0' }

url = "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables_datos.asp"

req = requests.get(url, params=payload)

html = req.content
soup = BeautifulSoup(html, features="html.parser")
table = soup.find("table", "table table-BCRA table-bordered table-hover table-responsive")

output_rows = []
output_rows.append(["fecha","Base_Monetaria_Total"])

for table_row in table.find_all_next('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.string.strip())
    output_rows.append(output_row)

with open('middle.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)

#CSV para grafico
df = pd.read_csv('middle.csv', parse_dates=['fecha'], dayfirst=True, usecols=('fecha', 'Base_Monetaria_Total'))
df = df.replace('\.', '', regex=True).astype(str)
df['fecha'] = pd.to_datetime(df.fecha)
#Manipulacion de fecha
df = df.replace('\/', '-', regex=True).astype(str)
df = df.replace('\-', ',', regex=True).astype(str)
df.to_csv('static/output.csv', header=False, index=False, sep=";")

#CSV para tabla
df = pd.read_csv('middle.csv', parse_dates=['fecha'], usecols=('fecha', 'Base_Monetaria_Total'))
df = df.replace('\.', '', regex=True).astype(str)
df['fecha'] = pd.to_datetime(df.fecha)
df.to_csv('static/tablaDatos.csv',index=False)

s3_client = boto3.client('s3')
object_name = 'static/tablaDatos.csv'
file_name = 'static/tablaDatos.csv'
response = s3_client.upload_file(file_name, 'basemon', object_name)
print(response)


