# ============================================================
# 0. CONSTRUIR Y ENTRENAR LOS TRES MODELOS
# ============================================================

# ============================================================
# 1. IMPORTAR LIBRERÍAS
# ============================================================

from sklearn.model_selection import train_test_split   #ok.train_test_split: divide los datos en entrenamiento y prueba.
from sklearn.pipeline import Pipeline   #Pipeline: une el preprocesamiento y el modelo.
from sklearn.dummy import DummyClassifier   #ok DummyClassifier: construye nuestro modelo base.
from sklearn.linear_model import LogisticRegression  #ok LogisticRegression: construye la regresión logística.
from sklearn.tree import DecisionTreeClassifier     #ok DecisionTreeClassifier: construye el árbol de decisión.

from grupo_4.preprocesamiento import obtener_preprocesador

# ============================================================
# 2. SEPARAR VARIABLES PREDICTORAS Y VARIABLE OBJETIVO
# ============================================================

def separar_variables(df):

    """
    Separa las variables predictoras (X) de la variable objetivo (y).
    """

    X = df.drop(columns=[
        "ID",                           #excluimos ID, porque es un identificador de cliente y no debe uasrse como predictor
        "default payment next month"
    ])

    y = df["default payment next month"]

    return X, y

# ============================================================
# 3. DIVIDIR LOS DATOS EN ENTRENAMIENTO Y PRUEBA
# ============================================================

def dividir_datos(X, y):

    """
    Divide los datos en conjuntos de entrenamiento y prueba.
    Utiliza una proporción 80/20 y conserva la distribución
    de la variable objetivo.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,             #reserva el 20 % para probar los modelos y utiliza el 80 % para entrenarlos.
        random_state=42,            #permite reproducir la misma división.
        stratify=y                  #conserva la proporción de clientes que incumplen y no incumplen en ambos conjuntos.
    )

    return X_train, X_test, y_train, y_test

# ============================================================
# 4. CREAR MODELO BASELINE
# ============================================================

def crear_modelo_baseline():

    """
    Crea un modelo base que predice siempre la clase más frecuente.
    """

    modelo = DummyClassifier(strategy="most_frequent")

    return modelo

# ============================================================
# 5. CREAR MODELO DE REGRESIÓN LOGÍSTICA
# ============================================================

def crear_modelo_logistico():

    """
    Crea un modelo de regresión logística que incluye
    el preprocesamiento de las variables.
    """

    modelo = Pipeline(steps=[
        ("preprocesamiento", obtener_preprocesador()),
        ("modelo", LogisticRegression(
            max_iter=1000,
            random_state=42
        ))
    ])

    return modelo

# ============================================================
# 6. CREAR MODELO DE ÁRBOL DE DECISIÓN
# ============================================================

def crear_modelo_arbol():

    """
    Crea un modelo de árbol de decisión que incluye
    el preprocesamiento de las variables.
    """

    modelo = Pipeline(steps=[
        ("preprocesamiento", obtener_preprocesador()),
        ("modelo", DecisionTreeClassifier(          #crea el modelo de árbol de decisión.
            max_depth=5,                            #limita la profundidad del árbol a cinco niveles
            random_state=42                         #permite reproducir los resultados. Semilla
        ))
    ])

    return modelo

# ============================================================
# 7. ENTRENAR LOS TRES MODELOS
# ============================================================

def entrenar_modelos(X_train, y_train):

    """
    Entrena el baseline, la regresión logística
    y el árbol de decisión utilizando los datos
    de entrenamiento.
    """

    print("Entrenando modelo baseline...")

    modelo_baseline = crear_modelo_baseline()       
    modelo_baseline.fit(X_train, y_train)           #fit le permite al modelo aprender a partir de los datos

    print("Entrenando regresión logística...")

    modelo_logistico = crear_modelo_logistico()
    modelo_logistico.fit(X_train, y_train)

    print("Entrenando árbol de decisión...")

    modelo_arbol = crear_modelo_arbol()
    modelo_arbol.fit(X_train, y_train)

    print("\nLos tres modelos fueron entrenados correctamente.")

    return {
        "baseline": modelo_baseline,
        "logistico": modelo_logistico,
        "arbol": modelo_arbol
    }
    
# ============================================================
# 8. EJECUTAR PROCESO COMPLETO DE ENTRENAMIENTO
# ============================================================

def ejecutar_entrenamiento(df):

    """
    Ejecuta la separación de variables, división de datos
    y entrenamiento de los tres modelos.
    """

    print("Separando variables predictoras y objetivo...")

    X, y = separar_variables(df)

    print("\nDividiendo datos en entrenamiento y prueba...")

    X_train, X_test, y_train, y_test = dividir_datos(X, y)

    print("\nEntrenando modelos...")

    modelos = entrenar_modelos(X_train, y_train)

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "modelos": modelos
    }