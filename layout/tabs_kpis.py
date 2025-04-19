# layout/tabs_kpis.py

from dash import dcc, html
from layout.tabs_rutas import layout_tab_rutas


def layout_kpis():
    return html.Div([
        html.Div([
            html.Div(id="kpi_1", className="card"), html.Div(id="kpi_2", className="card"),
            html.Div(id="kpi_3", className="card"), html.Div(id="kpi_4", className="card"),
            html.Div(id="kpi_5", className="card"), html.Div(id="kpi_6", className="card")
        ], className="kpi-container"),

        dcc.Tabs([
            dcc.Tab(label="📍 Por Ubicación", children=[
                dcc.Tabs([
                    dcc.Tab(label="🔹 Monto por Departamento", children=[dcc.Graph(id="graf_1")]),
                    dcc.Tab(label="🔹 Cantidad de Movimientos", children=[dcc.Graph(id="graf_4")]),
                    dcc.Tab(label="🔹 Participación del Monto", children=[dcc.Graph(id="graf_6")])
                ])
            ]),
            dcc.Tab(label="📈 Por Tiempo", children=[
                dcc.Tabs([
                    dcc.Tab(label="📊 Monto por Año", children=[dcc.Graph(id="graf_2")])
                ])
            ]),
            dcc.Tab(label="👥 Por Cliente", children=[
                dcc.Tabs([
                    dcc.Tab(label="📦 Clientes por Departamento", children=[dcc.Graph(id="graf_5")]),
                    dcc.Tab(label="📊 Distribución de Montos", children=[dcc.Graph(id="graf_3")])
                ])
            ]),
            dcc.Tab(label="🛣️ Rutas por Departamento", children=[layout_tab_rutas()])
        ])
    ])
