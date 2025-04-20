from dash import dcc, html

def layout_kpis():
    return  dcc.Tab(label="📊 KPIs", children=[
            html.Div([
                html.Div(id="kpi_1", className="card"),
                html.Div(id="kpi_2", className="card"),
                html.Div(id="kpi_3", className="card"),
                html.Div(id="kpi_4", className="card"),
                html.Div(id="kpi_5", className="card"),
                html.Div(id="kpi_6", className="card")
            ], className="kpi-container")
        ])