# Problema y KPIs (módulo 02)

## Tema

Predicción del incumplimiento de pago de clientes de tarjetas de crédito, como apoyo a la gestión del riesgo crediticio de una entidad financiera.

## Dataset

| Aspecto | Detalle |
|---|---|
| Nombre | *Default of Credit Card Clients* |
| Fuente | UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients |
| Archivo | `data/raw/default of credit card clients.xls` (se conserva sin modificar) |
| Tamaño | 30.000 filas × 25 columnas (ID, 23 variables explicativas y la variable objetivo) |
| Periodo | Abril a septiembre de 2005 (clientes de Taiwán); la variable objetivo se refiere a octubre de 2005 |
| ¿Qué representa una fila? | **Un cliente** de tarjeta de crédito, con su perfil, su cupo y su comportamiento de facturación y pago durante seis meses |
| Variable objetivo | `default payment next month` (1 = incumple el pago el mes siguiente, 0 = no incumple) |

## ¿Quién decide y qué decisión?

- **Quién:** el área de riesgo crediticio y el equipo de cobranza de la entidad.
- **Decisión que habilita el modelo:** a qué clientes priorizar cada mes para gestión preventiva (recordatorios, acuerdos de pago, revisión o congelamiento de cupo) y a cuáles se les puede mantener o aumentar el cupo.
- **Por qué importa:** dejar pasar a un cliente que va a incumplir (falso negativo) cuesta varias veces más que hacer seguimiento a un cliente que sí paga (falso positivo). Con los supuestos del notebook 05, el costo de no usar ningún modelo sobre los 6.000 clientes de prueba se estima en NT$ 40,4 millones.

## Preguntas por tipo de análisis

| Tipo | Pregunta |
|---|---|
| **Descriptivo** | ¿Qué proporción de clientes incumple? ¿Cómo se distribuyen el cupo, la facturación y los pagos? |
| **Diagnóstico** | ¿Qué características se asocian con el incumplimiento: retrasos recientes, utilización del cupo, proporción pagada o variables demográficas? |
| **Predictivo** | ¿Cuál es la probabilidad de que un cliente incumpla el próximo mes? |
| **Prescriptivo** | ¿Qué umbral de decisión minimiza el costo esperado y qué acción tomar con cada banda de riesgo (baja, media o alta)? |

## KPIs SMART

| KPI | Fórmula | Meta | Periodo | Columnas |
|---|---|---|---|---|
| **Detección de incumplidos (recall)** | Incumplidos detectados / total de incumplidos | ≥ 55 % en el conjunto de prueba (el *baseline* detecta 0 %) | Evaluación mensual, sobre la cartera del mes | `default payment next month` y la predicción del modelo |
| **Capacidad de ordenar el riesgo (ROC-AUC)** | Área bajo la curva ROC de las probabilidades | ≥ 0,75 | Por cada reentrenamiento | Probabilidad estimada y `default payment next month` |
| **Reducción de la pérdida esperada** | 1 − (costo con modelo / costo sin modelo), con costo FN = exposición × LGD 60 % y costo FP = exposición × margen 10 % | ≥ 40 % frente a no usar modelo | Mensual | `BILL_AMT1` (exposición), predicción y `default payment next month` |
| **Eficiencia de la gestión** | % de incumplidos que caen en las bandas media y alta / % de la cartera en esas bandas | Cubrir ≥ 50 % de los incumplidos revisando ≤ 30 % de la cartera | Mensual | Probabilidad estimada (bandas) y `default payment next month` |
| **Tasa de incumplimiento de la cartera** | Clientes que incumplen / total de clientes | Línea base: 22,1 %. Hacerle seguimiento mes a mes | Mensual | `default payment next month` |
