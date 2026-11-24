# Proyecto Grupo 4
## Predicción del incumplimiento de pagos de clientes con tarjeta de crédito

### 1. Integrantes

- Manuela Restrepo
- Andrea Paez
- Julian Olaya
- Ana Maria Montealegre

---

### 2. Contexto del proyecto

Las entidades financieras enfrentan el riesgo de que algunos de sus clientes no cumplan oportunamente con sus obligaciones de pago.

Identificar anticipadamente a los clientes que presentan una mayor probabilidad de incumplimiento puede ayudar a mejorar los procesos de gestión del riesgo crediticio y facilitar la toma de decisiones.

Este proyecto desarrolla un ejercicio de análisis de datos y aprendizaje automático para identificar patrones asociados al incumplimiento de pagos de tarjetas de crédito.

El propósito es construir y evaluar modelos predictivos que permitan estimar la probabilidad de que un cliente incumpla sus obligaciones financieras.

### 3. Objetivo del proyecto

**Objetivo general**

Desarrollar un modelo de clasificación que permita predecir el incumplimiento de pago de los clientes de tarjetas de crédito, utilizando información demográfica, características del crédito, historial de pagos, valores facturados y pagos realizados.

**Objetivos específicos**

- Analizar el comportamiento de los clientes y las características relacionadas con el incumplimiento.
- Preparar y transformar la información para su utilización en modelos de aprendizaje automático.
- Construir diferentes modelos predictivos y comparar su desempeño.
- Evaluar los resultados utilizando métricas apropiadas para un problema de clasificación con clases desbalanceadas.
- Proponer recomendaciones que puedan apoyar la gestión del riesgo crediticio.

### 4. Fuente de información

El proyecto utiliza el conjunto de datos **Default of Credit Card Clients**, disponible en el repositorio de la Universidad de California, Irvine (UCI).

Fuente: https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients

**Características del conjunto de datos:**

- 30.000 registros de clientes.
- 23 variables explicativas.
- 1 variable objetivo.
- Información relacionada con características demográficas, crédito, historial de pagos, facturación y pagos realizados.
- Datos correspondientes a clientes de Taiwán.

---

### 5. Descripción de las variables del conjunto de datos

El conjunto de datos contiene información de los clientes durante seis meses, relacionada con sus características personales, el crédito otorgado, el comportamiento de pago, los valores facturados y los pagos realizados.

Las 23 variables explicativas se organizan en cuatro grupos:

#### 5.1. Variables demográficas y características del crédito

Estas variables permiten conocer las características generales de los clientes y el monto del crédito que les fue otorgado.

| Variable | Descripción | Codificación o unidad |
|---|---|---|
| `LIMIT_BAL` | Monto total del crédito otorgado al cliente, incluyendo crédito individual y familiar complementario. | Dólares taiwaneses (NTD). |
| `SEX` | Sexo del cliente. | 1 = Hombre; 2 = Mujer. |
| `EDUCATION` | Nivel educativo del cliente. | 1 = Posgrado; 2 = Universidad; 3 = Secundaria; 4 = Otros. |
| `MARRIAGE` | Estado civil del cliente. | 1 = Casado; 2 = Soltero; 3 = Otros. |
| `AGE` | Edad del cliente. | Años. |

**Importancia para el negocio:** estas variables permiten analizar si las características demográficas y el nivel de crédito otorgado presentan alguna relación con el incumplimiento de las obligaciones financieras.

#### 5.2. Variables de historial de pagos

Estas variables representan el comportamiento de pago de los clientes durante los seis meses anteriores al período de predicción.

| Variable | Descripción | Período |
|---|---|---|
| `PAY_0` | Estado de pago del cliente. | Septiembre de 2005. |
| `PAY_2` | Estado de pago del cliente. | Agosto de 2005. |
| `PAY_3` | Estado de pago del cliente. | Julio de 2005. |
| `PAY_4` | Estado de pago del cliente. | Junio de 2005. |
| `PAY_5` | Estado de pago del cliente. | Mayo de 2005. |
| `PAY_6` | Estado de pago del cliente. | Abril de 2005. |

**Codificación del estado de pago:**

