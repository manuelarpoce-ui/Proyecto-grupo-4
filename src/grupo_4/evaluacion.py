# ============================================================
# 1. IMPORTAR LIBRERÍAS
# ============================================================

import pandas as pd

from sklearn.metrics import (
    accuracy_score,             #Mide la proporción de predicciones correctas.
    precision_score,            #Mide cuántos clientes identificados como incumplidos realmente incumplen.
    recall_score,               #Mide cuántos de los clientes que incumplen logramos identificar.
    f1_score,                   #Combina precision y recall.
    confusion_matrix,           #Permite identificar aciertos y errores de clasificación.
    classification_report,      #Presenta un resumen de las métricas por clase.
    roc_auc_score,              #Evalúa la capacidad del modelo para distinguir entre las dos clases.
    brier_score_loss            #Evalúa la calidad de las probabilidades predichas.
)

from sklearn.base import clone  #Permite crear una copia del modelo para ajustar el umbral sin modificar el modelo original.

# ============================================================
# 2. FUNCIÓN PARA CALCULAR LAS MÉTRICAS DE EVALUACIÓN
# ============================================================

def calcular_metricas(y_real, y_predicho):
    """
    Calcula las principales métricas para evaluar
    el desempeño de un modelo de clasificación.
    y_real: los resultados verdaderos de los clientes.
    y_predicho: los resultados que predijo el modelo.
    """

    metricas = {
        "accuracy": accuracy_score(y_real, y_predicho),             
        "precision": precision_score(y_real, y_predicho, zero_division=0),
        "recall": recall_score(y_real, y_predicho, zero_division=0),
        "f1": f1_score(y_real, y_predicho, zero_division=0)
    }

    return metricas

# ============================================================
# 3. FUNCIÓN PARA CALCULAR LA MATRIZ DE CONFUSIÓN
# ============================================================

def calcular_matriz_confusion(y_real, y_predicho):
    """
    Calcula la matriz de confusión para identificar
    las predicciones correctas e incorrectas del modelo.
    """

    matriz = confusion_matrix(y_real, y_predicho)

    return matriz

# ============================================================
# 4. FUNCIÓN PARA GENERAR EL INFORME DE CLASIFICACIÓN
# ============================================================

def generar_reporte(y_real, y_predicho):
    """
    Genera un informe detallado con las métricas
    de clasificación para cada clase.
    """

    reporte = classification_report(
        y_real,
        y_predicho,
        zero_division=0
    )

    return reporte

# ============================================================
# 5. FUNCIÓN PARA EVALUAR UN MODELO
# ============================================================

def evaluar_modelo(modelo, X_test, y_test):
    """
    Evalúa un modelo utilizando los datos de prueba.
    Calcula métricas, matriz de confusión e informe
    de clasificación.
    """

    # Realizar predicciones
    y_predicho = modelo.predict(X_test)

    # Calcular métricas
    metricas = calcular_metricas(y_test, y_predicho)

    # Calcular matriz de confusión
    matriz = calcular_matriz_confusion(y_test, y_predicho)

    # Generar informe de clasificación
    reporte = generar_reporte(y_test, y_predicho)

    return {
        "metricas": metricas,
        "matriz_confusion": matriz,
        "reporte": reporte
    }
# ============================================================
# 6. FUNCIÓN PARA EVALUAR TODOS LOS MODELOS
# ============================================================

def evaluar_modelos(modelos, X_test, y_test):
    """
    Evalúa todos los modelos entrenados utilizando
    los datos de prueba.
    """

    resultados = {}

    for nombre, modelo in modelos.items():

        print(f"\nEvaluando modelo: {nombre}")

        resultados[nombre] = evaluar_modelo(
            modelo,
            X_test,
            y_test
        )

    return resultados
# ============================================================
# 7. FUNCIÓN PARA CALCULAR ROC-AUC Y BRIER SCORE
# ============================================================

def evaluar_probabilidades(modelo, X_test, y_test):
    """
    Evalúa la capacidad del modelo para estimar
    probabilidades de incumplimiento.
    """

    probabilidades = modelo.predict_proba(X_test)[:, 1]

    roc_auc = roc_auc_score(y_test, probabilidades)   #mide qué tan bien el modelo diferencia entre clientes que incumplen y los que no.

    brier = brier_score_loss(y_test, probabilidades)  #mide qué tan cercanas están las probabilidades estimadas por el modelo a los resultados reales. Cuanto menor sea, mejor.

    return {
        "roc_auc": roc_auc,
        "brier_score": brier
    }
# ============================================================
# 8. FUNCIÓN PARA AJUSTAR EL UMBRAL DE DECISIÓN
# ============================================================

