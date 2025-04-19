import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker('es_ES')
np.random.seed(123)
random.seed(123)

# --- Departamentos
departamentos = [
    "CHUQUISACA", "LA PAZ", "COCHABAMBA", "ORURO", "POTOSI",
    "TARIJA", "SANTA CRUZ", "BENI", "PANDO"
]
df_departamentos = pd.DataFrame({
    "CODEPTO": range(1, 10),
    "DESCRIPCION": departamentos
})

# --- Profesiones
profesiones = [
    "ABOGADO", "ADMINISTRADOR", "CONTADOR", "ENFERMERA", "MINERO",
    "INGENIERO DE MINAS", "GEÓLOGO", "MECÁNICO", "ELECTRICISTA"
]
df_profesiones = pd.DataFrame({
    "CODPROF": range(1, 10),
    "DESCRIPCION": profesiones
})

# --- Clientes
n_clientes = 15000
carnets = np.random.choice(range(2000000, 6000000), n_clientes, replace=False)

# Pesos para desbalancear departamentos (SANTA CRUZ tendrá más, PANDO menos)
pesos_deptos = [
    0.04,  # CHUQUISACA
    0.22,  # LA PAZ       ← más clientes
    0.06,  # COCHABAMBA
    0.18,  # ORURO        ← más clientes
    0.25,  # POTOSÍ       ← más clientes
    0.04,  # TARIJA
    0.10,  # SANTA CRUZ
    0.06,  # BENI
    0.05   # PANDO
]

df_clientes = pd.DataFrame({
    "CARNET": carnets,
    "NOMBRES": [fake.name() for _ in range(n_clientes)],
    "CODPROF": np.random.choice(df_profesiones["CODPROF"], n_clientes),
    "CODEPTO": np.random.choice(df_departamentos["CODEPTO"], n_clientes, p=pesos_deptos),
    "GENERO": np.random.choice(["M", "F"], n_clientes),
    "FECHA_INGRESO": pd.to_datetime(np.random.choice(pd.date_range("2000-01-01", "2022-12-31"), n_clientes)),
    "TIPO_SOCIO": np.random.choice(["ACTIVO", "PASIVO", "JUBILADO"], n_clientes),
    "NRO_SOCIO": [f"SOC{str(i).zfill(5)}" for i in range(1, n_clientes + 1)],
    "ESTADO_CIVIL": np.random.choice(["SOLTERO", "CASADO", "DIVORCIADO", "VIUDO"], n_clientes),
    "TELEFONO": [fake.phone_number() for _ in range(n_clientes)],
    "EMAIL": [fake.email() for _ in range(n_clientes)],
    "ZONA_RESIDENCIA": np.random.choice(["CENTRO", "SUR", "NORTE", "VILLA", "RURAL"], n_clientes)
})

# --- Cuentas
def gen_cuenta():
    return f"{random.randint(1,9)}-{random.randint(100,109)}-{random.randint(10000,99999)}-{random.randint(1,9)}"

df_cuentas = pd.DataFrame({
    "CUENTA": [gen_cuenta() for _ in range(n_clientes)],
    "CARNET": df_clientes["CARNET"],
    "FAPERTURA": pd.to_datetime(np.random.choice(pd.date_range("2000-01-01", "2023-12-31"), n_clientes)),
    "TIPO_CUENTA": np.random.choice(["AHORRO", "APORTE", "CRÉDITO"], n_clientes),
    "ESTADO_CUENTA": np.random.choice(["ACTIVA", "INACTIVA", "CERRADA"], n_clientes),
    "SALDO_ACTUAL": np.round(np.random.uniform(0, 100000, n_clientes), 2),
    "PLAZO_MESES": np.random.choice([0, 6, 12, 24, 36], n_clientes),
    "TASA_INTERES": np.round(np.random.uniform(0.01, 0.12, n_clientes), 3),
    "FECHA_CIERRE": pd.NaT  # puede llenarse condicionalmente luego
})

# --- Movimientos
n_movs = 350000
cuentas_sample = np.random.choice(df_cuentas["CUENTA"], n_movs)

df_movimientos = pd.DataFrame({
    "CUENTA": cuentas_sample,
    "MONTO": np.round(np.random.uniform(10, 5000, n_movs), 2),
    "FECHA": pd.to_datetime(np.random.choice(pd.date_range("2022-01-01", "2025-04-01"), n_movs)),
    "TIPO_MOVIMIENTO": np.random.choice(["DEPÓSITO", "RETIRO", "PAGO", "TRANSFERENCIA"], n_movs),
    "CANAL": np.random.choice(["CAJA", "APP", "WEB", "CAJERO", "TRANSFERENCIA"], n_movs),
    "USUARIO_REGISTRO": [f"USR{random.randint(1001,1050)}" for _ in range(n_movs)],
    "FECHA_REGISTRO": pd.to_datetime(np.random.choice(pd.date_range("2022-01-01", "2025-04-01", freq='h'), n_movs)),
    "OBSERVACION": np.random.choice(["OK", "Sin observaciones", "Revisado", "Validado"], n_movs)
})

# --- (Opcional) Guardar a CSV
df_clientes.to_csv("_data/clientes.csv", index=False)
df_cuentas.to_csv("_data/cuentas.csv", index=False)
df_movimientos.to_csv("_data/movimientos.csv", index=False)
df_departamentos.to_csv("_data/departamentos.csv", index=False)
df_profesiones.to_csv("_data/profesiones.csv", index=False)
print("Todos los archivos fueron guardados en formato CSV.")

df_clientes.to_feather("_data/clientes.feather")
df_cuentas.to_feather("_data/cuentas.feather")
df_movimientos.to_feather("_data/movimientos.feather")
df_departamentos.to_feather("_data/departamentos.feather")
df_profesiones.to_feather("_data/profesiones.feather")

print("Todos los archivos fueron guardados en formato Feather.")