| Código | Significado |
|---|---|
| `-2` | Sin consumo. |
| `-1` | Pago realizado oportunamente. |
| `0` | Uso de crédito revolvente, sin retraso registrado. |
| `1` | Retraso de un mes. |
| `2` | Retraso de dos meses. |
| `3` | Retraso de tres meses. |
| `4` | Retraso de cuatro meses. |
| `5` | Retraso de cinco meses. |
| `6` | Retraso de seis meses. |
| `7` | Retraso de siete meses. |
| `8` | Retraso de ocho meses. |
| `9` | Retraso de nueve meses o más. |

**Importancia para el negocio:** estas variables son especialmente relevantes porque permiten identificar patrones de comportamiento relacionados con los retrasos en los pagos. Un cliente que presenta retrasos recurrentes podría representar un mayor riesgo de incumplimiento.

#### 5.3. Variables de importes facturados

Representan el valor de las facturas mensuales de los clientes durante los seis meses analizados.

| Variable | Descripción | Período |
|---|---|---|
| `BILL_AMT1` | Valor de la factura del cliente. | Septiembre de 2005. |
| `BILL_AMT2` | Valor de la factura del cliente. | Agosto de 2005. |
| `BILL_AMT3` | Valor de la factura del cliente. | Julio de 2005. |
| `BILL_AMT4` | Valor de la factura del cliente. | Junio de 2005. |
| `BILL_AMT5` | Valor de la factura del cliente. | Mayo de 2005. |
| `BILL_AMT6` | Valor de la factura del cliente. | Abril de 2005. |

**Unidad de medida:** dólares taiwaneses (NTD).

**Importancia para el negocio:** permiten analizar el nivel de endeudamiento y la evolución de las obligaciones facturadas. También ayudan a identificar posibles cambios en el comportamiento financiero de los clientes.

#### 5.4. Variables de pagos realizados

Representan los valores de los pagos efectuados por los clientes durante los seis meses analizados.

| Variable | Descripción | Período |
|---|---|---|
| `PAY_AMT1` | Valor del pago realizado por el cliente. | Septiembre de 2005. |
| `PAY_AMT2` | Valor del pago realizado por el cliente. | Agosto de 2005. |
| `PAY_AMT3` | Valor del pago realizado por el cliente. | Julio de 2005. |
| `PAY_AMT4` | Valor del pago realizado por el cliente. | Junio de 2005. |
| `PAY_AMT5` | Valor del pago realizado por el cliente. | Mayo de 2005. |
| `PAY_AMT6` | Valor del pago realizado por el cliente. | Abril de 2005. |

**Unidad de medida:** dólares taiwaneses (NTD).

**Importancia para el negocio:** permiten conocer cuánto dinero paga efectivamente el cliente frente a sus obligaciones y analizar si sus pagos son suficientes para cubrir los valores facturados.

#### 5.5. Variable objetivo: incumplimiento de pago

La variable que buscamos predecir es:

`default payment next month`

| Código | Significado |
|---|---|
| `0` | El cliente no presenta incumplimiento de pago en el siguiente mes. |
| `1` | El cliente presenta incumplimiento de pago en el siguiente mes. |

Esta variable se utiliza como objetivo para desarrollar modelos de clasificación que permitan estimar la probabilidad de incumplimiento de los clientes.

---

### 6. Metodología de trabajo

El proyecto se desarrolla siguiendo las siguientes etapas:

1. **Comprensión del negocio:** identificación del problema y del objetivo de predicción.
2. **Análisis exploratorio de datos (EDA):** revisión de la información, distribución de variables y comportamiento de los clientes.
3. **Limpieza y preparación de datos:** tratamiento de inconsistencias y preparación de las variables.
4. **Entrenamiento de modelos:** construcción de un modelo base, regresión logística y árbol de decisión.
5. **Evaluación de modelos:** comparación de resultados mediante métricas de clasificación.
6. **Ajuste del umbral de decisión:** análisis de alternativas para mejorar la identificación de clientes con incumplimiento.
7. **Conclusiones y recomendaciones:** interpretación de los resultados desde la perspectiva del negocio.

### 7. Modelos desarrollados

Se compararon tres alternativas con los mismos datos de entrenamiento (24.000 clientes) y de prueba (6.000 clientes):

