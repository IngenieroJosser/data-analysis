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
    # Aumentar el contraste usando ecualización de histograma
    return cv2.equalizeHist(image)

def procesar_imagen(ruta_imagen):
    """
    Procesa una imagen para extraer puntos de datos de un gráfico de línea.
    
    Args:
        ruta_imagen (str): La ruta de la imagen a procesar.
        
    Returns:
        List[Tuple[float, float]]: Lista de puntos extraídos (X, Y).
    """
    # Cargar la imagen en escala de grises
    image = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

    # Mejora de la imagen
    image = mejorar_imagen(image)

    # Preprocesamiento de la imagen
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Detección de líneas usando Hough Transform
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)

    # Lista para almacenar los puntos
    puntos = []

    # Extraer los puntos de las líneas detectadas
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Calcular el punto medio
            puntos.append(((x1 + x2) / 2, (y1 + y2) / 2))

    return puntos

def procesar_imagenes(carpeta_imagenes):
    """
    Procesa todas las imágenes en una carpeta y extrae los puntos de datos.
    
    Args:
        carpeta_imagenes (str): Ruta de la carpeta con imágenes a procesar.
        
    Returns:
        pd.DataFrame: DataFrame con los puntos extraídos de todas las imágenes.
    """
    # DataFrame para almacenar todos los puntos
    todos_los_puntos = []

    # Iterar a través de todas las imágenes en la carpeta
    for nombre_archivo in os.listdir(carpeta_imagenes):
        if nombre_archivo.endswith(('.jpg', '.png', '.jpeg')):  # Filtrar por tipos de archivo de imagen
            ruta_completa = os.path.join(carpeta_imagenes, nombre_archivo)
            puntos = procesar_imagen(ruta_completa)

            # Agregar los puntos al DataFrame
            for x, y in puntos:
                todos_los_puntos.append((x, y))

    # Crear un DataFrame con los valores de los ejes X e Y
    df = pd.DataFrame(todos_los_puntos, columns=['X', 'Y'])
    return df

def graficar_datos(df):
    """
    Grafica los datos extraídos.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos a graficar.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df['X'], df['Y'], marker='o', linestyle='-', color='b')
    plt.title('Gráfico reconstruido de todas las imágenes')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
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
