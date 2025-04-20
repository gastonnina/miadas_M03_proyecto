# callbacks/callbacks_sismos.py

import requests
import pandas as pd
import plotly.express as px
from dash import Output, Input, html, dcc, State


def registrar_callbacks_sismos(app):

    @app.callback(
        Output("filtro-magnitud", "value"),
        Output("filtro-tiempo", "value"),
        Output("filtro-region", "value"),
        Output("contenedor-sismos-tiempo-real", "children"),
        Input("intervalo-sismos", "n_intervals"),
        Input("filtro-magnitud", "value"),
        Input("filtro-tiempo", "value"),
        Input("filtro-region", "value"),

    )
    def actualizar_sismos(n, magnitud_minima, rango_tiempo, region):
        try:
            print(f"🔁 Ejecutando callback de sismos (intervalo {n})")

            feeds = {
                "1h": "all_hour.geojson",
                "6h": "all_day.geojson",
                "12h": "all_day.geojson",
                "24h": "all_day.geojson"
            }
            feed = feeds.get(rango_tiempo, "all_hour.geojson")
            url = f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{feed}"
            response = requests.get(url, timeout=10)
            data = response.json()

            features = data.get("features", [])
            print("Número de features:", len(features))
            if not features:
                return html.Div("No se encontraron sismos recientes.")

            sismos = pd.DataFrame([
                {
                    "Lugar": f["properties"]["place"],
                    "Magnitud": f["properties"]["mag"],
                    "Tiempo": pd.to_datetime(f["properties"]["time"], unit='ms'),
                    "Latitud": f["geometry"]["coordinates"][1],
                    "Longitud": f["geometry"]["coordinates"][0]
                } for f in features
                if f.get("properties")
                and f["properties"].get("mag") is not None
                and f.get("geometry")
                and f["geometry"].get("coordinates")
                and len(f["geometry"]["coordinates"]) >= 2
            ])

            sismos = sismos.dropna(subset=["Latitud", "Longitud", "Magnitud"])
            total_original = sismos.shape[0]
            sismos_sin_filtros = sismos.copy()

            
            if magnitud_minima is not None:
                sismos = sismos[sismos["Magnitud"] >= magnitud_minima]

            if region:
                sismos = sismos[sismos["Lugar"].str.contains(region, case=False, na=False)]

            print("Sismos válidos cargados tras filtros:", sismos.shape[0])

            fallback_aplicado = False
            if sismos.empty:
                sismos = sismos_sin_filtros
                fallback_aplicado = True
                print("⚠️ No hay datos con filtros, mostrando todos.")

            fig_mapa = px.scatter_geo(
                sismos,
                lat="Latitud",
                lon="Longitud",
                color="Magnitud",
                hover_name="Lugar",
                size="Magnitud",
                size_max=20,
                title="Ubicación de sismos recientes",
                color_continuous_scale="Reds",
                projection="natural earth"
            )

            fig_barras = px.bar(
                sismos.sort_values("Tiempo", ascending=False).head(15),
                x="Tiempo",
                y="Magnitud",
                color="Magnitud",
                hover_data=["Lugar"],
                title="Magnitudes recientes de los últimos sismos"
            )

            mensaje_fallback = html.P(
                "⚠️ No se encontraron coincidencias con los filtros seleccionados. Mostrando todos los datos disponibles.",
                style={"color": "#856404", "backgroundColor": "#fff3cd", "padding": "10px", "borderRadius": "5px"}
            ) if fallback_aplicado else None

            contador = html.P(f"🔢 Mostrando {sismos.shape[0]} sismos.")

            contenido = html.Div([
                mensaje_fallback,
                contador,
                dcc.Graph(figure=fig_mapa),
                dcc.Graph(figure=fig_barras)
            ])

            from dash import no_update
            return no_update, no_update, no_update, contenido
                

        except Exception as e:
            print("❌ Error en callback de sismos:", str(e))
            from dash import no_update
            return html.Div(f"Error al obtener datos de sismos: {str(e)}"), no_update, no_update, no_update