| Modelo | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Modelo base (*Baseline*: siempre "no incumple") | 0,7788 | 0,0000 | 0,0000 | 0,0000 | — |
| Regresión logística | 0,8168 | 0,6619 | 0,3512 | 0,4589 | 0,7580 |
| Árbol de decisión | 0,8165 | 0,6794 | 0,3225 | 0,4374 | 0,7402 |

La comparación permite identificar cuál ofrece el mejor equilibrio entre las métricas de desempeño y las necesidades del negocio. Se eligió la **regresión logística**, que supera al *baseline* y al árbol en recall, F1 y ROC-AUC. El detalle está en [`docs/05_modelado.md`](docs/05_modelado.md).

### 8. Resultados obtenidos

En la evaluación inicial sobre el conjunto de prueba, la regresión logística obtuvo los siguientes resultados:

| Métrica | Resultado |
|---|---:|
| Exactitud (Accuracy) | 81,68 % |
| Precisión (Precision) | 66,19 % |
| Sensibilidad (Recall) | 35,12 % |
| F1-score | 0,4589 |
| ROC-AUC | 0,7580 |

Posteriormente, se realizó un ajuste del umbral de clasificación a 0,20, con el propósito de identificar una mayor cantidad de clientes que presentan incumplimiento.

Con este ajuste se obtuvieron los siguientes resultados:

| Métrica | Resultado |
|---|---:|
| Exactitud (Accuracy) | 75,15 % |
| Precisión (Precision) | 45,24 % |
| Sensibilidad (Recall) | 58,70 % |
| F1-score | 0,511 |

El ajuste permitió aumentar la capacidad de identificación de clientes con incumplimiento, aunque también incrementó la cantidad de clientes clasificados incorrectamente como posibles incumplidores.

Los hallazgos del EDA están en [`docs/04_eda.md`](docs/04_eda.md); las decisiones de limpieza, en [`docs/03_decisiones_limpieza.md`](docs/03_decisiones_limpieza.md), y los KPIs y el *project charter*, en [`docs/01_problema_y_kpis.md`](docs/01_problema_y_kpis.md) y [`docs/02_project_charter.md`](docs/02_project_charter.md).

### 9. Enfoque de negocio y aplicación

Desde la perspectiva de una entidad financiera, los resultados pueden servir como herramienta de apoyo para la gestión del riesgo crediticio.

La identificación de clientes con mayor probabilidad de incumplimiento podría contribuir a:

- Detectar anticipadamente comportamientos asociados al riesgo.
- Priorizar el seguimiento de clientes.
- Apoyar estrategias de comunicación y gestión preventiva.
- Mejorar el análisis de las decisiones relacionadas con el crédito.

Con los supuestos financieros del notebook 05 (pérdida del 60 % del saldo por cada incumplimiento no detectado y 10 % de margen perdido por cada falsa alarma), la política de menor costo reduce la pérdida estimada en un **53,3 %** frente a no usar modelo. Además, las bandas de riesgo media y alta reúnen el **58,7 % de los incumplidos revisando solo el 28,7 % de la cartera**.

| Banda | Probabilidad de incumplimiento | Acción sugerida |
|---|---|---|
| Bajo | < 20 % | Mantener condiciones; candidato a aumento de cupo |
| Medio | 20 % – 50 % | Seguimiento y recordatorios de pago; no aumentar cupo |
| Alto | ≥ 50 % | Gestión preventiva de cobranza; revisar o congelar cupo |

El modelo debe utilizarse como herramienta de apoyo y no como único criterio para tomar decisiones sobre los clientes.

### 10. Límites del modelo

- **Datos antiguos y de otro país:** corresponden a clientes de Taiwán en 2005. El comportamiento de pago cambia con el país y el ciclo económico, así que el modelo debe reentrenarse con datos propios antes de usarse.
- **Precisión moderada:** con el umbral de 0,20, de cada 100 clientes señalados como posibles incumplidores, unos 45 incumplen realmente. Por eso se recomienda usarlo para priorizar la gestión, no para rechazar clientes.
- **Incumplimientos difíciles de detectar:** el 98 % de los incumplidos que el modelo no detecta no tenía retraso en el último mes, así que su historial no daba señales.
- **Supuestos financieros:** la pérdida por incumplimiento (60 %) y el margen (10 %) son supuestos de trabajo; la base no incluye recuperaciones ni rentabilidad reales. El umbral óptimo cambia entre 0,02 y 0,33 según esos supuestos.
- **Atributos sensibles:** el modelo usa sexo, estado civil y edad. Falta revisar si su desempeño es equitativo entre grupos.
- **Alcance del modelado:** no se usaron validación cruzada ni búsqueda de hiperparámetros, y las variables derivadas del EDA (meses con retraso, utilización del cupo, proporción pagada) aún no se incluyen como predictores.

