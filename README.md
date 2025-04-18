# 📊 Dashboard Interactivo en Tiempo Real – Cooperativa Minera ⛏️

## 🎯 Objetivo General
Desarrollar un dashboard interactivo para visualizar y analizar datos financieros de una **cooperativa minera**, con filtros dinámicos y métricas clave.

---

## 👥 Integrantes

- Paolo Ramos Mendez  
- Gaston Nina Sossa  

---

## 🗂️ Estructura del Proyecto

```
.
├── dashboard.py                  # Aplicación principal Dash
├── _data/
│   ├── clientes.csv              # Datos de clientes
│   ├── cuentas.csv               # Datos de cuentas
│   ├── movimientos.csv           # Movimientos financieros
│   ├── departamentos.csv         # Catálogo de departamentos
│   ├── profesiones.csv           # Catálogo de profesiones
│   ├── clientes.feather          # Versión Feather de los datos
│   ├── cuentas.feather
│   ├── movimientos.feather
│   ├── departamentos.feather
│   └── profesiones.feather
├── Dockerfile                    # Imagen para despliegue en contenedor
├── pyproject.toml                # Archivo de configuración PDM
├── .gitignore                    # Archivos ignorados por Git
└── README.md                     # Este archivo
```

---

## ⚙️ Requisitos

- Python ≥ 3.9
- PDM (gestor de dependencias recomendado) → https://pdm.fming.dev/

Librerías principales:

- `pandas`
- `dash`
- `plotly`
- `pyarrow`
- `faker`
- `numpy`

---

## 📦 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/usuario/cooperativa-dashboard.git
cd cooperativa-dashboard
```

2. Instalar dependencias con [PDM](https://pdm.fming.dev/):

```bash
pdm install
```

---

## 🚀 Ejecución

```bash
pdm run app.py
```

Esto abrirá una instancia local del dashboard en:  
📍 `http://127.0.0.1:8050`

---

## 🧪 Datos

Los datos provienen de archivos `.csv` y `.feather` ubicados en la carpeta `_data`. Para optimizar el rendimiento, el script utiliza archivos en formato **Feather**.

Si solo tienes los `.csv`, puedes convertirlos a `.feather` con este ejemplo:

```python
import pandas as pd
df = pd.read_csv("_data/clientes.csv", sep=";")
df.to_feather("_data/clientes.feather")
```

---

## 📊 Funcionalidades del Dashboard

- Filtros por departamento, año, profesión, cliente y rango de montos
- Indicadores clave (total movimientos, monto promedio, cuentas activas, etc.)
- Visualizaciones en pestañas:
  - Por ubicación geográfica
  - Por tiempo
  - Por cliente

---

## 📦 Docker (opcional)

Si deseas ejecutar en contenedor:

```bash
docker build -t cooperativa-dashboard .
docker run -p 8050:8050 cooperativa-dashboard
```

---

## 🧠 Créditos

Este proyecto fue desarrollado como parte del curso de Ciencia de Datos para apoyar el análisis de datos simulados de una cooperativa minera.