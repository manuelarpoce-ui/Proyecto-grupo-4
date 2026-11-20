# ============================================================
# 0. PREPARA LAS VARIABLES NUMERICAS Y CATEGORICAS PARA LOS MODELOS
# ============================================================


# ============================================================
# 1. IMPORTAR LIBRERÍAS
# ============================================================

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# ============================================================
# 2. DEFINIR VARIABLES NUMÉRICAS (14) Y CATEGÓRICAS (9)
# ============================================================

VARIABLES_CATEGORICAS = [
    "SEX",
    "EDUCATION",
    "MARRIAGE",
    "PAY_0",
    "PAY_2",
    "PAY_3",
    "PAY_4",
    "PAY_5",
    "PAY_6"
]

VARIABLES_NUMERICAS = [
    "LIMIT_BAL",
    "AGE",
    "BILL_AMT1",
    "BILL_AMT2",
    "BILL_AMT3",
    "BILL_AMT4",
    "BILL_AMT5",
    "BILL_AMT6",
    "PAY_AMT1",
    "PAY_AMT2",
    "PAY_AMT3",
    "PAY_AMT4",
    "PAY_AMT5",
    "PAY_AMT6"
]

# ============================================================
# 3. PREPROCESAMIENTO DE VARIABLES NUMÉRICAS
# ============================================================

pipeline_numerico = Pipeline(steps=[
    ("imputador", SimpleImputer(strategy="median")),  #si alguna variable numérica tiene valores faltantes, los reemplaza por la mediana de esa variable.
    ("escalador", StandardScaler())   #estandariza las variables para que tengan escalas comparables.
])

# ============================================================
# 4. PREPROCESAMIENTO DE VARIABLES CATEGÓRICAS
# ============================================================

pipeline_categorico = Pipeline(steps=[
    ("imputador", SimpleImputer(strategy="most_frequent")),  #si encuentra datos faltantes, los reemplaza por la categoría que más se repite.
    ("codificador", OneHotEncoder(handle_unknown="ignore"))   #convierte las categorías en columnas numéricas para que los modelos puedan trabajar con ellas.
])                                                            #evita que el proceso falle si aparece una categoría que no estaba presente cuando se entrenó el modelo.

# ============================================================
# 5. UNIR LOS PIPELINE
# ============================================================

preprocesador = ColumnTransformer(
    transformers=[
        ("numericas", pipeline_numerico, VARIABLES_NUMERICAS),
        ("categoricas", pipeline_categorico, VARIABLES_CATEGORICAS)
    ]
)

# ============================================================
# 6. FUNCIÓN PARA OBTENER EL PREPROCESADOR
# ============================================================

def obtener_preprocesador():
    """
    Retorna el preprocesador que transforma las variables
    numéricas y categóricas.
    """

    return preprocesador