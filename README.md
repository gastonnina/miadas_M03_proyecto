<!-- omit in toc -->
# Proyecto: MODELAMIENTO Y VISUALIZACIÓN DE LA INFORMACIÓN EN "R" 🕷️📊

Este proyecto tiene como objetivo extraer datos de fuentes distintas en línea: portales de noticias nacional y tiendas digitales.

📄 **Resultados generados:** Se pueden ver localmente en el `index.html` o en línea aquí: [🌐 Proyecto en GitHub Pages](https://gastonnina.github.io/miadas_M03_proyecto)

<!-- omit in toc -->
## 🗂️ Tabla de Contenidos

- [🛠️ Requisitos](#️-requisitos)
- [⚙️ Instalación](#️-instalación)
- [📁 Estructura de Archivos](#-estructura-de-archivos)
- [🚀 Ejecución](#-ejecución)
- [📊 Resultados](#-resultados)


## 🛠️ Requisitos

- **R** (≥ 4.0.0): [📥 Descargar R](https://cran.r-project.org/)
- **RStudio** (opcional, pero recomendado): [📥 Descargar RStudio](https://posit.co/download/rstudio-desktop/)

- **Librerías de R:** `httr`, `rvest`, `dplyr`, `jsonlite`, `wbstats`

## ⚙️ Instalación

1. Clonar el repositorio 🧑‍💻:

   ```bash
   git clone https://github.com/gastonnina/miadas_M03_proyecto.git
   cd miadas_M03_proyecto
   ```

2. Instalar librerías en R 📦:

   ```r
   install.packages(c("dplyr", "stringr"))
   ```

## 📁 Estructura de Archivos

```

├── README.md                    # 📄 Archivo con instrucciones del proyecto
├── index.Rmd                    # 🔢 Código principal en R Markdown
├── _fig/                        # 🖼️ graficas auxiliares del proyecto
├── _data/                       # 📂 Resultados guardados
│   └── datos_consolidado.RData  # 💾 Base de datos consolidada
```

## 🚀 Ejecución

1. Abre `index.Rmd` en RStudio. 🖥️
2. Ejecuta las siguientes secciones del archivo en orden correlativo: 🛠️

## 📊 Resultados

📁 **El archivo de datos consolidado se guardará en:**
`_data/datos_consolidado.RData`.

Este archivo contendrá información del proyecto **3500 registros**.

🔍 Los resultados generados se pueden ver localmente en el `index.html` o en línea aquí: [🌐 Proyecto en GitHub Pages](https://gastonnina.github.io/miadas_M03_proyecto)