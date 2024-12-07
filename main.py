import pandas as pd
from utils import *

registered = get_data('data/registrados.csv')
non_registered = get_data('data/no_registrados.csv')

# TO-DO
# REGISTRADOS:
# - Cuántos han venido antes?
# - De dónde sacan principalmente la info?
# - Días de registro
# ALL:
# - registrados vs no registrados
# - normalizar RUTs
# - estadistica de marcas de bicicleta (quizás modelos también y colores)
# - Graficar hora de llegada, identificando registrados y no registrados
# - Graficar hora de salida, identificando registrados y no registrados
# - Calcular permanencia de cada persona
# - Graficar permanencia según hora de entrada
# - Graficar hora de salida y superponer con gráfico de hora de entrada

registered['RUT'] = registered['RUT'].apply(normalize_rut)
registered['Fecha Registro'] = pd.to_datetime(registered['Marca temporal'], dayfirst=True)
non_registered['RUT'] = non_registered['RUT'].apply(normalize_rut)
people = pd.concat([registered, non_registered], axis=0)
people = people.dropna(subset=['Ingreso', 'Salida'])
people['Ingreso'] = people['Ingreso'].str.replace('.',':')
people['Salida'] = people['Salida'].str.replace('.',':')
people['Ingreso_dt'] = people['Ingreso'].apply(lambda x: parse_time(x))
people['Salida_dt'] = people['Salida'].apply(lambda x: parse_time(x))
people['Estadia_horas'] = (people['Salida_dt'] - people['Ingreso_dt']).dt.total_seconds() / 3600

# Tiempos de estadia
estadia = pd.to_timedelta(people['Estadia_horas'], unit='h')
stats = estadia.describe()
print(stats)

# print(people)
pie_chart(registered, '¿Has alojado en nuestro Bici-Refugio en años anteriores?', save=True, savename='reincidencia')
pie_chart(registered, '¿Como te enteraste del Bici-Refugio?', save=True, savename='fuente')
bar_chart(registered, 'Fecha Registro', True, save=True, savename='fechas_registro')

inout_chart(people, 'Ingreso_dt', save=True, savename='ingreso')
inout_chart(people, 'Salida_dt', True, save=True, savename='salida')
inoutfull_chart(people, ['Ingreso_dt', 'Salida_dt'], True, save=True, savename='ingreso_salida')