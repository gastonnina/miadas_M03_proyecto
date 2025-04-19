# callbacks/callbacks_rutas.py

from dash import Output, Input, html
from utils.data_loader import cargar_rutas_desde_json
from utils.mapas import generar_mapa_rutas_avanzado


def registrar_callbacks(app):

    @app.callback(
        Output('contenedor-mapa-json', 'children'),
        Input('filtro-origen-json', 'value'),
        Input('filtro-destino-json', 'value')
    )
    def actualizar_mapa_json(origen, destino):
        rutas = cargar_rutas_desde_json('_data/rutas_mineras.json')

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

        html_mapa = generar_mapa_rutas_avanzado(rutas_filtradas)
        return html.Iframe(srcDoc=html_mapa, width='100%', height='600')
