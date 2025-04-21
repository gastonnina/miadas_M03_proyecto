# 📊 Dashboard Interactivo en Tiempo Real – Cooperativa Minera ⛏️

## 🎯 Objetivo General
Desarrollar un dashboard interactivo para visualizar y analizar datos financieros y operativos de una **cooperativa minera**, con filtros dinámicos, mapas interactivos, análisis en tiempo real y métricas clave.

---

## 👥 Integrantes

- Paolo Ramos Mendez
- Gaston Nina Sosa

---

## 🗂️ Estructura del Proyecto

```
.
├── app.py                         # Aplicación principal Dash
├── _data/                         # Datos en CSV y Feather
│   ├── clientes.csv / .feather    # Datos de clientes
│   ├── cuentas.csv / .feather     # Cuentas bancarias
│   ├── movimientos.csv / .feather # Movimientos financieros
│   ├── departamentos.csv/.feather # Catálogo de departamentos
│   ├── profesiones.csv/.feather   # Catálogo de profesiones
│   └── rutas_mineras.json         # Rutas entre ciudades mineras
├── assets/
│   └── styles.css                 # Estilos personalizados (CSS)
├── layout/                        # Layouts modulares (tabs y filtros)
│   ├── filtros.py
│   ├── layout_kpis.py
│   ├── layout_tabs.py
│   ├── tabs_rutas.py              # Módulo de rutas con mapa
│   └── tabs_sismos.py             # Módulo en tiempo real de sismos
├── callbacks/                     # Callbacks organizados por módulo
│   ├── callbacks_dashboard.py
│   ├── callbacks_rutas.py
│   └── callbacks_sismos.py
├── utils/                         # Utilidades compartidas
│   ├── data_loader.py             # Carga y manipulación de datos
│   └── mapa_utils.py              # Mapas con Google Maps API + Folium
├── Dockerfile
├── pyproject.toml
├── .gitignore
└── README.md
```

---

## ⚙️ Requisitos

- Python ≥ 3.9
- [PDM](https://pdm.fming.dev/) como gestor de dependencias

Librerías principales:

- `dash`
- `plotly`
- `pandas`
- `requests`
- `polyline`
- `folium`
- `faker`
- `pyarrow`
- `numpy`

---

## 📦 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/usuario/cooperativa-dashboard.git
cd cooperativa-dashboard
```

2. Instalar dependencias con PDM:

```bash
pdm install
```

---

## 🚀 Ejecución

```bash
pdm run python app.py
```

Esto abrirá una instancia local del dashboard en:  
📍 `http://127.0.0.1:8050`

---

## 🧪 Datos

Los datos provienen de archivos `.csv` y `.feather` en la carpeta `_data/`. Para mejor rendimiento se usan los `.feather`. 

Convertir `.csv` a `.feather`:

```python
import pandas as pd
df = pd.read_csv("_data/clientes.csv", sep=";")
df.to_feather("_data/clientes.feather")
```

---

## 📊 Funcionalidades del Dashboard

- Filtros dinámicos por:
  - Departamento
  - Año
  - Profesión
  - Cliente
  - Rango de montos
- Indicadores clave (KPIs)
- Visualizaciones interactivas por pestañas:
  - 📍 Por Ubicación (barras, tortas, KPIs)
  - 📈 Por Tiempo (montos por año)
  - 👥 Por Cliente (movimientos y distribución)
  - 🛣️ Rutas por Departamento (mapas con Google Maps)
  - 🌍 Sismos en Tiempo Real (datos USGS + filtros por magnitud, región y tiempo)

---

## 🌍 Módulo de Rutas y Mapas

- Carga de rutas mineras desde JSON
- Visualización en Folium usando Google Maps Directions API
- Filtros dinámicos por departamento de origen y destino
- Marcadores personalizados (mina y transporte)

---

## ⏱️ Módulo de Sismos en Tiempo Real

- Consumo de API pública [USGS Earthquake API](https://earthquake.usgs.gov/)
- Filtros por magnitud mínima, región y tiempo
- Actualización automática cada 60 segundos
- Visualización en mapa geográfico y gráfico de barras
- Mensajes inteligentes cuando no hay datos válidos

---

## 📦 Docker (opcional)

```bash
docker build -t cooperativa-dashboard .
docker run -p 8050:8050 cooperativa-dashboard
```

---


---

## 🔑 Configuración de la API Key

Para que el módulo de **Rutas y Mapas** funcione correctamente, es necesario configurar una **clave de Google Maps API**.

1. Abre el archivo `utils/mapas.py`.
2. Ubica la línea donde se define la API Key, por ejemplo:

```python
API_KEY = "TU_API_KEY_AQUI"
```

3. Reemplaza `"TU_API_KEY_AQUI"` con tu propia clave generada desde [Google Cloud Console](https://console.cloud.google.com/).

> ⚠️ **Importante:** No compartas tu clave en repositorios públicos. Se recomienda usar un archivo `.env` o variables de entorno para mayor seguridad en entornos de producción.


## 🧠 Créditos

Este proyecto fue desarrollado como parte del curso de Ciencia de Datos aplicado a una cooperativa minera. Incluye módulos para análisis financiero, visualización de rutas y eventos sísmicos en tiempo real, utilizando Dash, Plotly y APIs públicas.
