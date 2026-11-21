# Hallazgos del EDA (módulo 05)

El análisis completo está en [`notebooks/01_eda.ipynb`](../notebooks/01_eda.ipynb). La tasa global de incumplimiento es **22,1 %**.

| # | Hallazgo | Evidencia | Implicación para el modelo |
|---|---|---|---|
| 1 | **El historial de pagos es la señal más fuerte del incumplimiento** | Con `PAY_0 = 2` (dos meses de retraso) incumple el 69,1 %, frente al 12,8 % a 16,8 % de quienes no tienen retraso. La tasa pasa de 11,7 % sin ningún mes con retraso a 70,3 % con retraso en los seis meses | Incluir `PAY_0` a `PAY_6`. Tratarlas como categóricas, porque -2, -1 y 0 no siguen un orden |
| 2 | **No pagar la factura anterior se asocia con mucho más incumplimiento** | Quienes no pagaron nada de la factura anterior incumplen el 52,5 %; quienes pagaron el 100 % o más, el 13,9 % | Los montos pagados (`PAY_AMT`) y facturados aportan información cuando se combinan |
| 3 | **Usar más cupo se asocia con más incumplimiento** | Utilización ≥ 100 %: 30,1 %; utilización de 0 % a 25 %: 16,8 %. A mayor `LIMIT_BAL`, menor incumplimiento (correlación -0,15) | Incluir `LIMIT_BAL`; la utilización del cupo es candidata a variable derivada |
| 4 | **Las variables demográficas muestran diferencias moderadas** | Hombres 24,2 % vs. mujeres 20,8 %; secundaria 25,2 % vs. posgrado 19,2 %; la edad tiene forma de U (21-25 años: 26,7 %; 31-35: 19,4 %) | Su peso es menor. Sexo y estado civil son atributos sensibles: hay que discutir si se usan |
| 5 | **Las facturas están muy correlacionadas entre sí y casi nada con el objetivo** | `BILL_AMT1` a `BILL_AMT6` tienen correlaciones de 0,80 a 0,95 entre sí y cercanas a 0 con el incumplimiento | Hay multicolinealidad en el modelo lineal; se estandarizan y se mantienen, porque pueden aportar en conjunto |
| 6 | **Las clases están desbalanceadas** | 77,9 % no incumple y 22,1 % sí | Un modelo que siempre diga "no incumple" acierta el 77,9 %: se evalúa con recall, F1 y ROC-AUC, y se ajusta el umbral |

## Hipótesis del charter

| Hipótesis | Resultado | Evidencia |
|---|---|---|
| H1. Los clientes con retrasos recientes de pago tienen más probabilidad de incumplir | **Confirmada** | La tasa sube de 12,8 % a 16,8 % (sin retraso) a 33,9 % con un mes y 69,1 % con dos meses de retraso en `PAY_0` |
| H2. Pagar menos de la factura anterior y usar más cupo aumenta la probabilidad de incumplir | **Confirmada** | No pagó nada: 52,5 % vs. pagó el 100 %: 13,9 %. Utilización ≥ 100 %: 30,1 % vs. 0-25 %: 16,8 % |
| H3. Las características demográficas explican el incumplimiento | **No concluyente** (diferencias moderadas) | Diferencias de 3 a 8 puntos entre grupos; el análisis descriptivo no permite separar su efecto del de otras variables |

## Variables candidatas / descartadas

- **Incluidas en el modelo (23):** `LIMIT_BAL`, `SEX`, `EDUCATION`, `MARRIAGE`, `AGE`, `PAY_0` a `PAY_6`, `BILL_AMT1` a `BILL_AMT6`, `PAY_AMT1` a `PAY_AMT6`.
- **Descartada:** `ID` (identificador sin valor predictivo).
- **Variables derivadas exploradas, pero no incluidas en el modelo actual:** meses con retraso, utilización del cupo (`BILL_AMT1 / LIMIT_BAL`) y proporción pagada (`PAY_AMT1 / BILL_AMT2`). Mostraron una relación clara con el incumplimiento y son candidatas para una siguiente versión.
- **Valores extremos:** se conservan (ver `03_decisiones_limpieza.md`).
