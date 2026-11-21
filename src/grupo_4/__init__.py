"""Grupo 4: predicción del incumplimiento de pago en tarjetas de crédito."""


def main() -> None:
    print("Proyecto Grupo 4: predicción del incumplimiento de pago en tarjetas de crédito\n")
    print("Comandos principales:")
    print("  uv sync                                  # instalar dependencias")
    print("  uv run python -m grupo_4.guardar_modelo  # entrenar y guardar el modelo")
    print("  uv run uvicorn grupo_4.api:app --reload  # iniciar la API (http://127.0.0.1:8000/)")
    print("  uv run pytest                            # correr las pruebas")
