"""Configuración compartida de las pruebas.

La API carga el modelo desde models/modelo_logistico.joblib al importarse.
Si el modelo todavía no existe (por ejemplo, en un clon nuevo), se entrena
y se guarda antes de correr las pruebas.
"""

import pytest
from fastapi.testclient import TestClient

from grupo_4.prediccion import RUTA_MODELO


def _asegurar_modelo():
    if not RUTA_MODELO.exists():
        from grupo_4.guardar_modelo import guardar_modelo

        guardar_modelo()


@pytest.fixture(scope="session")
def cliente_api():
    _asegurar_modelo()
    from grupo_4.api import app

    return TestClient(app)


@pytest.fixture
def cliente_riesgoso():
    """Cliente con dos meses de retraso reciente y casi sin pagos."""
    return {
        "LIMIT_BAL": 50000, "SEX": 2, "EDUCATION": 2, "MARRIAGE": 1, "AGE": 35,
        "PAY_0": 2, "PAY_2": 2, "PAY_3": 0, "PAY_4": 0, "PAY_5": 0, "PAY_6": 0,
        "BILL_AMT1": 48000, "BILL_AMT2": 47000, "BILL_AMT3": 45000,
        "BILL_AMT4": 40000, "BILL_AMT5": 38000, "BILL_AMT6": 36000,
        "PAY_AMT1": 0, "PAY_AMT2": 1500, "PAY_AMT3": 1800,
        "PAY_AMT4": 1500, "PAY_AMT5": 1400, "PAY_AMT6": 1300,
    }


@pytest.fixture
def cliente_cumplido():
    """Cliente con cupo alto, pagos puntuales y pagos completos."""
    return {
        "LIMIT_BAL": 500000, "SEX": 2, "EDUCATION": 1, "MARRIAGE": 2, "AGE": 34,
        "PAY_0": -1, "PAY_2": -1, "PAY_3": -1, "PAY_4": -1, "PAY_5": -1, "PAY_6": -1,
        "BILL_AMT1": 5000, "BILL_AMT2": 4000, "BILL_AMT3": 6000,
        "BILL_AMT4": 3000, "BILL_AMT5": 4500, "BILL_AMT6": 5000,
        "PAY_AMT1": 4000, "PAY_AMT2": 6000, "PAY_AMT3": 3000,
        "PAY_AMT4": 4500, "PAY_AMT5": 5000, "PAY_AMT6": 5000,
    }
