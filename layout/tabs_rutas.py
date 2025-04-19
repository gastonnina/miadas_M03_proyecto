# layout/tabs_rutas.py
from dash import dcc, html
from utils.data_loader import cargar_rutas_desde_json

def layout_tab_rutas():
    rutas_json = cargar_rutas_desde_json('_data/rutas_mineras.json')
    departamentos = sorted(list(set(
        ruta["departamento_origen"] for ruta in rutas_json
    ).union(
        ruta["departamento_destino"] for ruta in rutas_json
    )))

    return dcc.Tab(label='🛣️ Rutas por Departamento', children=[
        html.H3("Filtrar rutas enriquecidas por origen y destino"),
        html.Div([
            html.Label("Departamento de Origen:"),
            dcc.Dropdown(
                id='filtro-origen-json',
                options=[{'label': d, 'value': d} for d in departamentos],
                placeholder="Selecciona origen"
            ),
            html.Label("Departamento de Destino:"),
            dcc.Dropdown(
                id='filtro-destino-json',
                options=[{'label': d, 'value': d} for d in departamentos],
                placeholder="Selecciona destino"
            ),
        ], style={'width': '40%', 'margin-bottom': '20px'}),

        html.Div(id='contenedor-mapa-json')
    ])
