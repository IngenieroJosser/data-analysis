import pandas as pd
import requests
import os

# Leer el CSV en un DataFrame
df = pd.read_csv('productosE-commerce_d1.csv')

# Crear una carpeta para almacenar las imágenes
os.makedirs('imagenes', exist_ok=True)

# Función para descargar una imagen
def descargar_imagen(url, nombre):
    try:
        respuesta = requests.get(url, stream=True)
        if respuesta.status_code == 200:
            ruta_imagen = os.path.join('imagenes', nombre)
            with open(ruta_imagen, 'wb') as f:
                f.write(respuesta.content)
            print(f"Imagen guardada: {nombre}")
        else:
            print(f"No se pudo descargar la imagen: {url}")
    except Exception as e:
        print(f"Error al descargar la imagen: {url} - {e}")

# Recorrer el DataFrame para descargar las imágenes
for index, row in df.iterrows():
    nombre_producto = row['Nombre']
    url_imagen = row['Imagen']
    
    if url_imagen != "Sin imagen":  # Verificar que haya una URL válida
        nombre_archivo = f"{nombre_producto}.jpg".replace(" ", "_")
        descargar_imagen(url_imagen, nombre_archivo)
    else:
        print(f"No hay imagen para: {nombre_producto}")
