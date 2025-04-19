# utils/data_loader.py

import json

def cargar_rutas_desde_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
