# app.py

from dash import Dash, html, dcc
from layout.filtros import layout_filtros
from layout.tabs_kpis import layout_kpis
from utils.transformaciones import cargar_dataset_completo
from callbacks.callbacks_kpis import registrar_callbacks_kpis
from callbacks.callbacks_rutas import registrar_callbacks

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
    layout_filtros(departamentos_disponibles, anios_disponibles, profesiones_disponibles, clientes_disponibles, monto_min, monto_max),
    layout_kpis(),
])

# Callbacks
registrar_callbacks_kpis(app, df, monto_min, monto_max)
registrar_callbacks(app)

# Ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)

