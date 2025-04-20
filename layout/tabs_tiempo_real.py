# layout/tabs_tiempo_real.py

from dash import dcc, html


def layout_tab_monitoreo_sismos():
    return dcc.Tab(
        label="🌐 Monitoreo Sísmico Global",
        children=[
            html.H3("🌍 Sismos Recientes (fuente: USGS, actualizado cada minuto)"),
            html.Div(
                [
                    html.Label("🔎 Magnitud mínima:"),
                    dcc.Slider(
                        id="filtro-magnitud",
                        min=0,
                        max=10,
                        step=0.1,
                        value=2.5,
                        marks={i: str(i) for i in range(0, 11)},
                        tooltip={"always_visible": False, "placement": "bottom"},
                    ),
                    html.Label("🕒 Intervalo de tiempo:"),
                    dcc.Dropdown(
                        id="filtro-tiempo",
                        options=[
                            {"label": "Última hora", "value": "1h"},
                            {"label": "Últimas 6 horas", "value": "6h"},
                            {"label": "Últimas 12 horas", "value": "12h"},
                            {"label": "Últimas 24 horas", "value": "24h"},
                        ],
                        value="1h",
                        placeholder="Selecciona el rango de tiempo",
                    ),
                    html.Label("🌎 Filtrar por región (texto libre):"),
                    dcc.Input(
                        id="filtro-region",
                        type="text",
                        placeholder="Ej. Chile, California, Perú...",
                        debounce=True,
                        style={"width": "100%", "marginTop": "8px"},
                    ),
                ],
                className="tab-content",
            ),
            html.Div(id="contenedor-sismos-tiempo-real"),
            dcc.Interval(
                id="intervalo-sismos", interval=60000, n_intervals=0
            ),  # actualiza cada 60 segundos
        ],
    )
