from datetime import datetime, date, timedelta
#from modules import Homerico
from io import StringIO
import pandas as pd
import numpy as np
import time, json

registros = {
    1444: "BLBP",           # Barras Laminadas/ Barras Perdiades
    1350: "SUCATEAMENTO",   # Sucateamento de Laminado
    1333: "ACIDENTE CPT",   # Acidente CPT
    1336: "PROD LAMINADO",  # Produção da Laminação
    3087: "REND. METALICO"  # Rendimento Metálico do Laminado
}

print('''
            _____  _____   _                 __  __ 
     /\    |  __ \|_   _| | |         /\    |  \/  |
    /  \   | |__) | | |   | |        /  \   | \  / |
   / /\ \  |  ___/  | |   | |       / /\ \  | |\/| |
  / ____ \ | |     _| |_  | |____  / ____ \ | |  | |
 /_/    \_\|_|    |_____| |______|/_/    \_\|_|  |_|
                                                    
                                                    
''')


def trimStartEndDates( month: int, now: datetime ) -> tuple[str, str]:
    if month > now.month: return (None, None)
    day = (
        now.day if month == now.month else
        lastDayOfMonth(date(now.year, month, 1)).day
    )
    sdate = date(now.year, month, 1)
    edate = date(now.year, now.month, day)
    return (sdate, edate)

def lastDayOfMonth(date: datetime): # Get lart day of month
    return date.replace(day=31) if date.month == 12 else date.replace(month=(date.month + 1), day=1) - timedelta(days=1)

def checkTypeNumber(numero: float): # Parse string to int or float
    return int(float(numero)) if float(numero) // 1 == float(numero) else float(numero)

def replaceNaNValues(number): # Replace NaN values in pandas
    return number if str(number) != str(np.nan) else int(str(number).replace(str(np.nan), '0'))

def get_registro(datas, registro):
    x, day, metaD = 0, 0, 0
    final = datas[1].strftime("%d/%m/%Y")
    if datas[1].month == datetime.now().date().month:
        final = datetime.now().date().strftime("%d/%m/%Y")
    df = pd.read_csv(StringIO(RelatorioGerencialRegistro("{}".format(final), str(registro))), sep = ";").filter(['registro','meta','dia','acumulado'])
    try:
        x = checkTypeNumber(df['acumulado'][0])
        day = checkTypeNumber(df['dia'][0])
        metaD = checkTypeNumber(df['meta'][0])
    except ValueError:
        x = checkTypeNumber(df['acumulado'][0].replace(',','.'))
        day = checkTypeNumber(df['dia'][0].replace(',','.'))
        metaD = checkTypeNumber(df['meta'][0].replace(',','.'))
    except:
        pass
    x = x if x > 0 else 0
    return {'total':x, 'dia':day,'meta':metaD}

def get_Plista():
    now = datetime.now()
    final = datetime.now().date().strftime("%d/%m/%Y")
    csv_file = (StringIO(ProducaoLista("{}".format(final),"1269")))
    df = pd.read_csv(csv_file, sep = ";")
    df = df.filter(['data','peso'])
    lista = {}
    for i in range(1, now.day+1):
        df['data'] = df['data'].replace([i],"{0:-02d}/m/y".format(i))  
    df = df.stack().str.replace('m','{0:-02d}'.format(now.month)).unstack()
    df = df.stack().str.replace('y','{}'.format(now.year)).unstack()
    df = df.stack().str.replace(',','.').unstack()
    df['peso'].astype(float)
    df = df.to_dict(orient="records")
    return json.dumps(df)

def pegaIndicadores(registro, nome):
    now = datetime.now()
    tlst = dict[int, tuple[int, int, int]]
    trims: tlst = { 1: (1, 2, 3), 2: (4, 5, 6), 3: (7, 8, 9), 4: (10, 11, 12) }
    trim = trims[1 + ((now.month - 1) // 3)]
    helper = lambda m: (m, lastDayOfMonth(date(now.year, m, 1)))
    metaNow = get_registro(trimStartEndDates(now.month, now), str(registro))
    meta = {str(nome):{
        'acumulado': replaceNaNValues(metaNow['total']),
        'mes1': replaceNaNValues(get_registro(trimStartEndDates(*helper(trim[0])), str(registro))['total']),
        'mes2': replaceNaNValues(get_registro(trimStartEndDates(*helper(trim[1])), str(registro))['total']),
        'mes3': replaceNaNValues(get_registro(trimStartEndDates(*helper(trim[2])), str(registro))['total']),
        'dia':  replaceNaNValues(metaNow['dia']),
        'meta':  replaceNaNValues(metaNow['meta'])
    }}
    return meta