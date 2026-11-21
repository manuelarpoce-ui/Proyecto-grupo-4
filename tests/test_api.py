"""Pruebas de la API de riesgo de incumplimiento.

Ejecutar con:  uv run pytest
"""


def test_formulario_responde(cliente_api):
    respuesta = cliente_api.get("/")
    assert respuesta.status_code == 200
    assert "text/html" in respuesta.headers["content-type"]


def test_estado_ok(cliente_api):
    respuesta = cliente_api.get("/estado")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["estado"] == "ok"
    assert 0 < datos["umbral"] < 1


def test_predecir_devuelve_estructura_completa(cliente_api, cliente_riesgoso):
    respuesta = cliente_api.post("/predecir", json=cliente_riesgoso)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert set(datos) == {
        "probabilidad_incumplimiento", "umbral", "prediccion",
        "interpretacion", "banda_riesgo", "accion_sugerida",
    }
    assert 0 <= datos["probabilidad_incumplimiento"] <= 1
    assert datos["prediccion"] in (0, 1)
    assert datos["banda_riesgo"] in ("Bajo", "Medio", "Alto")


def test_cliente_riesgoso_tiene_mas_riesgo_que_cliente_cumplido(
    cliente_api, cliente_riesgoso, cliente_cumplido
):
    p_riesgoso = cliente_api.post("/predecir", json=cliente_riesgoso).json()
    p_cumplido = cliente_api.post("/predecir", json=cliente_cumplido).json()
    assert p_riesgoso["probabilidad_incumplimiento"] > p_cumplido["probabilidad_incumplimiento"]
    assert p_riesgoso["prediccion"] == 1
    assert p_cumplido["prediccion"] == 0


def test_codigos_no_documentados_se_aceptan(cliente_api, cliente_cumplido):
    """EDUCATION 0, 5, 6 y MARRIAGE 0 se agrupan en 'otros', igual que en la limpieza."""
    cliente_cumplido.update({"EDUCATION": 5, "MARRIAGE": 0})
    respuesta = cliente_api.post("/predecir", json=cliente_cumplido)
    assert respuesta.status_code == 200


def test_falta_una_variable_devuelve_422(cliente_api, cliente_riesgoso):
    del cliente_riesgoso["PAY_0"]
    respuesta = cliente_api.post("/predecir", json=cliente_riesgoso)
    assert respuesta.status_code == 422


def test_valor_fuera_de_rango_devuelve_422(cliente_api, cliente_riesgoso):
    cliente_riesgoso["AGE"] = 10
    respuesta = cliente_api.post("/predecir", json=cliente_riesgoso)
    assert respuesta.status_code == 422
