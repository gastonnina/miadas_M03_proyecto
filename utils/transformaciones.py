# utils/transformaciones.py

import pandas as pd


def cargar_dataset_completo():
    df_clientes = pd.read_feather("_data/clientes.feather")
    df_cuentas = pd.read_feather("_data/cuentas.feather")
    df_movimientos = pd.read_feather("_data/movimientos.feather")
    df_departamentos = pd.read_feather("_data/departamentos.feather")
    df_profesiones = pd.read_feather("_data/profesiones.feather")

    df_departamentos = df_departamentos.rename(columns={"DESCRIPCION": "DEPARTAMENTO"})
    df_profesiones = df_profesiones.rename(columns={"DESCRIPCION": "PROFESION"})

    df = df_movimientos.merge(df_cuentas, on="CUENTA")
    df = df.merge(df_clientes, on="CARNET")
    df = df.merge(df_departamentos, on="CODEPTO")
    df = df.merge(df_profesiones, on="CODPROF")
    df["FECHA"] = pd.to_datetime(df["FECHA"], dayfirst=True)
    df["ANIO"] = df["FECHA"].dt.year

    return df
