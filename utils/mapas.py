# utils/mapas.py

import folium
import requests
import polyline

API_KEY = "AIzaSyBZpi6RTWeNiFrc680OGFicJHDTTvZArsM"


def generar_mapa_rutas_avanzado(rutas):
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

            colores_riesgo = {"bajo": "green", "medio": "orange", "alto": "red"}
            color_linea = ruta.get("color")

            tooltip = (
                f"<b>{ruta['nombre']}</b><br>"
                f"Mineral: {ruta['mineral']}<br>"
                f"Empresa: {ruta['empresa_transportista']}<br>"
                f"Carga: {ruta['carga_toneladas']} t<br>"
                f"Distancia: {distancia} | Duración: {duracion}<br>"
                f"Camino: {ruta['tipo_camino']} | Altitud: {ruta['altitud_promedio']} m<br>"
                f"Estado: {ruta['estado']} | Riesgo: {ruta['riesgo']}<br>"
                f"Temperatura: {ruta['temperatura_media']} °C"
            )

            folium.PolyLine(
                locations=puntos,
                color=color_linea,
                weight=2 + ruta['carga_toneladas'] / 10,
                tooltip=tooltip
            ).add_to(mapa)

            folium.Marker(
                location=puntos[0],
                tooltip="Origen: Mina",
                icon=folium.Icon(icon="industry", prefix="fa", color="darkred")
            ).add_to(mapa)

            folium.Marker(
                location=puntos[-1],
                tooltip="Destino: Transporte",
                icon=folium.Icon(icon="truck", prefix="fa", color="green")
            ).add_to(mapa)
        else:
            print(f"Error en la ruta {ruta['nombre']}: {data['status']}")

    return mapa._repr_html_()
