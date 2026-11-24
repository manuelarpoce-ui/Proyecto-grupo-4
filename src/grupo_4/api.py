# ============================================================
# 0. API PARA CONSULTAR EL RIESGO DE INCUMPLIMIENTO DE UN CLIENTE
# ============================================================
# Instalar dependencias (una sola vez):  uv add fastapi uvicorn
# Iniciar la API:                        uv run uvicorn grupo_4.api:app --reload
# Formulario para usuarios:              http://127.0.0.1:8000
# Vista técnica (desarrolladores):       http://127.0.0.1:8000/docs

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from grupo_4.prediccion import cargar_modelo, predecir_cliente


# ============================================================
# 1. DATOS QUE RECIBE LA API (UN CLIENTE)
# ============================================================

class Cliente(BaseModel):
    LIMIT_BAL: float = Field(..., gt=0, description="Límite de crédito (NT$)")
    SEX: int = Field(..., ge=1, le=2, description="1 = masculino, 2 = femenino")
    EDUCATION: int = Field(..., ge=0, le=6, description="1 = posgrado, 2 = universidad, 3 = secundaria, 4 = otros")
    MARRIAGE: int = Field(..., ge=0, le=3, description="1 = casado, 2 = soltero, 3 = otros")
    AGE: int = Field(..., ge=18, le=100, description="Edad en años")
    PAY_0: int = Field(..., ge=-2, le=9, description="Estado de pago septiembre (-1 = puntual, 1-9 = meses de retraso)")
    PAY_2: int = Field(..., ge=-2, le=9, description="Estado de pago agosto")
    PAY_3: int = Field(..., ge=-2, le=9, description="Estado de pago julio")
    PAY_4: int = Field(..., ge=-2, le=9, description="Estado de pago junio")
    PAY_5: int = Field(..., ge=-2, le=9, description="Estado de pago mayo")
    PAY_6: int = Field(..., ge=-2, le=9, description="Estado de pago abril")
    BILL_AMT1: float = Field(..., description="Monto facturado septiembre")
    BILL_AMT2: float = Field(..., description="Monto facturado agosto")
    BILL_AMT3: float = Field(..., description="Monto facturado julio")
    BILL_AMT4: float = Field(..., description="Monto facturado junio")
    BILL_AMT5: float = Field(..., description="Monto facturado mayo")
    BILL_AMT6: float = Field(..., description="Monto facturado abril")
    PAY_AMT1: float = Field(..., ge=0, description="Monto pagado septiembre")
    PAY_AMT2: float = Field(..., ge=0, description="Monto pagado agosto")
    PAY_AMT3: float = Field(..., ge=0, description="Monto pagado julio")
    PAY_AMT4: float = Field(..., ge=0, description="Monto pagado junio")
    PAY_AMT5: float = Field(..., ge=0, description="Monto pagado mayo")
    PAY_AMT6: float = Field(..., ge=0, description="Monto pagado abril")

    model_config = {
        "json_schema_extra": {
            "example": {
                "LIMIT_BAL": 50000, "SEX": 2, "EDUCATION": 2, "MARRIAGE": 1, "AGE": 35,
                "PAY_0": 2, "PAY_2": 2, "PAY_3": 0, "PAY_4": 0, "PAY_5": 0, "PAY_6": 0,
                "BILL_AMT1": 48000, "BILL_AMT2": 47000, "BILL_AMT3": 45000,
                "BILL_AMT4": 40000, "BILL_AMT5": 38000, "BILL_AMT6": 36000,
                "PAY_AMT1": 0, "PAY_AMT2": 1500, "PAY_AMT3": 1800,
                "PAY_AMT4": 1500, "PAY_AMT5": 1400, "PAY_AMT6": 1300,
            }
        }
    }


# ============================================================
# 2. CREAR LA API Y CARGAR EL MODELO
# ============================================================

app = FastAPI(
    title="API de riesgo de incumplimiento - Grupo 4",
    description="Predice la probabilidad de que un cliente incumpla el pago de su tarjeta de crédito el próximo mes.",
    version="1.0",
)

paquete = cargar_modelo()

RUTA_FORMULARIO = Path(__file__).resolve().parent / "formulario.html"


# ============================================================
# 3. RUTAS (ENDPOINTS)
# ============================================================

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def formulario():
    """Página con el formulario para consultar el riesgo de un cliente."""
    return RUTA_FORMULARIO.read_text(encoding="utf-8")


@app.get("/estado")
@app.get("/health")
def estado():
    """Verifica que la API esté funcionando."""
    return {"estado": "ok", "modelo": "Regresión logística", "umbral": paquete["umbral"]}


@app.post("/predecir")
@app.post("/predict")
def predecir(cliente: Cliente):
    """Recibe los datos de un cliente y devuelve su nivel de riesgo."""
    try:
        return predecir_cliente(cliente.model_dump(), paquete)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))
