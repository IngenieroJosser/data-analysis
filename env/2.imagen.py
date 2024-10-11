import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

carpeta_imagenes = 'imagenes-linea'

def extraer_puntos_grafico(imagen_path):
    imagen = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
    imagen_suavizada = cv2.GaussianBlur(imagen, (5, 5), 0)
    bordes = cv2.Canny(imagen_suavizada, 50, 150)
    lineas = cv2.HoughLinesP(bordes, rho=1, theta=np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
    puntos = []
    if lineas is not None:
        for linea in lineas:
            for x1, y1, x2, y2 in linea:
                puntos.append((x1, y1))
                puntos.append((x2, y2))
    return puntos

def mostrar_puntos(puntos, imagen_path):
    imagen_color = cv2.imread(imagen_path)
    puntos = np.array(puntos)
    plt.imshow(cv2.cvtColor(imagen_color, cv2.COLOR_BGR2RGB))
    if puntos.size > 0:
        plt.scatter(puntos[:, 0], puntos[:, 1], color='red', s=10)
    plt.title('Puntos detectados en el gráfico')
    plt.show()

for imagen_nombre in os.listdir(carpeta_imagenes):
    imagen_path = os.path.join(carpeta_imagenes, imagen_nombre)
    puntos = extraer_puntos_grafico(imagen_path)
    mostrar_puntos(puntos, imagen_path)
    print(f"Puntos extraídos de {imagen_nombre}:")
    for punto in puntos:
        print(punto)
