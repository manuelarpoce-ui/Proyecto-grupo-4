# ============================================================
# 0. CARGA, LIMPIA. VALIDA Y GUARDA BASE DE DATOS
# ============================================================

from pathlib import Path

import pandas as pd
import numpy as np


# ============================================================
# 1. DEFINIR LAS RUTAS DEL PROYECTO
# ============================================================

# Obtener la carpeta principal del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parents[2]

# Ruta de la base original
RUTA_BASE_ORIGINAL = (
    RUTA_PROYECTO
    / "data"
    / "raw"
    / "default of credit card clients.xls"
)

# Ruta donde se guardará la base limpia
RUTA_BASE_LIMPIA = (
    RUTA_PROYECTO
    / "data"
    / "processed"
    / "datos_limpios.csv"
)


# ============================================================
# 2. CARGAR LA BASE DE DATOS ORIGINAL
# ============================================================

def cargar_base(ruta_archivo=RUTA_BASE_ORIGINAL):

    """
    Carga la base original de clientes desde el archivo Excel.

    El parámetro header=1 indica que los encabezados
    se encuentran en la segunda fila del archivo.
    """

    df = pd.read_excel(ruta_archivo, header=1)

    return df


# ============================================================
# 3. LIMPIAR Y PREPARAR LOS DATOS
# ============================================================

def limpiar_base(df):

    """
    Realiza la limpieza inicial de la base de datos:

    - Convierte las columnas a valores numéricos.
    - Agrupa los códigos no especificados de EDUCATION.
    - Agrupa el código no especificado de MARRIAGE.

    Se conservan los demás valores originales.
    """

    # Convertir las columnas a sus tipos numéricos
    df = df.apply(pd.to_numeric, errors="coerce")

    # Agrupar los códigos 0, 5 y 6 de EDUCATION en la categoría 4
    df["EDUCATION"] = df["EDUCATION"].replace({
        0: 4,
        5: 4,
        6: 4
    })

    # Agrupar el código 0 de MARRIAGE en la categoría 3
    df["MARRIAGE"] = df["MARRIAGE"].replace({
        0: 3
    })

    return df


# ============================================================
# 4. VALIDAR LA BASE DE DATOS
# ============================================================

def validar_base(df):

    """
    Revisa las dimensiones de la base, los valores faltantes
    y los registros duplicados.
    """

    print("Dimensiones de la base:", df.shape)

    print("\nValores faltantes por columna:")
    print(df.isnull().sum())

    print("\nTotal de valores faltantes:", df.isnull().sum().sum())

    print("\nCantidad de ID duplicados:",
          df["ID"].duplicated().sum())

    print("\nCantidad de filas completamente duplicadas:",
          df.duplicated().sum())

    print("\nCantidad de filas duplicadas sin considerar ID:",
          df.drop(columns=["ID"]).duplicated().sum())


# ============================================================
# 5. GUARDAR LA BASE LIMPIA
# ============================================================

def guardar_base(df, ruta_salida=RUTA_BASE_LIMPIA):

    """
    Guarda la base limpia en formato CSV dentro de data/processed.
    """

    ruta_salida = Path(ruta_salida)

    # Crear la carpeta de destino si todavía no existe
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(ruta_salida, index=False)

    print("\nBase limpia guardada correctamente en:")
    print(ruta_salida)


# ============================================================
# 6. EJECUTAR EL PROCESO COMPLETO DE LIMPIEZA
# ============================================================

def ejecutar_limpieza():

    """
    Ejecuta en orden la carga, limpieza, validación
    y almacenamiento de la base de datos.
    """

    print("Cargando base de datos original...")

    df = cargar_base()

    print("\nEjecutando limpieza...")

    df = limpiar_base(df)

    print("\nValidando información...")

    validar_base(df)

    print("\nGuardando base limpia...")

    guardar_base(df)

    return df

if __name__ == "__main__":
    ejecutar_limpieza()