# app.py

from dash import Dash, html, dcc
from layout.filtros import layout_filtros
from layout.tabs_kpis import layout_kpis
from layout.tabs_rutas import layout_tab_rutas
from layout.tabs_tiempo_real import layout_tab_monitoreo_sismos
from utils.transformaciones import cargar_dataset_completo
from callbacks.callbacks_kpis import registrar_callbacks_kpis
from callbacks.callbacks_rutas import registrar_callbacks
from callbacks.callbacks_sismos import registrar_callbacks_sismos

# Cargar datos una vez

df = cargar_dataset_completo()
monto_min = float(df["MONTO"].min()) if not df.empty else 0
monto_max = float(df["MONTO"].max()) if not df.empty else 1

# Listas únicas para filtros
departamentos_disponibles = df["DEPARTAMENTO"].unique().tolist()
anios_disponibles = sorted(df["ANIO"].unique())
profesiones_disponibles = sorted(df["PROFESION"].unique())
clientes_disponibles = sorted(df["NOMBRES"].unique())

# Crear app
app = Dash(__name__)
app.title = "Dashboard Cooperativa Minera"

# Layout general
app.layout = html.Div([
    html.H1("📊 Dashboard Cooperativa Minera", style={"textAlign": "center"}),
    layout_filtros(
        departamentos_disponibles,
        anios_disponibles,
        profesiones_disponibles,
        clientes_disponibles,
        monto_min,
        monto_max
    ),
    layout_kpis(),
    dcc.Tabs([
        layout_tab_rutas(),
        layout_tab_monitoreo_sismos()
    ])
])

# Callbacks
registrar_callbacks_kpis(app, df, monto_min, monto_max)
registrar_callbacks(app)
registrar_callbacks_sismos(app)

# Ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)