### 11. Estructura del repositorio

```
Proyecto-grupo-4/
├── README.md
├── pyproject.toml          ← dependencias del proyecto (uv)
├── uv.lock                 ← versiones exactas
├── data/
│   ├── raw/                ← datos originales de UCI (no se modifican)
│   └── processed/          ← base limpia generada por el código (ignorada por git)
├── docs/
│   ├── 00_acuerdos_equipo.md
│   ├── 01_problema_y_kpis.md
│   ├── 02_perfil_inicial.md
│   ├── 02_project_charter.md
│   ├── 03_decisiones_limpieza.md
│   ├── 04_eda.md
│   ├── 05_modelado.md
│   └── 06_pipeline.md
├── notebooks/
│   ├── 01_eda.ipynb              ← análisis exploratorio y hallazgos
│   ├── 02_procesamiento.ipynb    ← preparación de variables
│   ├── 03_modelamiento.ipynb     ← baseline, regresión logística y árbol
│   ├── 04_evaluacion.ipynb       ← métricas, umbral y sobreajuste
│   └── 05_impacto_negocio.ipynb  ← costos, umbral óptimo y bandas de riesgo
├── api/
│   └── main.py              ← punto de entrada de la API (usa src/grupo_4/api.py)
├── src/
│   ├── limpieza.py          ← atajo a grupo_4/limpieza.py
│   └── train.py             ← atajo: reentrena el modelo (uv run python -m src.train)
├── src/grupo_4/
│   ├── limpieza.py          ← carga, limpia, valida y guarda la base
│   ├── preprocesamiento.py  ← ColumnTransformer (escalado + one-hot)
│   ├── entrenamiento.py     ← división de datos y Pipelines de los modelos
│   ├── evaluacion.py        ← métricas y comparación de umbrales
│   ├── guardar_modelo.py    ← entrena el modelo final y lo guarda en models/
│   ├── prediccion.py        ← carga el modelo y calcula el riesgo de un cliente
│   ├── api.py               ← API con FastAPI
│   └── formulario.html      ← formulario web de la API
├── models/                  ← modelo entrenado (ignorado por git; se regenera)
└── tests/                   ← pruebas con pytest
```

### 12. Instalación y ejecución

El proyecto utiliza UV para administrar las dependencias del entorno de trabajo.

**1. Sincronizar las dependencias:**

```bash
uv sync
```

**2. Entrenar y guardar el modelo** (crea `models/modelo_logistico.joblib`; es necesario antes de iniciar la API):

```bash
uv run python -m src.train
```

**3. Iniciar la API:**

```bash
uv run uvicorn api.main:app --reload
```

- Formulario para consultar un cliente: http://127.0.0.1:8000/
- Documentación técnica de la API: http://127.0.0.1:8000/docs
- `GET /health` (o `GET /estado`): verifica que la API esté funcionando.
- `POST /predict` (o `POST /predecir`): recibe los datos de un cliente y devuelve la probabilidad de incumplimiento, la predicción, la banda de riesgo y la acción sugerida.

**4. Correr las pruebas:**

```bash
uv run pytest
```

**5. Abrir los notebooks:**

```bash
uv run jupyter lab
```

### 13. Conclusión general

Este proyecto permite explorar cómo las técnicas de aprendizaje automático pueden contribuir a la identificación del riesgo de incumplimiento en clientes de tarjetas de crédito.

La comparación de modelos y el ajuste del umbral de clasificación muestran que la selección de un modelo no debe depender únicamente de su exactitud, sino también de su capacidad para identificar correctamente a los clientes que presentan incumplimiento.

De esta manera, se busca aportar una herramienta analítica que apoye la toma de decisiones y fortalezca los procesos de gestión del riesgo crediticio.