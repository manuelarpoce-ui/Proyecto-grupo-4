# ============================================================
# 0. ENTRENA EL MODELO FINAL Y LO GUARDA EN LA CARPETA models/
# ============================================================
# Ejecutar desde la carpeta del proyecto con:
#     uv run python -m grupo_4.guardar_modelo

from pathlib import Path

import joblib

from grupo_4.limpieza import ejecutar_limpieza
from grupo_4.entrenamiento import ejecutar_entrenamiento


# ============================================================
# 1. RUTAS Y PARÁMETROS
# ============================================================

RUTA_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_MODELO = RUTA_PROYECTO / "models" / "modelo_logistico.joblib"

# Umbral de clasificación acordado por el equipo (ajustar según el notebook 05)
UMBRAL = 0.20


# ============================================================
# 2. ENTRENAR Y GUARDAR
# ============================================================

def guardar_modelo(umbral=UMBRAL, ruta=RUTA_MODELO):
    """
    Entrena la regresión logística con el mismo proceso de los notebooks
    y guarda en un solo archivo el modelo, el umbral y el orden de las variables.
    """

    df = ejecutar_limpieza()
    resultado = ejecutar_entrenamiento(df)

    nombre_logistico = next(n for n in resultado["modelos"] if "log" in n.lower())
    modelo = resultado["modelos"][nombre_logistico]

    paquete = {
        "modelo": modelo,
        "umbral": umbral,
        "variables": list(resultado["X_train"].columns),
    }

    ruta.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(paquete, ruta)

    print(f"Modelo guardado en: {ruta}")
    print(f"Umbral: {umbral} | Variables: {len(paquete['variables'])}")
    return ruta


if __name__ == "__main__":
    guardar_modelo()
