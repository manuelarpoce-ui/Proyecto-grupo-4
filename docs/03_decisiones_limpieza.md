# Registro de decisiones de limpieza (módulo 04)

El código de la limpieza está en [`src/grupo_4/limpieza.py`](../src/grupo_4/limpieza.py) y se ejecuta con `ejecutar_limpieza()`. El archivo original en `data/raw/` nunca se modifica; la base limpia se guarda en `data/processed/datos_limpios.csv`, que git ignora.

## Perfil inicial de calidad

| Revisión | Resultado |
|---|---|
| Dimensiones | 30.000 filas × 25 columnas, sin cambios después de la limpieza |
| Encabezados | Están en la segunda fila del Excel (se lee con `header=1`) |
| Tipos de datos | Las 25 columnas se leían como texto; todas representan números |
| Valores faltantes | 0 |
| ID duplicados | 0 |
| Filas idénticas sin considerar el ID | 35 pares |
| Variable objetivo | 77,88 % no incumple (23.364) y 22,12 % incumple (6.636) |

## Decisiones

| Columna(s) | Problema | Decisión | Justificación | Responsable |
|---|---|---|---|---|
| Todas | Se leían como texto (`object`) | Convertir a numérico con `pd.to_numeric(errors="coerce")` | Todas las variables son numéricas o códigos; la conversión no generó faltantes | Equipo |
| `EDUCATION` | Códigos 0, 5 y 6 no documentados (345 registros) | Agruparlos en el código 4 ("otros") | La documentación solo define 1 a 4; son pocos registros y no hay forma de saber su significado real | Equipo |
| `MARRIAGE` | Código 0 no documentado | Agruparlo en el código 3 ("otros") | La documentación solo define 1 a 3 | Equipo |
| `PAY_0` a `PAY_6` | Códigos -2 y 0 no documentados (la documentación solo define -1 y 1 a 9) | Conservarlos tal como vienen y tratar `PAY_x` como **categórica** | La evidencia sugiere que -2 ≈ "sin consumo" y 0 ≈ "pago mínimo / crédito rotativo"; además, las tasas de incumplimiento de -2, -1 y 0 no son ordenadas, así que no se tratan como un número | Equipo |
| `BILL_AMT1` a `BILL_AMT6` | Valores negativos | Conservarlos | Pueden ser saldos a favor o ajustes; no hay evidencia de que sean errores | Equipo |
| `BILL_AMT`, `PAY_AMT`, `LIMIT_BAL` | Valores extremos (más de NT$ 1 millón) | Conservarlos; las variables numéricas se estandarizan en el `Pipeline` | Son clientes reales; eliminarlos sesgaría el modelo | Equipo |
| `PAY_AMT1` a `PAY_AMT6` | — | Sin cambios | No hay negativos ni faltantes | Equipo |
| Filas | 35 pares de clientes con ID distinto e información idéntica | Conservarlos | No hay evidencia suficiente para decir que son errores; representan el 0,2 % de la base | Equipo |
| `ID` | Identificador sin valor predictivo | Se conserva en la base limpia, pero se excluye de los predictores | Usarlo como variable generaría ruido | Equipo |
| Nombres de columnas | Salto de `PAY_0` a `PAY_2` | Conservar los nombres originales y documentar a qué mes corresponde cada variable | Cambiarlos no aporta al modelo y dificulta comparar con la documentación de UCI | Equipo |

## Preprocesamiento para el modelo

Lo hace [`src/grupo_4/preprocesamiento.py`](../src/grupo_4/preprocesamiento.py) dentro de un `ColumnTransformer`, que solo aprende con los datos de entrenamiento:

- **14 numéricas** (`LIMIT_BAL`, `AGE`, `BILL_AMT1-6`, `PAY_AMT1-6`): imputación con la mediana (por seguridad) y `StandardScaler`.
- **9 categóricas** (`SEX`, `EDUCATION`, `MARRIAGE`, `PAY_0`, `PAY_2` a `PAY_6`): imputación con la moda y `OneHotEncoder(handle_unknown="ignore")`.
- Resultado: de 23 columnas se pasa a 87.

La API aplica las mismas reglas a cada cliente nuevo (`preparar_cliente` en `src/grupo_4/prediccion.py`).
