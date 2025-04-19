# layout/filtros.py

from dash import html, dcc

def layout_filtros(
    departamentos, anios, profesiones, clientes, monto_min, monto_max
):
    return html.Div([
        html.Div([
            html.Label("🏢 Departamento:"),
            dcc.Dropdown(
                options=[{"label": d, "value": d} for d in departamentos],
                id="filtro_departamento",
                value=[],
                multi=True
            )
        ], style={"flex": "1", "padding": "10px"}),

        html.Div([
            html.Label("📅 Año:"),
            dcc.Dropdown(
                options=[{"label": str(a), "value": a} for a in anios],
                id="filtro_anio",
                multi=True
            )
        ], style={"flex": "1", "padding": "10px"}),

        html.Div([
            html.Label("👷‍♂️ Profesión:"),
            dcc.Dropdown(
                options=[{"label": p, "value": p} for p in profesiones],
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
                value=[monto_min, monto_max],
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={"flex": "2", "padding": "10px"}),

        html.Div([
            html.Label("🔍 Cliente:"),
            dcc.Dropdown(
                options=[{"label": n, "value": n} for n in clientes],
                id="filtro_cliente",
                multi=True
            )
        ], style={"flex": "2", "padding": "10px"}),

        html.Div([
            html.Br(),
            html.Button("🔄 Resetear Filtros", id="reset_btn", n_clicks=0)
        ], style={"flex": "1", "padding": "10px", "display": "flex", "alignItems": "center"})
    ], style={"display": "flex", "flexWrap": "wrap", "justifyContent": "space-around", "margin": "20px auto", "width": "90%"})
