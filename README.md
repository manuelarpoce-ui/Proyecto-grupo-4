# Proyecto Grupo 4

## Integrantes 
- Manuela Restrepo
- Andrea Paez
- Julian Olaya 
- Ana Maria Montealegre

## Como ejecutar

uv sync 
uv run jupyter lab 

##DataSet: 
Incumplimiento de pagos de clientes con tarjeta de crédito: Esta investigación se centró en el caso de los impagos de clientes en Taiwán y comparó la precisión predictiva de la probabilidad de impago entre seis métodos de minería de datos. Desde la perspectiva de la gestión de riesgos, la precisión predictiva de la probabilidad estimada de impago será más valiosa que el resultado binario de la clasificación (clientes solventes o no solventes). Dado que la probabilidad real de impago es desconocida, este estudio presentó el novedoso Método de Suavizado por Ordenación para estimarla. Con la probabilidad real de impago como variable de respuesta (Y) y la probabilidad predictiva de impago como variable independiente (X), el resultado de la regresión lineal simple (Y = A + BX) muestra que el modelo de pronóstico generado por la red neuronal artificial tiene el coeficiente de determinación más alto; su intersección de regresión (A) es cercana a cero y su coeficiente de regresión (B) a uno. Por lo tanto, entre las seis técnicas de minería de datos, la red neuronal artificial es la única que puede estimar con precisión la probabilidad real de impago. https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
## Descripción de las variables del conjunto de datos

En esta investigación se utilizó una variable binaria como variable de respuesta: el **impago de la tarjeta de crédito** (Sí = 1, No = 0). A partir de la revisión de la literatura existente, el estudio empleó 23 variables explicativas relacionadas con las características demográficas de los clientes, el historial de pagos, los importes de las facturas y los pagos realizados.

### 1. Variables demográficas y características del crédito

| Variable | Descripción | Codificación o unidad |
|---|---|---|
| `X1` | Monto del crédito otorgado, que incluye el crédito al consumo individual y el crédito familiar suplementario. | Dólares NT |
| `X2` | Género del cliente. | 1 = Hombre; 2 = Mujer |
| `X3` | Nivel educativo del cliente. | 1 = Posgrado; 2 = Universidad; 3 = Educación secundaria; 4 = Otros |
| `X4` | Estado civil del cliente. | 1 = Casado/a; 2 = Soltero/a; 3 = Otros |
| `X5` | Edad del cliente. | Años |

### 2. Historial de pagos (`X6`–`X11`)

Estas variables representan el estado de pago mensual de los clientes entre abril y septiembre de 2005.

| Variable | Descripción |
|---|---|
| `X6` | Estado de pago en septiembre de 2005. |
| `X7` | Estado de pago en agosto de 2005. |
| `X8` | Estado de pago en julio de 2005. |
| `X9` | Estado de pago en junio de 2005. |
| `X10` | Estado de pago en mayo de 2005. |
| `X11` | Estado de pago en abril de 2005. |

La codificación del estado de pago es la siguiente:

| Código | Significado |
|---|---|
| `-2` | Sin consumo. |
| `-1` | Pago realizado a tiempo. |
| `0` | Pago del mínimo, según la descripción suministrada. |
| `1` | Retraso de un mes. |
| `2` a `8` | Retraso de dos a ocho meses, respectivamente. |
| `9` | Retraso de nueve meses o más. |

### 3. Importe de las facturas (`X12`–`X17`)

Estas variables representan el importe de las facturas mensuales de los clientes, expresado en dólares NT, durante el período comprendido entre abril y septiembre de 2005.

| Variable | Descripción |
|---|---|
| `X12` | Importe de la factura en septiembre de 2005. |
| `X13` | Importe de la factura en agosto de 2005. |
| `X14` | Importe de la factura en julio de 2005. |
| `X15` | Importe de la factura en junio de 2005. |
| `X16` | Importe de la factura en mayo de 2005. |
| `X17` | Importe de la factura en abril de 2005. |

### 4. Importe de los pagos realizados (`X18`–`X23`)

Estas variables representan los importes de los pagos efectuados por los clientes durante el mismo período, expresados en dólares NT.

| Variable | Descripción |
|---|---|
| `X18` | Importe pagado en septiembre de 2005. |
| `X19` | Importe pagado en agosto de 2005. |
| `X20` | Importe pagado en julio de 2005. |
| `X21` | Importe pagado en junio de 2005. |
| `X22` | Importe pagado en mayo de 2005. |
| `X23` | Importe pagado en abril de 2005. |

### Variable de respuesta: impago

La variable objetivo representa si el cliente incurrió en impago de su tarjeta de crédito:

- `1`: Sí, el cliente incurrió en impago.
- `0`: No, el cliente no incurrió en impago.

Esta variable se utiliza como variable dependiente para desarrollar modelos de clasificación que permitan estimar la probabilidad de impago de los clientes.