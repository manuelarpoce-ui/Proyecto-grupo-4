# Diseño del pipeline (módulo 07)

El pipeline une el preprocesamiento y el modelo en un solo objeto, de modo que
las mismas transformaciones se aplican al entrenar y al predecir.

```
Pipeline
├── preprocesamiento (ColumnTransformer)
│   ├── numéricas (14):   LIMIT_BAL, AGE, BILL_AMT1-6, PAY_AMT1-6
│   │                     → imputar con la mediana → estandarizar (StandardScaler)
│   ├── categóricas (9):  SEX, EDUCATION, MARRIAGE, PAY_0, PAY_2-6
│   │                     → imputar con la categoría más frecuente → OneHotEncoder
│   └── ordinales:        ninguna (ver decisiones)
└── modelo: regresión logística (modelo final)
```

## Datos de entrada
- Base limpia generada por `src/limpieza.py` (`data/processed/datos_limpios.csv`).
- Variable objetivo: `default payment next month`. Se excluye la columna `ID`.

## División de los datos
- 80 % entrenamiento y 20 % prueba, estratificada por la variable objetivo para
  conservar la proporción de clientes que incumplen (≈ 22 %).
- Semilla fija `random_state=42` para que el resultado sea reproducible.

## Modelos comparados
| Modelo | Configuración |
|---|---|
| Baseline | Predice siempre la clase mayoritaria (no incumple) |
| Regresión logística | `max_iter=1000`, `random_state=42` |
| Árbol de decisión | `max_depth=5`, `random_state=42` |

Los tres comparten el mismo preprocesamiento. El modelo final es la regresión
logística, con umbral de decisión de 0,20 (elegido en validación, ver
`docs/05_modelado.md`).

## Decisiones de diseño
- **Las variables `PAY_*` se tratan como categóricas**, no como ordinales. Así el
  modelo no supone que la distancia entre "retraso de 1 mes" y "retraso de 2
  meses" es la misma en toda la escala, pero se pierde el orden entre categorías.
- **`OneHotEncoder(handle_unknown="ignore")`**: si en producción llega una
  categoría que no se vio al entrenar, no falla.
- **Imputación**: la base no tiene valores faltantes, pero el pipeline la incluye
  para que no falle con datos nuevos.
- **Todo dentro del `Pipeline`**: el escalado y la codificación se ajustan solo con
  los datos de entrenamiento, para evitar fuga de información (*leakage*).

## Cómo entrenar
```bash
uv run python -m src.train
```
Entrena los tres modelos y guarda el modelo final en `models/modelo_logistico.joblib`
(esa carpeta no se sube a GitHub).

## Cómo se usa después
La API (`api/main.py`) carga ese archivo, aplica el mismo preprocesamiento y
devuelve la probabilidad de incumplimiento y la banda de riesgo.