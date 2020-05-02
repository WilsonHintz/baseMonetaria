import csv
import json

import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto3
from datetime import datetime
import os

def importBase(fecha):
    #fecha = 2020-04-30
    payload = {
        'fecha_desde': '2000-01-01',
        'fecha_hasta': fecha,
        'B1': 'Enviar',
        'primeravez': '1',
        'serie': '250',
        'serie1': '0',
        'serie2': '0',
        'serie3': '0',
        'serie4': '0'}

    url = "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables_datos.asp"

    req = requests.get(url, params=payload)

    html = req.content
    soup = BeautifulSoup(html, features="html.parser")
    table = soup.find("table", "table table-BCRA table-bordered table-hover table-responsive")

    output_rows = []
    output_rows.append(["fecha", "Base_Monetaria_Total"])

    for table_row in table.find_all_next('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.string.strip())
        output_rows.append(output_row)

    with open('middle.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)

    # CSV para grafico
    df = pd.read_csv('middle.csv', parse_dates=['fecha'], dayfirst=True, usecols=('fecha', 'Base_Monetaria_Total'))
    df = df.replace('\.', '', regex=True).astype(str)
    df['fecha'] = pd.to_datetime(df.fecha)
    # Manipulacion de fecha
    df = df.replace('\/', '-', regex=True).astype(str)
    df = df.replace('\-', ',', regex=True).astype(str)
    df.to_csv('static/output.csv', header=False, index=False, sep=";")

    # CSV para tabla (Deprecated)
    df = pd.read_csv('middle.csv', parse_dates=['fecha'], usecols=('fecha', 'Base_Monetaria_Total'))
    df = df.replace('\.', '', regex=True).astype(str)
    df['fecha'] = pd.to_datetime(df.fecha)
    df.to_csv('static/tablaDatos.csv', index=False)

    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d-%m-%Y, %H:%M:%S")
    S3_BUCKET = os.environ.get('S3_BUCKET')
    s3_client = boto3.client('s3')

    object_name_tabla_bkp = 'imports/tablaDatos' + dt_string + '.csv'
    object_name_output = 'static/output.csv'
    file_name_tabla = 'static/tablaDatos.csv'
    file_name_output = 'static/output.csv'

    response = s3_client.upload_file(file_name_tabla, 'basemon', object_name_tabla_bkp)
    response = s3_client.upload_file(file_name_output, 'basemon', object_name_output)

    presigned_post = s3_client.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=file_name_output,
        Fields={"acl": "public-read", "Content-Type": 'csv'},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": 'csv'}
        ],
        ExpiresIn=3600
    )

    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name_output)
    })

def getCsv():
    s3_client = boto3.resource('s3')
    file_name = 'static/tablaDatos.csv'
    object_name = 'static/tablaDatos.csv'
    response = s3_client.meta.client.download_file('basemon', object_name, file_name)
    print(response)
    return response


