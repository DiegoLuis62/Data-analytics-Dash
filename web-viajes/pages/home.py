import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pyodbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots


from app import app


titulo = "Viajes aereopuerto 2022"

# Define los nombres de los integrantes
Por = "Diego Luis Linero Ramirez"

# Define la información de la fuente de los datos
fuente = "el csv fue obtenido de https://www.kaggle.com/datasets/iamsouravbanerjee/airline-dataset Página web del Kagle para crear la base de datos."

# Define una lista de las herramientas utilizadas
herramientas = ["Python", "Dash", "HTML", "CSS"]

informacion ="""Este conjunto de datos es de gran importancia en la industria de la aerolínea, ya que proporciona información valiosa sobre operaciones de vuelo, rutas, horarios, datos demográficos de los pasajeros y preferencias. Esta información permite a las aerolíneas optimizar sus operaciones y mejorar la experiencia del cliente. También es fundamental para identificar tendencias, mejorar la puntualidad y tomar medidas ante interrupciones como retrasos o cancelaciones.

Además, organismos reguladores y responsables de políticas aéreas utilizan estos datos para garantizar la seguridad y hacer cumplir regulaciones. Los investigadores los emplean para estudiar tendencias de mercado, evaluar impactos ambientales y desarrollar estrategias de crecimiento sostenible en la industria. En resumen, estos datos son fundamentales para la toma de decisiones informadas, la eficiencia operativa y el avance de la industria de la aviación.

El conjunto de datos incluye información diversa sobre operaciones aéreas a nivel mundial, como detalles de pasajeros, rutas de vuelo, información de la tripulación y estados de vuelo. Esto brinda una visión completa de la demografía de los pasajeros, detalles de viaje, rendimiento de los pilotos y estados de vuelo, lo que facilita el análisis de tendencias y la optimización de la operación de vuelos."""

def layout ():return[html.Div([
    html.H1(titulo,style={'text-align': 'center'}),
    html.H2("Fuente de los datos:"),
    html.P(fuente, style={'font-size': '20px'}),
    html.H2("Sobre la base de datos:"),
    html.P(informacion, style={'font-size': '20px', 'text-align': 'justify'}),
    html.H2("Herramientas utilizadas:"),
    html.Ul([html.Li(h) for h in herramientas], style={'font-size': '18px'}),
    html.H2("Por:"),
    html.P(Por, style={'font-size': '20px'}),
],style={
        "background-color": "#333333",
        "color": "white",
        "padding": "50px",
        "font-family": "sans-serif"
    }
)]