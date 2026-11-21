# Project Charter: Predicción del incumplimiento de pagos en tarjetas de crédito

**Equipo:** Manuela Restrepo, Andrea Paez, Julian Olaya, Ana Maria Montealegre · **Fecha:** 2026-11-21 · **Versión:** 1.0 (actualizada con los resultados del modelado)

## 1. Contexto y problema de negocio

Las entidades financieras asumen el riesgo de que algunos clientes de tarjeta de crédito no paguen sus obligaciones. Hoy la gestión de cobranza es reactiva: se actúa cuando el cliente ya entró en mora. En la base analizada, **el 22,1 % de los clientes incumple el mes siguiente**. Cada incumplimiento no detectado implica perder una parte del saldo adeudado, y restringir sin criterio a buenos clientes implica perder ingresos. Con los supuestos de trabajo (LGD 60 %, margen 10 %), el costo de no usar ningún modelo sobre 6.000 clientes se estima en **NT$ 40,4 millones**.

## 2. Objetivo

| Nivel | Descripción |
|---|---|
| **Negocio** | Reducir la pérdida esperada por incumplimiento, priorizando la gestión preventiva en los clientes de mayor riesgo |
| **Ciencia de datos** | Estimar la probabilidad de que un cliente incumpla el pago de su tarjeta el próximo mes y clasificarlo en bandas de riesgo |
| **Tipo de problema** | Clasificación binaria (con clases desbalanceadas: 77,9 % / 22,1 %) |
| **Variable objetivo** | `default payment next month` |

## 3. Criterios de éxito

| Tipo | Métrica | Umbral | Resultado obtenido |
|---|---|---|---|
| Negocio (KPI) | Reducción de la pérdida esperada frente a no usar modelo | ≥ 40 % | 53,3 % (política de menor costo, notebook 05) |
| Modelo | Recall de la clase "incumple" en prueba | ≥ 0,55 | 0,587 (umbral 0,20) |
| Modelo | ROC-AUC en prueba | ≥ 0,75 | 0,758 |
| *Baseline* a superar | Predecir siempre "no incumple" (clase mayoritaria) | Accuracy 0,779 · Recall 0 · F1 0 | Superado: F1 0,511 frente a 0 |

## 4. Datos

| Fuente | Descripción | Filas × columnas | Acceso |
|---|---|---|---|
| [UCI – Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) | Perfil, cupo, estado de pago, facturación y pagos de clientes de Taiwán (abril a septiembre de 2005) | 30.000 × 25 | Público; archivo incluido en `data/raw/` |

**¿Qué representa una fila?** Un cliente de tarjeta de crédito, con seis meses de historial.

## 5. Alcance

- **Incluye:** limpieza y validación de los datos, EDA con hipótesis, modelos de clasificación (*baseline*, regresión logística y árbol de decisión), ajuste del umbral por F1 y por costo, bandas de riesgo y una API con formulario web para consultar a un cliente.
- **No incluye:** despliegue en producción, integración con los sistemas de la entidad, datos de recuperación reales ni rentabilidad por cliente, ni monitoreo automático del modelo.

## 6. Riesgos y supuestos

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Clases desbalanceadas (22,1 % incumple) | Alta | Alto | Evaluar con recall, F1 y ROC-AUC, no solo con accuracy; ajustar el umbral de decisión |
| Fuga de información (*data leakage*) | Media | Alto | División estratificada entrenamiento/prueba (80/20, `random_state=42`); el preprocesamiento va dentro del `Pipeline` y solo aprende con entrenamiento; el umbral se elige en validación |
| Códigos no documentados (`EDUCATION` 0, 5, 6; `MARRIAGE` 0; `PAY_x` -2 y 0) | Alta | Medio | Agruparlos en "otros" o conservarlos como categoría; documentado en `03_decisiones_limpieza.md` |
| Supuestos financieros no validados (LGD, margen) | Alta | Medio | Análisis de sensibilidad (notebook 05); validar con el área financiera antes de fijar el umbral |
| Datos antiguos y de otro país (Taiwán, 2005) | Alta | Medio | Usar el modelo como apoyo, no como decisión automática; reentrenar con datos propios |
| Uso de atributos sensibles (sexo, estado civil) | Media | Medio | Discutir su exclusión y revisar las métricas por grupo antes de usar el modelo |

## 7. Plan (cronograma del curso)

| Semana | Fase CRISP-DM | Entregable | Estado |
|---|---|---|---|
| 1 | Negocio + Datos | Charter, problema y KPIs, perfil inicial | ✅ |
| 2 | Preparación + EDA | `src/grupo_4/limpieza.py`, `notebooks/01_eda.ipynb` | ✅ |
| 3 | Modelado | *Baseline*, regresión logística, árbol y `Pipeline` | ✅ |
| 4 | Evaluación + Despliegue | Ajuste del umbral, impacto en el negocio, API y presentación | ✅ (presentación en preparación) |

## 8. Stakeholders

| Persona/rol | Interés | Cómo se le comunica |
|---|---|---|
| Gerencia de riesgo crediticio | Reducir la pérdida por incumplimiento y definir la política de cupos | Informe de resultados e indicadores de pérdida esperada |
| Equipo de cobranza | Saber a qué clientes contactar primero | Bandas de riesgo con la acción sugerida (formulario/API) |
| Área financiera | Validar los supuestos de LGD y margen | Análisis de sensibilidad del umbral |
| Docente del curso | Evaluar el proyecto | Repositorio en GitHub y presentación |
