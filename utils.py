from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import mplcursors


COLORS = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

regular = 'static/Urbanist-Regular.ttf'
medium = 'static/Urbanist-Regular.ttf'
title_prop = fm.FontProperties(fname=medium)
graph_prop = fm.FontProperties(fname=regular)


def get_data(src_file, delimiter=','):
    ext = src_file.split('.')[-1]
    if (ext == 'csv'):
        return pd.read_csv(src_file, delimiter=delimiter, low_memory=False)
    elif (ext in ['xlsx', 'xls']):
        return pd.read_excel(src_file)
    else:
        return -1


def normalize_rut(rut):
    rut = rut.strip().replace('.', '')
    rut = rut.upper()
    if ('-' in rut):
        rut = rut.replace('-', '')
    return rut


def get_day(date):
    # obj_date = datetime.strptime(date, '%Y-%m-%d')
    day = date.strftime('%A %d de %b del %Y')
    return day.capitalize()


def parse_time(hour_str):
    reference_date = datetime(2023, 12, 8)
    hour, minute = map(int, hour_str.split(':'))
    dt = datetime.combine(reference_date, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
    if hour > 16:  # Si es mayor a las 16, pertenece al día anterior
        dt -= timedelta(days=1)
    return dt


def pie_chart(df: pd.DataFrame, colname: str, debug=False, save=False, savename=None):
    frec = df[colname].value_counts()
    frec['Otro'] = frec[frec < 5].sum()
    frec = frec[frec >= 5]
    options = frec.index
    values = frec.values

    if (debug):
        print(frec)
    else:
        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=options, autopct='%1.1f%%', startangle=90,
                colors=COLORS)

        plt.title(colname, fontproperties=graph_prop, fontsize=15)
        plt.tight_layout()

        if (save):
            if (savename):
                plt.savefig(f'images/{savename}.jpg', dpi=300, bbox_inches='tight')
            else:
                plt.savefig('images/graph.jpg', dpi=300, bbox_inches='tight')

        plt.show()


def bar_chart(df: pd.DataFrame, colname: str, usedate: bool, save=False, savename=None):
    if (usedate):
        data = df[colname].dt.date.value_counts()
    
    options = data.index
    values = data.values
    plt.figure(figsize=(6, 6))
    plt.bar(options, values)
    plt.xticks(rotation=45)
    plt.title(colname, fontproperties=graph_prop, fontsize=15)
    if (save):
            if (savename):
                plt.savefig(f'images/{savename}.jpg', dpi=300, bbox_inches='tight')
            else:
                plt.savefig('images/graph.jpg', dpi=300, bbox_inches='tight')
    plt.show()

def inout_chart(df: pd.DataFrame, col_name: str, out: bool, save=False, savename=None):
    if not out:
        df = df.sort_values(by=col_name, ascending=True).reset_index()
    else:
        df = df.sort_values(by=col_name, ascending=False).reset_index()
    plt.figure(figsize=(10, 6))
    line, = plt.plot(df[f'{col_name}'], df.index, label=f"{col_name.replace('_dt','')}")
    plt.xticks(rotation=90)
    plt.title(f"Horarios de {col_name.replace('_dt','')}")
    plt.xlabel('Hora')
    plt.ylabel('Cantidad de Personas')
    plt.grid()
    plt.legend()
    if (save):
            if (savename):
                plt.savefig(f'images/{savename}.jpg', dpi=300, bbox_inches='tight')
            else:
                plt.savefig('images/graph.jpg', dpi=300, bbox_inches='tight')
    
    cursor = mplcursors.cursor(line, hover=True)
    cursor.connect('add', lambda sel: sel.annotation.set_text(
        f"Hora: {df[col_name].iloc[int(sel.index)]}\nCantidad: {int(sel.index)}"
    ))
    plt.tight_layout()
    plt.show()

def inoutfull_chart(df: pd.DataFrame, cols_name: list, out: bool, save=False, savename=None):
    df_sorted = df.copy()

    plt.figure(figsize=(10, 6))
    df_sorted = df_sorted.sort_values(by=cols_name[0], ascending=True).reset_index()
    line_in = plt.plot(df_sorted[f'{cols_name[0]}'], df_sorted.index, label=f"{cols_name[0].replace('_dt','')}", color='green')

    df_sorted = df_sorted.sort_values(by=cols_name[1], ascending=False).reset_index()
    line_out = plt.plot(df_sorted[f'{cols_name[1]}'], df_sorted.index, label=f"{cols_name[1].replace('_dt','')}", color='red')


    plt.xticks(rotation=90)
    plt.title(f"Horarios de ingreso/salida")
    plt.xlabel('Hora')
    plt.ylabel('Cantidad de Personas')
    plt.grid()
    plt.legend()

    # Guardar la imagen si se indica
    if save:
        if savename:
            plt.savefig(f'images/{savename}.jpg', dpi=300, bbox_inches='tight')
        else:
            plt.savefig('images/graph.jpg', dpi=300, bbox_inches='tight')

    # Agregar información sobre los puntos al pasar el ratón
    cursor_in = mplcursors.cursor(line_in, hover=True)
    cursor_out = mplcursors.cursor(line_out, hover=True)

    cursor_in.connect('add', lambda sel: sel.annotation.set_text(
        f"Hora: {df_sorted[cols_name[0]].iloc[int(sel.index)]}\nCantidad: {int(sel.index)}"
    ))

    # Función de anotación para la línea de salida
    cursor_out.connect('add', lambda sel: sel.annotation.set_text(
        f"Hora: {df_sorted[cols_name[1]].iloc[int(sel.index)]}\nCantidad: {int(sel.index)}"
    ))

    # Ajustar el diseño y mostrar el gráfico
    plt.tight_layout()
    plt.show()