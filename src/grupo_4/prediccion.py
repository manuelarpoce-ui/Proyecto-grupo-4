# ============================================================
# 0. CARGA EL MODELO GUARDADO Y CALCULA EL RIESGO DE UN CLIENTE
# ============================================================
# Este módulo no depende de la API: se puede usar desde un notebook
# o desde cualquier otro programa.

from pathlib import Path

import joblib
import pandas as pd


RUTA_MODELO = Path(__file__).resolve().parents[2] / "models" / "modelo_logistico.joblib"


# ============================================================
# 1. CARGAR EL MODELO
# ============================================================

def cargar_modelo(ruta=RUTA_MODELO):
    """Carga el archivo creado por guardar_modelo.py."""
    if not Path(ruta).exists():
        raise FileNotFoundError(
            f"No se encontró el modelo en {ruta}. "
            "Ejecute primero: uv run python -m grupo_4.guardar_modelo"
        )
    return joblib.load(ruta)


# ============================================================
# 2. APLICAR LA MISMA LIMPIEZA DE LOS NOTEBOOKS
# ============================================================

def preparar_cliente(datos):
    """
    Recibe los datos de un cliente (diccionario) y aplica las mismas
    reglas de limpieza usadas en el entrenamiento.
    """
    datos = dict(datos)
    if datos.get("EDUCATION") in (0, 5, 6):   # códigos no documentados -> "otros"
        datos["EDUCATION"] = 4
    if datos.get("MARRIAGE") == 0:            # código no documentado -> "otros"
        datos["MARRIAGE"] = 3
    return datos


# ============================================================
# 3. CLASIFICAR EN BANDAS DE RIESGO
# ============================================================

def clasificar_banda(probabilidad):
    """Bandas definidas en el notebook 05."""
    if probabilidad < 0.20:
        return "Bajo", "Mantener condiciones; candidato a aumento de cupo"
    if probabilidad < 0.50:
        return "Medio", "Seguimiento y recordatorios de pago; no aumentar cupo"
    return "Alto", "Gestión preventiva de cobranza; revisar o congelar cupo"


# ============================================================
# 4. PREDECIR EL RIESGO DE UN CLIENTE
# ============================================================

def predecir_cliente(datos, paquete):
    """
    Devuelve la probabilidad de incumplimiento, la predicción según
    el umbral acordado y la banda de riesgo con su acción sugerida.
    """
    datos = preparar_cliente(datos)
    faltantes = [v for v in paquete["variables"] if v not in datos]
    if faltantes:
        raise ValueError(f"Faltan variables: {faltantes}")

    X = pd.DataFrame([datos])[paquete["variables"]]
    probabilidad = float(paquete["modelo"].predict_proba(X)[0, 1])
    banda, accion = clasificar_banda(probabilidad)

    return {
        "probabilidad_incumplimiento": round(probabilidad, 4),
        "umbral": paquete["umbral"],
        "prediccion": int(probabilidad >= paquete["umbral"]),
        "interpretacion": "Posible incumplimiento" if probabilidad >= paquete["umbral"] else "Sin alerta de incumplimiento",
        "banda_riesgo": banda,
        "accion_sugerida": accion,
    }
