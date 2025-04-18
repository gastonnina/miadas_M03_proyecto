import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, ctx, no_update
from dash.exceptions import PreventUpdate

# Cargar los dataframes desde archivos feather
df_clientes = pd.read_feather("_data/clientes.feather")
df_cuentas = pd.read_feather("_data/cuentas.feather")
df_movimientos = pd.read_feather("_data/movimientos.feather")
df_departamentos = pd.read_feather("_data/departamentos.feather")
df_profesiones = pd.read_feather("_data/profesiones.feather")

# Renombrar columnas para evitar conflictos
df_departamentos = df_departamentos.rename(columns={"DESCRIPCION": "DEPARTAMENTO"})
df_profesiones = df_profesiones.rename(columns={"DESCRIPCION": "PROFESION"})

# Unir los datos en un solo DataFrame para análisis
df = df_movimientos.merge(df_cuentas, on="CUENTA")
df = df.merge(df_clientes, on="CARNET")
df = df.merge(df_departamentos, on="CODEPTO")
df = df.merge(df_profesiones, on="CODPROF")
df["FECHA"] = pd.to_datetime(df["FECHA"], dayfirst=True)
df["ANIO"] = df["FECHA"].dt.year

# Valores por defecto seguros
departamentos_disponibles = df["DEPARTAMENTO"].unique().tolist()
anios_disponibles = sorted(df["ANIO"].unique())
profesiones_disponibles = sorted(df["PROFESION"].unique())
clientes_disponibles = sorted(df["NOMBRES"].unique())
monto_min = float(df["MONTO"].min()) if not df.empty else 0
monto_max = float(df["MONTO"].max()) if not df.empty else 1

# Iniciar la app Dash
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("📊 Dashboard Cooperativa Minera", style={"textAlign": "center"}),

    html.Div([
        html.Label("🏢 Departamento:"),
        dcc.Dropdown(
            options=[{"label": d, "value": d} for d in departamentos_disponibles],
            id="filtro_departamento",
            multi=True
        ),
        html.Label("📅 Año:"),
        dcc.Dropdown(
            options=[{"label": str(a), "value": a} for a in anios_disponibles],
            id="filtro_anio",
            multi=True
        ),
        html.Label("👷‍♂️ Profesión:"),
        dcc.Dropdown(
            options=[{"label": p, "value": p} for p in profesiones_disponibles],
            id="filtro_profesion",
            multi=True
        ),
        html.Label("🔢 Rango de Monto:"),
        dcc.RangeSlider(
            id="filtro_monto",
            min=monto_min,
            max=monto_max,
            step=10,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.Label("🔍 Cliente:"),
        dcc.Dropdown(
            options=[{"label": n, "value": n} for n in clientes_disponibles],
            id="filtro_cliente",
            multi=True
        ),
        html.Br(),
        html.Button("🔄 Resetear Filtros", id="reset_btn", n_clicks=0)
    ], style={"width": "80%", "margin": "auto"}),

    html.Div([
        html.Div(id="kpi_1", className="card"), html.Div(id="kpi_2", className="card"),
        html.Div(id="kpi_3", className="card"), html.Div(id="kpi_4", className="card"),
        html.Div(id="kpi_5", className="card"), html.Div(id="kpi_6", className="card")
    ], style={"display": "flex", "justifyContent": "space-around", "padding": "20px"}),

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

@app.callback(
    [
        Output("filtro_departamento", "value"),
        Output("filtro_anio", "value"),
        Output("filtro_profesion", "value"),
        Output("filtro_monto", "value"),
        Output("filtro_cliente", "value")
    ],
    Input("reset_btn", "n_clicks")
)
def reset_filters(n_clicks):
    if ctx.triggered_id == "reset_btn":
        return None, None, None, [monto_min, monto_max], None
    raise PreventUpdate

@app.callback(
    [
        Output("kpi_1", "children"), Output("kpi_2", "children"), Output("kpi_3", "children"),
        Output("kpi_4", "children"), Output("kpi_5", "children"), Output("kpi_6", "children"),
        Output("graf_1", "figure"), Output("graf_2", "figure"), Output("graf_3", "figure"),
        Output("graf_4", "figure"), Output("graf_5", "figure"), Output("graf_6", "figure")
    ],
    [
        Input("filtro_departamento", "value"),
        Input("filtro_anio", "value"),
        Input("filtro_profesion", "value"),
        Input("filtro_monto", "value"),
        Input("filtro_cliente", "value")
    ]
)
def update_dashboard(departamentos, anios, profesiones, monto_range, clientes):
    dff = df.copy()
    if departamentos:
        dff = dff[dff["DEPARTAMENTO"].isin(departamentos)]
    if anios:
        dff = dff[dff["ANIO"].isin(anios)]
    if profesiones:
        dff = dff[dff["PROFESION"].isin(profesiones)]
    if monto_range:
        dff = dff[(dff["MONTO"] >= monto_range[0]) & (dff["MONTO"] <= monto_range[1])]
    if clientes:
        dff = dff[dff["NOMBRES"].isin(clientes)]

    if dff.empty:
        return ["Sin datos"] * 6 + [px.scatter(title="Sin datos")] * 6

    kpis = [
        html.Div(f"📌 Total Movimientos: {dff.shape[0]}"),
        html.Div(f"💰 Total Monto: Bs {dff['MONTO'].sum():,.2f}"),
        html.Div(f"📊 Monto Promedio: Bs {dff['MONTO'].mean():,.2f}"),
        html.Div(f"📂 Cuentas Activas: {dff['CUENTA'].nunique()}"),
        html.Div(f"👤 Clientes Únicos: {dff['CARNET'].nunique()}"),
        html.Div(f"💎 Monto Máximo: Bs {dff['MONTO'].max():,.2f}")
    ]

    fig1 = px.bar(dff.groupby("DEPARTAMENTO")["MONTO"].sum().reset_index(), x="DEPARTAMENTO", y="MONTO", title="Monto por Departamento")
    fig2 = px.histogram(dff, x="ANIO", y="MONTO", histfunc="sum", title="Monto por Año")
    fig3 = px.box(dff, x="DEPARTAMENTO", y="MONTO", title="Distribución de Montos por Departamento")
    fig4 = px.histogram(dff, x="DEPARTAMENTO", title="Cantidad de Movimientos por Departamento")
    fig5 = px.bar(dff.groupby("DEPARTAMENTO")["CARNET"].nunique().reset_index(), x="DEPARTAMENTO", y="CARNET", title="Clientes por Departamento")
    fig6 = px.pie(dff, names="DEPARTAMENTO", values="MONTO", title="Participación del Monto por Departamento")

    return (*kpis, fig1, fig2, fig3, fig4, fig5, fig6)

if __name__ == "__main__":
    app.run_server(debug=True)
