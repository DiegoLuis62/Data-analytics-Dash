import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
import os
import pandas as pd
from dash.dependencies import Input, Output, State


from app import app

import pages


server = app.server

PLOTLY_LOGO = "assets/avion-comercial.png"
nav_item = dbc.NavItem(dbc.NavLink("Home", href=app.get_relative_path("/")))
nav_item1 = dbc.NavItem(dbc.NavLink("Grafica 1", href=app.get_relative_path("/Graph1")))
nav_item2 = dbc.NavItem(dbc.NavLink("Grafica 2", href=app.get_relative_path("/Graph2")))
nav_item3 = dbc.NavItem(dbc.NavLink("Grafica 3", href=app.get_relative_path("/Graph3")))
nav_item4 = dbc.NavItem(dbc.NavLink("Grafica 4", href=app.get_relative_path("/Graph4")))

logo = dcc.Location(id="url", refresh=False)
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Viajes Aereopuerto", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item, nav_item1, nav_item2, nav_item3, nav_item4],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ],
    ),
    color="dark",
    dark=True,
    className="mb-0"
)

app.layout = html.Div(
    children=[logo, navbar, html.Div(id="page-content")]
)




@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page_content(pathname):
    path = app.strip_relative_path(pathname)
    if not path:
        return pages.home.layout()
    elif path == "Graph1":
        return pages.grafica1.layout()
    elif path == "Graph2":
        return pages.grafica2.layout()
    elif path == "Graph3":
        return pages.grafica3.layout()
    elif path == "Graph4":
        return pages.grafica4.layout()
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(debug=True)