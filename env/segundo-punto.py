import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def mejorar_imagen(image):
    """
    Mejora la imagen ajustando el brillo y el contraste.
    
    Args:
        image (ndarray): La imagen original en escala de grises.
        
    Returns:
        ndarray: La imagen mejorada.
    """
    return cv2.equalizeHist(image)

def procesar_imagen(ruta_imagen):
    """
    Procesa una imagen para extraer puntos de datos de múltiples gráficos de línea.
    
    Args:
        ruta_imagen (str): La ruta de la imagen a procesar.
        
    Returns:
        Dict: Diccionario con identificadores de gráfica y puntos extraídos.
    """
    # Cargar la imagen en escala de grises
    image = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    image = mejorar_imagen(image)

    # Preprocesamiento de la imagen
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Detección de contornos para identificar gráficos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Diccionario para almacenar puntos por cada gráfico
    graficas_puntos = {}

    # Procesar cada contorno encontrado
    for i, contour in enumerate(contours):
        # Crear una máscara para el contorno actual
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [contour], -1, 255, -1)

        # Aplicar la máscara a la imagen
        masked_image = cv2.bitwise_and(image, mask)

        # Detección de líneas en la imagen enmascarada
        lines = cv2.HoughLinesP(masked_image, rho=1, theta=np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

        # Lista para almacenar los puntos de la gráfica actual
        puntos = []

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                puntos.append(((x1 + x2) / 2, (y1 + y2) / 2))

        # Guardar los puntos en el diccionario con un identificador
        graficas_puntos[f'Grafica_{i+1}'] = puntos

    return graficas_puntos

def procesar_imagenes(carpeta_imagenes):
    """
    Procesa todas las imágenes en una carpeta y extrae los puntos de datos de múltiples gráficas.
    
    Args:
        carpeta_imagenes (str): Ruta de la carpeta con imágenes a procesar.
        
    Returns:
        pd.DataFrame: DataFrame con los puntos extraídos de todas las imágenes.
    """
    # Lista para almacenar todos los puntos
    todos_los_puntos = []

    # Iterar a través de todas las imágenes en la carpeta
    for nombre_archivo in os.listdir(carpeta_imagenes):
        if nombre_archivo.endswith(('.jpg', '.png', '.jpeg')):  # Filtrar por tipos de archivo de imagen
            ruta_completa = os.path.join(carpeta_imagenes, nombre_archivo)
            graficas_puntos = procesar_imagen(ruta_completa)

            # Agregar los puntos al DataFrame
            for grafica, puntos in graficas_puntos.items():
                for x, y in puntos:
                    todos_los_puntos.append((grafica, x, y))

    # Crear un DataFrame con los valores de los ejes X e Y y el identificador de gráfica
    df = pd.DataFrame(todos_los_puntos, columns=['Grafica', 'X', 'Y'])
    return df

def graficar_datos(df):
    """
    Grafica los datos extraídos por cada gráfica.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos a graficar.
    """
    unique_graphs = df['Grafica'].unique()

    plt.figure(figsize=(10, 6))
    for grafica in unique_graphs:
        subset = df[df['Grafica'] == grafica]
        plt.plot(subset['X'], subset['Y'], marker='o', linestyle='-', label=grafica)

    plt.title('Gráficos reconstruidos de todas las imágenes')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == '__main__':
    # Ruta de la carpeta de imágenes
    carpeta_imagenes = 'imagenes'

    # Procesar imágenes y obtener DataFrame
    df = procesar_imagenes(carpeta_imagenes)

    # Mostrar la tabla generada
    print("Datos extraídos de los gráficos:")
    print(df)

    # Graficar los datos extraídos
    graficar_datos(df)
