from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from conexion_sql import conexion
from app import app
import sqlalchemy
from sqlalchemy import create_engine

# Define el diseño de la página 3
def layout():
    return html.Div([
        html.H1("Página 2 - Gráfico de Pastel"),
        
        # Dropdown para seleccionar la categoría del gráfico de pastel
        dcc.Dropdown(
            id='pie-chart-dropdown',
            options=[
                {'label': 'Género', 'value': 'gender'},
                {'label': 'Estado de Viaje', 'value': 'flight_status'},
                {'label': 'Continentes', 'value': 'continent'}
            ],
            value='gender',  # Valor predeterminado
            multi=False
        ),
        
        # Div para mostrar el gráfico de pastel
        dcc.Graph(id='pie-chart')
    ])

# Función para obtener el título personalizado en español
def get_title(selected_category):
    if selected_category == 'gender':
        return 'Distribución de Género'
    elif selected_category == 'flight_status':
        return 'Distribución de Estado de Viaje'
    elif selected_category == 'continent':
        return 'Distribución de Continentes mas visitados'
    else:
        return 'Gráfico de Pastel'

# Callback para actualizar el gráfico de pastel
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('pie-chart-dropdown', 'value')]
)
def update_pie_chart(selected_category):
    # Ejecuta una consulta SQL para obtener los datos de la categoría seleccionada
    if selected_category in ['gender', 'flight_status', 'continent']:
        if selected_category == 'continent':
            query = "SELECT continents as continent, COUNT(*) as Count FROM datos_pasajeros GROUP BY continents"
        else:
            query = f"SELECT {selected_category}, COUNT(*) as Count FROM datos_pasajeros GROUP BY {selected_category}"
        
        conn = conexion()
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Crea el gráfico de pastel con el título personalizado en español
        fig = px.pie(df, names=selected_category, values='count', title=get_title(selected_category))
        
        return fig
    else:
        return px.pie()
