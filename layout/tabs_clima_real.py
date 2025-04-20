from dash import dcc, html, Output, Input
import dash
import requests
import plotly.graph_objs as go
import datetime

# Coordenadas por departamento
DEPARTAMENTOS = {
    "La Paz": {"lat": -16.5, "lon": -68.15},
    "Oruro": {"lat": -17.98, "lon": -67.12},
    "Potosí": {"lat": -19.58, "lon": -65.75},
}

def obtener_clima(dep):
    """Consulta datos actuales de clima de Open-Meteo"""
    lat, lon = DEPARTAMENTOS[dep]["lat"], DEPARTAMENTOS[dep]["lon"]
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,weathercode"
    )
    try:
        resp = requests.get(url, timeout=10).json()
        datos = resp["current"]
        return {
            "temperatura": datos["temperature_2m"],
            "humedad": datos["relative_humidity_2m"],
            "estado": interpretar_codigo_clima(datos["weathercode"])
        }
    except Exception as e:
        return {"temperatura": None, "humedad": None, "estado": "Error"}

def interpretar_codigo_clima(code):
    """Traduce códigos de clima de Open-Meteo"""
    codigos = {
        0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado",
        3: "Nublado", 45: "Neblina", 48: "Neblina con escarcha",
        51: "Llovizna débil", 53: "Llovizna", 55: "Llovizna intensa",
        61: "Lluvia débil", 63: "Lluvia moderada", 65: "Lluvia intensa",
        80: "Chubascos débiles", 81: "Chubascos", 82: "Chubascos fuertes",
    }
    return codigos.get(code, "Desconocido")
def layout_tab_clima():
    return dcc.Tab(label="⏱️ Clima en Tiempo Real - Bolivia", children=[
        html.H3("⏱️ Clima en Tiempo Real - Bolivia"),

        # Tarjetas
        html.Div(id="tarjetas-clima", className="card-container-clima"),

        # Gráfico en tiempo real
        dcc.Graph(id="grafico-temperatura"),

        # Intervalo para actualizar datos
        dcc.Interval(id="interval-clima", interval=60*1000, n_intervals=0)
    ])

@dash.callback(
    [Output("tarjetas-clima", "children"),
     Output("grafico-temperatura", "figure")],
    [Input("interval-clima", "n_intervals")]
)
def actualizar_clima(n):
    tarjetas = []
    temps = []
    labels = []
    now = datetime.datetime.now().strftime("%H:%M:%S")

    for dep in DEPARTAMENTOS:
        clima = obtener_clima(dep)
        tarjetas.append(html.Div([
            html.H4(dep),
            html.P(f"🌡️ Temperatura: {clima['temperatura']} °C"),
            html.P(f"💧 Humedad: {clima['humedad']}%"),
            html.P(f"🌤️ Estado: {clima['estado']}")
        ], className="card-clima"))

        temps.append(clima["temperatura"])
        labels.append(dep)

    figura = go.Figure()
    figura.add_trace(go.Bar(
        x=labels,
        y=temps,
        marker_color=["#0088cc", "#00cc88", "#ff8800"]
    ))
    figura.update_layout(
        title=f"🌡️ Temperatura Actual por Departamento ({now})",
        yaxis_title="Temperatura (°C)",
        xaxis_title="Departamento",
        template="plotly_dark"
    )

    return tarjetas, figura
