# layout/tabs_kpis.py

from dash import dcc, html


def layout_graficas():
    return  dcc.Tab(label="📈 Gráficas", children=[
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
                ])
            ])
        ])