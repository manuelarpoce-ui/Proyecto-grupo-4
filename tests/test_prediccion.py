"""Pruebas de las reglas de negocio de grupo_4.prediccion (no necesitan el modelo)."""

from grupo_4.prediccion import clasificar_banda, preparar_cliente


def test_bandas_de_riesgo():
    assert clasificar_banda(0.05)[0] == "Bajo"
    assert clasificar_banda(0.20)[0] == "Medio"
    assert clasificar_banda(0.49)[0] == "Medio"
    assert clasificar_banda(0.50)[0] == "Alto"
    assert clasificar_banda(0.95)[0] == "Alto"


def test_preparar_cliente_agrupa_codigos_no_documentados():
    for codigo in (0, 5, 6):
        assert preparar_cliente({"EDUCATION": codigo, "MARRIAGE": 1})["EDUCATION"] == 4
    assert preparar_cliente({"EDUCATION": 2, "MARRIAGE": 0})["MARRIAGE"] == 3


def test_preparar_cliente_no_modifica_el_original():
    original = {"EDUCATION": 5, "MARRIAGE": 0}
    preparar_cliente(original)
    assert original == {"EDUCATION": 5, "MARRIAGE": 0}
