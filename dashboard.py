import pandas as pd
import requests
import polyline
import folium
import json
import polyline
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, ctx, no_update
from dash.exceptions import PreventUpdate

# Reemplazá con tu API Key real
API_KEY = "AIzaSyBZpi6RTWeNiFrc680OGFicJHDTTvZArsM"

# Cargar rutas
def cargar_rutas(path='_data/rutas_mineras.json'):
    with open(path, 'r') as f:
        rutas = json.load(f)
    return rutas

def generar_mapa_rutas_multiples(rutas):
    # Centrar el mapa en Bolivia
    mapa = folium.Map(location=[-17.5, -66.0], zoom_start=6)

    for ruta in rutas:
        url = (
            f"https://maps.googleapis.com/maps/api/directions/json?"
            f"origin={ruta['origen']}&destination={ruta['destino']}&key={API_KEY}"
        )
        if ruta.get('waypoints'):
            url += f"&waypoints={ruta['waypoints']}"

        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            puntos = polyline.decode(data['routes'][0]['overview_polyline']['points'])
            distancia = data['routes'][0]['legs'][0]['distance']['text']
            duracion = data['routes'][0]['legs'][0]['duration']['text']
            tooltip_text = f"{ruta['nombre']}<br>Distancia: {distancia}<br>Duración: {duracion}"

            folium.PolyLine(
                locations=puntos,
                color=ruta.get('color', 'blue'),
                weight=5,
                tooltip=tooltip_text
            ).add_to(mapa)

            # Icono en origen: mina
            folium.Marker(
                location=puntos[0],
                tooltip="Origen: Mina",
                icon=folium.Icon(icon="industry", prefix="fa", color="darkred")
            ).add_to(mapa)

            # Icono en destino: camión
            folium.Marker(
                location=puntos[-1],
                tooltip="Destino: Transporte",
                icon=folium.Icon(icon="truck", prefix="fa", color="green")
            ).add_to(mapa)
        else:
            print(f"Error en la ruta {ruta['nombre']}: {data['status']}")

    return mapa._repr_html_()

# Tab rutas filtradas
def tab_rutas_filtradas():
    rutas_json = cargar_rutas('_data/rutas_mineras.json')
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
        html.Div([
            html.Label("🏢 Departamento:"),
            dcc.Dropdown(
                options=[{"label": d, "value": d} for d in departamentos_disponibles],
                id="filtro_departamento",
                value=[],
                multi=True
            )
        ], style={"flex": "1", "padding": "10px"}),

        html.Div([
            html.Label("📅 Año:"),
            dcc.Dropdown(
                options=[{"label": str(a), "value": a} for a in anios_disponibles],
                id="filtro_anio",
                multi=True
            )
        ], style={"flex": "1", "padding": "10px"}),

        html.Div([
            html.Label("👷‍♂️ Profesión:"),
            dcc.Dropdown(
                options=[{"label": p, "value": p} for p in profesiones_disponibles],
                id="filtro_profesion",
                multi=True
            )
        ], style={"flex": "1", "padding": "10px"}),

        html.Div([
            html.Label("🔢 Rango de Monto:"),
            dcc.RangeSlider(
                id="filtro_monto",
                min=monto_min,
                max=monto_max,
                step=10,
                value=[monto_min, monto_max],  # Valor por defecto
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={"flex": "2", "padding": "10px"}),

        html.Div([
            html.Label("🔍 Cliente:"),
            dcc.Dropdown(
                options=[{"label": n, "value": n} for n in clientes_disponibles],
                id="filtro_cliente",
                multi=True
            )
        ], style={"flex": "2", "padding": "10px"}),

        html.Div([
            html.Br(),
            html.Button("🔄 Resetear Filtros", id="reset_btn", n_clicks=0)
        ], style={"flex": "1", "padding": "10px", "display": "flex", "alignItems": "center"})
    ], style={"display": "flex", "flexWrap": "wrap", "justifyContent": "space-around", "margin": "20px auto", "width": "90%"}),

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
        ]),
        tab_rutas_filtradas(),
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
    Input("reset_btn", "n_clicks"),
    prevent_initial_call=False
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
    try:
        print("\n=== CALLBACK EJECUTADO ===")
        print("Filtro - Departamento:", departamentos)
        print("Filtro - Año:", anios)
        print("Filtro - Profesión:", profesiones)
        print("Filtro - Rango Monto:", monto_range)
        print("Filtro - Cliente:", clientes)
        dff = df.copy()
        print("→ Total registros iniciales:", dff.shape[0])

        if departamentos:
            dff = dff[dff["DEPARTAMENTO"].isin(departamentos)]
        if anios:
            dff = dff[dff["ANIO"].isin(anios)]
        if profesiones:
            dff = dff[dff["PROFESION"].isin(profesiones)]
        if monto_range and monto_range[0] is not None and monto_range[1] is not None:
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
    except Exception as e:
        print("❌ Error en callback:", str(e))
        return ["Error"] * 6 + [px.scatter(title="Error")] * 6

@app.callback(
    Output('contenedor-mapa-json', 'children'),
    Input('filtro-origen-json', 'value'),
    Input('filtro-destino-json', 'value')
)
def actualizar_mapa_json(origen, destino):
    rutas = cargar_rutas('_data/rutas_mineras.json')

    # Mostrar todas si no hay filtros
    if origen is None and destino is None:
        rutas_filtradas = rutas
    else:
        rutas_filtradas = [
            r for r in rutas
            if (origen is None or r["departamento_origen"] == origen)
            and (destino is None or r["departamento_destino"] == destino)
        ]

    if not rutas_filtradas:
        return html.Div("No se encontraron rutas con los filtros seleccionados.")

    html_mapa = generar_mapa_rutas_multiples(rutas_filtradas)
    return html.Iframe(srcDoc=html_mapa, width='100%', height='600')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
