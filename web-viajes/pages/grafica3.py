# Importa las bibliotecas necesarias
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
# Importa tu función de conexión desde tu módulo basesdedatos
from conexion_sql import conexion
from app import app

# Define la función de diseño para la tercera página


def layout():
    return html.Div([
        html.H1("Página 3 - Gráfico de Radar"),

        # Dropdown para seleccionar las variables a comparar
        dcc.Dropdown(
            id='radar-chart-dropdown',
            options=[
                {'label': 'Edad vs. Estado de Vuelo',
                    'value': 'age_vs_flight_status'},
                {'label': 'Nacionalidad vs. Estado de Vuelo',
                    'value': 'nationality_vs_flight_status'}
            ],
            value='age_vs_flight_status',  # Valor predeterminado
            multi=False
        ),

        # Div para mostrar el Gráfico de Radar
        dcc.Graph(id='radar-chart')
    ])

# Define la función de callback para actualizar el Gráfico de Radar


@app.callback(
    Output('radar-chart', 'figure'),
    [Input('radar-chart-dropdown', 'value')]
)
def update_radar_chart(selected_option):
    # Define y ejecuta la consulta SQL según la opción seleccionada
    if selected_option == 'age_vs_flight_status':
        query = """
        SELECT flight_status, AVG(age) as avg_age
        FROM datos_pasajeros
        GROUP BY flight_status;
        """
    elif selected_option == 'nationality_vs_flight_status':
        query = """
    SELECT flight_status, nationality, COUNT(*) as count
    FROM (
        SELECT flight_status, nationality
        FROM datos_pasajeros
        WHERE nationality IN (
            SELECT nationality
            FROM datos_pasajeros
            GROUP BY nationality
            ORDER BY COUNT(*) DESC
            LIMIT 10
        )
    ) AS top_nationalities
    GROUP BY flight_status, nationality
    """

    conn = conexion()
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Crea el Gráfico de Radar
    fig = go.Figure()

    if selected_option == 'age_vs_flight_status':
        fig.add_trace(go.Scatterpolar(
            r=df['avg_age'],
            theta=df['flight_status'],
            fill='toself',
            name='Edad Promedio'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(df['avg_age']) + 10]
                )
            )
        )
    elif selected_option == 'nationality_vs_flight_status':
        # Crea subtramas para cada nacionalidad
        for nationality in df['nationality'].unique():
            data = df[df['nationality'] == nationality]
            fig.add_trace(go.Scatterpolar(
                r=data['count'],
                theta=data['flight_status'],
                fill='toself',
                name=nationality
            ))

    return fig
