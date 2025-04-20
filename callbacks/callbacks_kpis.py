# callbacks/callbacks_kpis.py

from dash import Output, Input, ctx
from dash.exceptions import PreventUpdate
import plotly.express as px
from dash import html

def registrar_callbacks_kpis(app, df, monto_min, monto_max):

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
        print("🚨 reset_filters ejecutado con n_clicks =", n_clicks)
        # if ctx.triggered_id == "reset_btn":
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
        print("\n=== CALLBACK EJECUTADO ===")
        print("Filtro - Departamento:", departamentos)
        print("Filtro - Año:", anios)
        print("Filtro - Profesión:", profesiones)
        print("Filtro - Rango Monto:", monto_range)
        print("Filtro - Cliente:", clientes)
        try:
            dff = df.copy()

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
                html.Div(f"\ud83d\udccc Total Movimientos: {dff.shape[0]}"),
                html.Div(f"\ud83d\udcb0 Total Monto: Bs {dff['MONTO'].sum():,.2f}"),
                html.Div(f"\ud83d\udcca Monto Promedio: Bs {dff['MONTO'].mean():,.2f}"),
                html.Div(f"\ud83d\udcc2 Cuentas Activas: {dff['CUENTA'].nunique()}"),
                html.Div(f"\ud83d\udc64 Clientes \u00dAnicos: {dff['CARNET'].nunique()}"),
                html.Div(f"\ud83d\udc8e Monto Máximo: Bs {dff['MONTO'].max():,.2f}")
            ]

            fig1 = px.bar(dff.groupby("DEPARTAMENTO")["MONTO"].sum().reset_index(), x="DEPARTAMENTO", y="MONTO", title="Monto por Departamento")
            fig2 = px.histogram(dff, x="ANIO", y="MONTO", histfunc="sum", title="Monto por Año")
            fig3 = px.box(dff, x="DEPARTAMENTO", y="MONTO", title="Distribución de Montos por Departamento")
            fig4 = px.histogram(dff, x="DEPARTAMENTO", title="Cantidad de Movimientos por Departamento")
            fig5 = px.bar(dff.groupby("DEPARTAMENTO")["CARNET"].nunique().reset_index(), x="DEPARTAMENTO", y="CARNET", title="Clientes por Departamento")
            fig6 = px.pie(dff, names="DEPARTAMENTO", values="MONTO", title="Participación del Monto por Departamento")

            return (*kpis, fig1, fig2, fig3, fig4, fig5, fig6)
        except Exception:
            return ["Error"] * 6 + [px.scatter(title="Error")] * 6
