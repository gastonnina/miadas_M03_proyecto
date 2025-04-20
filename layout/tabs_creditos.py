from dash import dcc, html

def layout_creditos():
    return  dcc.Tab(label="ℹ️ Créditos", children=[
            html.Div([
                html.H2("👥 Créditos del Proyecto", style={"marginBottom": "20px"}),

                html.H4("📌 Roles y Contribuciones"),
                html.Ul([
                    html.Li([
                        html.Strong("Paolo Ramos Mendez – Data Visualization Specialist: "),
                        "Desarrolló las rutas de mapas, diseñó los indicadores clave de desempeño (KPIs) y construyó un gráfico con simulación en tiempo real."
                    ]),
                    html.Li([
                        html.Strong("Gaston Nina Sossa – Data Engineer & Analyst: "),
                        "Se encargó de la generación y limpieza de los datos, el diseño de los KPIs, y la implementación de un gráfico con simulación en tiempo real."
                    ])
                ]),

                html.Br(),
                html.P("Este dashboard fue desarrollado como parte de un proyecto académico de visualización de datos interactiva."),
                html.P("Construido con Python, Dash, Plotly y ❤️ por estudiantes apasionados por la ciencia de datos.")
            ], style={"padding": "25px", "lineHeight": "1.8"})
        ])