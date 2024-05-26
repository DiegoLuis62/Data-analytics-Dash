from dash import html  # Cambio aquí
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from conexion_sql import conexion
from app import app
import sqlalchemy
from sqlalchemy import create_engine

# Define el diseño de la página 1
def layout():
    return html.Div([
        html.H1("Página 1 - Gráfico de Barras de Nacionalidades de Pasajeros"),
        dcc.Graph(id='grafico-de-barras'),
        html.Label("Seleccionar género:"),
        dcc.Dropdown(
            id='genero-dropdown',
            options=[
                {'label': 'Hombre', 'value': 'Male'},
                {'label': 'Mujer', 'value': 'Female'},
                {'label': 'Ambos Géneros', 'value': 'Ambos'},
            ],
            value='Ambos',  # Valor predeterminado
            multi=False  # Para permitir una sola selección
        ),
        html.Label("Ordenar por:"),
        dcc.Dropdown(
            id='orden-dropdown',
            options=[
                {'label': 'Ascendente', 'value': 'ascendente'},
                {'label': 'Descendente', 'value': 'descendente'},
            ],
            value='descendente',  # Valor predeterminado
            multi=False  # Para permitir una sola selección
        ),
        html.Label("Seleccionar mes o todo el año:"),
        dcc.Dropdown(
            id='mes-dropdown',
            options=[
                {'label': 'Todo el año', 'value': 'todo_el_anio'},
                {'label': 'Enero', 'value': 1},
                {'label': 'Febrero', 'value': 2},
                {'label': 'Marzo', 'value': 3},
                {'label': 'Abril', 'value': 4},
                {'label': 'Mayo', 'value': 5},
                {'label': 'Junio', 'value': 6},
                {'label': 'Julio', 'value': 7},
                {'label': 'Agosto', 'value': 8},
                {'label': 'Septiembre', 'value': 9},
                {'label': 'Octubre', 'value': 10},
                {'label': 'Noviembre', 'value': 11},
                {'label': 'Diciembre', 'value': 12},
            ],
            value="todo_el_anio",  # Valor predeterminado (Enero)
            multi=False  # Para permitir una sola selección
        ),
    ])

# Callback para actualizar el gráfico de barras
@app.callback(
    Output('grafico-de-barras', 'figure'),
    [
        Input('genero-dropdown', 'value'),
        Input('orden-dropdown', 'value'),
        Input('mes-dropdown', 'value'),
    ]
)
def actualizar_grafico(genero, orden, mes):
    # Realiza la consulta SQL y ajustes de DataFrame según las selecciones
    # en los dropdowns y crea el gráfico en función de esas selecciones
    # Devuelve la figura actualizada

    if mes == 'todo_el_anio':
        # Si se selecciona 'Todo el año', no aplicamos filtro por mes
        if genero == 'Ambos':
            # Si 'Ambos Géneros' está seleccionado, no aplicamos filtro por género
            consulta_sql = """
            SELECT nationality, COUNT(*) as pasajero
            FROM datos_pasajeros
            GROUP BY nationality
            ORDER BY pasajero DESC
            LIMIT 15
            """
            df = pd.read_sql_query(consulta_sql, conexion())
        else:
            # Si se selecciona un género específico, aplicamos el filtro correspondiente
            consulta_sql = """
            SELECT nationality, COUNT(*) as pasajero
            FROM datos_pasajeros
            WHERE gender = %s
            GROUP BY nationality
            ORDER BY pasajero DESC
            LIMIT 15
            """
            df = pd.read_sql_query(consulta_sql, conexion(), params=(genero,))
    else:
        # Si se selecciona un mes específico, aplicamos el filtro por mes
        if genero == 'Ambos':
            # Si 'Ambos Géneros' está seleccionado, no aplicamos filtro por género
            consulta_sql = """
            SELECT nationality, COUNT(*) as pasajero
            FROM datos_pasajeros
            WHERE EXTRACT(MONTH FROM departure_date) = %s
            GROUP BY nationality
            ORDER BY pasajero DESC
            LIMIT 15
            """
            df = pd.read_sql_query(consulta_sql, conexion(), params=(mes,))
        else:
            # Si se selecciona un género específico, aplicamos el filtro correspondiente
            consulta_sql = """
            SELECT nationality, COUNT(*) as pasajero
            FROM datos_pasajeros
            WHERE gender = %s AND EXTRACT(MONTH FROM departure_date) = %s
            GROUP BY nationality
            ORDER BY pasajero DESC
            LIMIT 15
            """
            df = pd.read_sql_query(
                consulta_sql, conexion(), params=(genero, mes))

    if orden == 'ascendente':
        # Ordena los datos en orden ascendente
        df = df.sort_values(by='pasajero', ascending=True)
    elif orden == 'descendente':
        # Ordena los datos en orden descendente (predeterminado)
        df = df.sort_values(by='pasajero', ascending=False)

    fig = px.bar(df, x='nationality', y='pasajero',
                 title="Nacionalidades de Pasajeros (Top 15)")
    fig.update_xaxes(title_text='Nacionalidad')
    fig.update_yaxes(title_text='Pasajero')

    return fig
