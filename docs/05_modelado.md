# Modelado (módulo 06)

Código: [`src/grupo_4/entrenamiento.py`](../src/grupo_4/entrenamiento.py), [`src/grupo_4/preprocesamiento.py`](../src/grupo_4/preprocesamiento.py) y [`src/grupo_4/evaluacion.py`](../src/grupo_4/evaluacion.py). Notebooks: `03_modelamiento`, `04_evaluacion` y `05_impacto_negocio`.

## Tipo de problema y métrica principal (y por qué)

- **Clasificación binaria** con clases desbalanceadas (22,1 % incumple).
- **Métrica principal: recall de la clase "incumple"**, acompañada del **F1-score** para no disparar las falsas alarmas. Para la entidad, un falso negativo (no detectar a quien va a incumplir) cuesta mucho más que un falso positivo: con los supuestos de trabajo, el falso negativo cuesta el 60 % del saldo (LGD) y el falso positivo el 10 % (margen perdido).
- **ROC-AUC** como métrica complementaria, porque mide qué tan bien ordena el modelo a los clientes por riesgo, que es lo que usan las bandas.
- El **accuracy no sirve como métrica principal**: el *baseline* que siempre dice "no incumple" ya obtiene 77,9 %.

## Comparación (baseline vs. modelos)

División estratificada: 80 % entrenamiento (24.000) y 20 % prueba (6.000), con `random_state=42`. Los tres modelos usan el mismo `Pipeline` de preprocesamiento.

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| *Baseline* (`DummyClassifier`, clase mayoritaria) | 0,7788 | 0,0000 | 0,0000 | 0,0000 | — |
| Regresión logística (umbral 0,50) | 0,8168 | 0,6619 | 0,3512 | 0,4589 | 0,7580 |
| Árbol de decisión (umbral 0,50) | 0,8165 | 0,6794 | 0,3225 | 0,4374 | 0,7402 |
| **Regresión logística (umbral 0,20)** | 0,7515 | 0,4524 | **0,5870** | **0,5110** | 0,7580 |

## Modelo elegido y justificación

**Regresión logística con umbral de decisión 0,20.**

- Supera al *baseline* y al árbol en recall, F1 y ROC-AUC.
- Es interpretable: se puede explicar al área de riesgo qué variables suben o bajan la probabilidad.
- Bajar el umbral de 0,50 a 0,20 sube el recall de 35 % a 59 % (detecta 779 de 1.327 incumplidos en prueba), a cambio de más falsas alarmas.
- El umbral 0,20 se eligió por el mejor F1 en validación (notebook 04). El notebook 05 muestra que, si se minimiza el costo con LGD 60 % y margen 10 %, el umbral óptimo es cercano a 0,15, y que se mueve entre 0,02 y 0,33 según los supuestos. **La API usa 0,20**, y el umbral definitivo se debe fijar con el área financiera.
- Las probabilidades se agrupan en bandas: **Bajo** (< 0,20), **Medio** (0,20–0,50) y **Alto** (≥ 0,50), cada una con una acción sugerida.

## Métrica en test (una sola vez)

Con el umbral 0,20, sobre los 6.000 clientes de prueba:

| Métrica | Valor |
|---|---:|
| Recall | 58,70 % |
| Precision | 45,24 % |
| F1-score | 0,511 |
| Accuracy | 75,15 % |
| ROC-AUC | 0,758 |

Matriz de confusión: 779 verdaderos positivos, 548 falsos negativos, 943 falsos positivos y 3.730 verdaderos negativos.

Impacto en el negocio (notebook 05): la política de menor costo reduce la pérdida estimada en un **53,3 %** frente a no usar modelo. Las bandas media y alta reúnen el **58,7 % de los incumplidos revisando solo el 28,7 % de la cartera**.

## Análisis de errores y límites

- **Falsos negativos (548):** clientes que incumplieron con probabilidad baja; el 98 % no tenía retraso en septiembre (`PAY_0` ≤ 0), así que su historial no daba señales. Es el error más costoso; por eso se bajó el umbral.
- **Falsos positivos (943):** clientes marcados como riesgosos que finalmente pagaron; el 64 % tenía al menos un mes de retraso en septiembre. Son el costo de detectar más incumplidos y se mitigan usando el modelo para priorizar, no para rechazar.
- **Sin sobreajuste:** el F1 es de 53,2 % en entrenamiento y 51,1 % en prueba.
- **Límites:**
  - Los datos son de Taiwán en 2005: el comportamiento de pago cambia con el país y el ciclo económico, así que hay que reentrenar con datos propios.
  - Los costos (LGD y margen) son supuestos, no datos reales de recuperación.
  - El modelo usa atributos sensibles (sexo, estado civil); falta revisar las métricas por grupo.
  - No se usaron validación cruzada ni búsqueda de hiperparámetros; tampoco se incluyeron las variables derivadas del EDA.
  - El modelo es una **herramienta de apoyo** y no debe ser el único criterio para decidir sobre un cliente.