def predecir_con_umbral(probabilidades, umbral):
    """
    Convierte las probabilidades estimadas por el modelo
    en predicciones de clase utilizando un umbral definido.
    Si la probabilidad de incumplimiento es 0.15, con un umbral de 0.20 se clasifica como 0.
    Si la probabilidad es 0.35, con un umbral de 0.20 se clasifica como 1.
    Es decir, el modelo marcará como posibles incumplidos a los clientes cuya probabilidad sea igual o superior al umbral.
    """

    predicciones = (probabilidades >= umbral).astype(int)

    return predicciones
# ============================================================
# 9. FUNCIÓN PARA COMPARAR DIFERENTES UMBRALES
# ============================================================

def comparar_umbrales(modelo, X_validacion, y_validacion):
    """
    Compara el desempeño del modelo utilizando
    diferentes umbrales de decisión.
    """

    probabilidades = modelo.predict_proba(X_validacion)[:, 1]

    umbrales = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]

    resultados = []

    for umbral in umbrales:

        y_predicho = predecir_con_umbral(probabilidades, umbral)

        metricas = calcular_metricas(y_validacion, y_predicho)

        resultados.append({
            "umbral": umbral,
            **metricas
        })

    return pd.DataFrame(resultados)

from sklearn.model_selection import train_test_split
# ============================================================
# 10. FUNCIÓN PARA DIVIDIR LOS DATOS DE VALIDACIÓN
# ============================================================

def dividir_datos_validacion(X_train, y_train):
    """
    Divide los datos de entrenamiento en entrenamiento
    interno y validación para ajustar el umbral.
    """

    X_entrenamiento, X_validacion, y_entrenamiento, y_validacion = train_test_split(
        X_train,
        y_train,
        test_size=0.20,
        random_state=42,
        stratify=y_train
    )

    return X_entrenamiento, X_validacion, y_entrenamiento, y_validacion
# ============================================================
# 11. FUNCIÓN PARA ENTRENAR EL MODELO DE VALIDACIÓN
# ============================================================

def entrenar_modelo_validacion(modelo, X_entrenamiento, y_entrenamiento):
    """
    Crea una copia del modelo original y la entrena
    utilizando únicamente los datos de entrenamiento interno.
    """

    modelo_validacion = clone(modelo)   #usamos clone porque queremos usar una copia independiente

    modelo_validacion.fit(X_entrenamiento, y_entrenamiento)

    return modelo_validacion
# ============================================================
# 12. FUNCIÓN PARA AJUSTAR EL UMBRAL DEL MODELO
# ============================================================

def ajustar_umbral(modelo, X_train, y_train):
    """
    Selecciona el umbral de decisión utilizando
    únicamente los datos de validación.
    """

    # Dividir los datos de entrenamiento
    X_entrenamiento, X_validacion, y_entrenamiento, y_validacion = (
        dividir_datos_validacion(X_train, y_train)
    )

    # Entrenar una copia del modelo
    modelo_validacion = entrenar_modelo_validacion(
        modelo,
        X_entrenamiento,
        y_entrenamiento
    )

    # Comparar los diferentes umbrales
    resultados = comparar_umbrales(
        modelo_validacion,
        X_validacion,
        y_validacion
    )

    # Seleccionar el umbral con mayor F1
    mejor_resultado = resultados.loc[resultados["f1"].idxmax()]

    mejor_umbral = mejor_resultado["umbral"]

    return {
        "mejor_umbral": mejor_umbral,
        "resultados_umbrales": resultados,
        "modelo_validacion": modelo_validacion
    }
# ============================================================
# 13. FUNCIÓN PARA EVALUAR EL MODELO CON EL UMBRAL AJUSTADO
# ============================================================

def evaluar_con_umbral(modelo, X_test, y_test, umbral):
    """
    Evalúa el modelo utilizando un umbral de decisión
    seleccionado previamente con los datos de validación.
    """

    # Obtener probabilidades de incumplimiento
    probabilidades = modelo.predict_proba(X_test)[:, 1]

    # Generar predicciones con el umbral seleccionado
    y_predicho = predecir_con_umbral(probabilidades, umbral)

    # Calcular métricas
    metricas = calcular_metricas(y_test, y_predicho)

    # Calcular matriz de confusión
    matriz = calcular_matriz_confusion(y_test, y_predicho)

    # Generar informe de clasificación
    reporte = generar_reporte(y_test, y_predicho)

    return {
        "umbral": umbral,
        "metricas": metricas,
        "matriz_confusion": matriz,
        "reporte": reporte
    }