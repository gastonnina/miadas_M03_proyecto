# layout/tabs_kpis.py

from dash import dcc, html
from layout.tabs_rutas import layout_tab_rutas


def layout_kpis():
    return  dcc.Tab(label="📊 KPIs", children=[
            html.Div([
                html.Div(id="kpi_1", className="card"),
                html.Div(id="kpi_2", className="card"),
                html.Div(id="kpi_3", className="card"),
                html.Div(id="kpi_4", className="card"),
                html.Div(id="kpi_5", className="card"),
                html.Div(id="kpi_6", className="card")
            ], className="kpi-container")
        ])