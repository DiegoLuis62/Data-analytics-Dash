import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from conexion_sql import conexion
from app import app

# Define el diseño de la página 4 (Gráfico de Burbujas)
def layout():
    return html.Div([
        html.H1("Página 4 - Gráfico de Burbujas"),
        
        # Dropdown para seleccionar las variables a mostrar
        dcc.Dropdown(
            id='bubble-chart-dropdown',
            options=[
                {'label': 'Nacionalidad vs. Continente vs. Cantidad de Pasajeros', 'value': 'nationality_vs_continent_vs_passengers'},
                {'label': 'Estado de Vuelo vs. Aeropuerto de Destino vs. Cantidad de Vuelos', 'value': 'flight_status_vs_arrival_airport_vs_flight_count'},
            ],
            value='nationality_vs_continent_vs_passengers',  # Valor predeterminado
            multi=False
        ),
        
        # Div para mostrar el gráfico de burbujas
        dcc.Graph(id='bubble-chart')
    ])

# Callback para actualizar el gráfico de burbujas
@app.callback(
    Output('bubble-chart', 'figure'),
    [Input('bubble-chart-dropdown', 'value')]
)
def update_bubble_chart(selected_option):
    query = """
    SELECT {}, {}, COUNT(*) as count
    FROM datos_pasajeros
    GROUP BY {}, {}
    ORDER BY count DESC
    LIMIT 50
    """
    
    if selected_option == 'nationality_vs_continent_vs_passengers':
        query = query.format('nationality', 'continents', 'nationality', 'continents')
    elif selected_option == 'flight_status_vs_arrival_airport_vs_flight_count':
        query = query.format('flight_status', 'arrival_airport', 'flight_status', 'arrival_airport')
    
    # Conecta a la base de datos y ejecuta la consulta
    conn = conexion()
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Crea el gráfico de burbujas
    if selected_option == 'nationality_vs_continent_vs_passengers':
        fig = px.scatter(df, x='nationality', y='continents', size='count',
                         title='Nacionalidad vs. Continente vs. Cantidad de Pasajeros',
                         labels={'count': 'Cantidad de Pasajeros'})
    elif selected_option == 'flight_status_vs_arrival_airport_vs_flight_count':
        fig = px.scatter(df, x='flight_status', y='arrival_airport', size='count',
                         title='Estado de Vuelo vs. Aeropuerto de Destino vs. Cantidad de Vuelos',
                         labels={'count': 'Cantidad de Vuelos'})
    
    return fig
