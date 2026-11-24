# Perfil inicial de los datos (módulo 03)

Reporte de calidad de la base original `data/raw/default of credit card clients.xls`
(UCI, clientes de tarjeta de crédito en Taiwán, abril a septiembre de 2005). El reporte
se generó con `03-CRISP-DM/scripts/perfil_inicial.py` del curso, sobre la base sin
limpiar (en el Excel los nombres de columnas están en la segunda fila).

## Dimensiones y calidad general

| Aspecto | Resultado |
|---|---|
| Filas | 30.000 (un cliente por fila) |
| Columnas | 25 (ID, 23 variables explicativas y la variable objetivo) |
| Tipos | Las 25 columnas se leen como numéricas |
| Valores nulos | 0 |
| ID repetidos | 0 |
| Filas idénticas sin considerar el ID | 35 |
| Variable objetivo | `default payment next month`: 22,1 % de clientes incumple |

## Advertencias del reporte automático
- `ID` tiene un valor distinto por fila: es un identificador y no se usa como variable.
- La regla de *outliers* por rango intercuartílico (IQR) marca como atípicas la variable
  objetivo (22,1 %) y las variables `PAY_*` (entre 10 % y 15 %). No son errores: son
  códigos de categorías, y por eso no se eliminan.
- Todas las columnas se leen como numéricas, aunque `SEX`, `EDUCATION`, `MARRIAGE` y
  `PAY_*` son categorías.

## Tres problemas de calidad encontrados

1. **Códigos no documentados en las variables demográficas.** `EDUCATION` trae los
   valores 0, 5 y 6 (345 clientes) y `MARRIAGE` trae el valor 0 (54 clientes), pero el
   diccionario solo define 1 a 4 y 1 a 3.
2. **Códigos no documentados en el historial de pagos.** `PAY_0` a `PAY_6` incluyen
   los valores -2 y 0, que el diccionario no define (solo -1 y 1 a 9). En `PAY_0`
   suman el 58 % de los clientes (2.759 con -2 y 14.737 con 0). Además, la primera
   columna se llama `PAY_0` y no existe `PAY_1`.
3. **Montos negativos en la facturación.** 1.930 clientes tienen algún `BILL_AMT`
   negativo (el mínimo es -339.603 dólares NT). Pueden ser saldos a favor del cliente
   o ajustes; no hay evidencia de que sean errores.

Otros hallazgos: 35 filas repetidas con ID distinto y clases desbalanceadas (22,1 %).
Cómo se trató cada problema está en `docs/03_decisiones_limpieza.md`.

## Tres hipótesis para validar en el EDA

1. **El retraso reciente predice el incumplimiento.** Los clientes con retraso en el
   último mes (`PAY_0` ≥ 1) incumplen mucho más que el resto: 50,3 % frente a 13,8 %.
2. **A mayor cupo de crédito, menos incumplimiento.** La tasa baja de 31,8 % en el
   cuartil de menor `LIMIT_BAL` a 14,0 % en el de mayor `LIMIT_BAL`.
3. **Usar casi todo el cupo aumenta el riesgo.** Los clientes cuya facturación del último
   mes es al menos el 90 % del cupo incumplen más (26,3 %) que los que usan menos del
   30 % (18,3 %).

Las tres se contrastan con evidencia en `docs/04_eda.md`.