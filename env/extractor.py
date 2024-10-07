import time
import csv
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Configuración del logging
logging.basicConfig(
    filename='extraccion_productos.log',  # Archivo donde se guardarán los logs
    level=logging.INFO,  # Nivel de los logs (INFO para seguimiento del proceso)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato de los logs
)

# Inicializar el navegador Microsoft Edge
driver = webdriver.Edge()

# Lista de URLs para navegar
urls = [
    "https://domicilios.tiendasd1.com/ca/extraordinarios/EXTRAORDINARIOS",
    "https://domicilios.tiendasd1.com/ca/congelados/CONGELADOS",
    "https://domicilios.tiendasd1.com/ca/alimentos-y-despensa/ALIMENTOS%20Y%20DESPENSA",
    "https://domicilios.tiendasd1.com/ca/aseo-hogar/ASEO%20HOGAR",
    "https://domicilios.tiendasd1.com/ca/aseo-y-cuidado-personal/ASEO%20Y%20CUIDADO%20PERSONAL",
    "https://domicilios.tiendasd1.com/ca/lacteos/LÁCTEOS",
    "https://domicilios.tiendasd1.com/ca/mascotas/MASCOTAS"
]

# Recorrer todas las URLs
productos = []  # Lista para almacenar los productos

for url in urls:
    logging.info(f'Extrayendo productos de la URL: {url}')  # Log de inicio de extracción
    driver.get(url)
    time.sleep(3)  # Esperar que cargue la página

    # Scroll dinámico para cargar más productos
    last_height = driver.execute_script("return document.body.scrollHeight")
    productos_extraidos = 0  # Contador de productos extraídos

    while productos_extraidos < 1000:
        # Hacer scroll hasta abajo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Esperar que se carguen los nuevos productos

        # Obtener el HTML después de la carga
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extraer los productos
        for index, product in enumerate(soup.select('div.styles__StyledCard-sc-3jvmda-0')):
            nombre = product.select_one('p.CardName__CardNameStyles-sc-147zxke-0')
            precio = product.select_one('p.CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0')
            descripcion = product.select_one('p.styles_PumStyles-sc-omx4ld-0')
            imagen = product.select_one('img')  # Seleccionar la imagen

            nombre_text = nombre.text.strip() if nombre else 'Sin nombre'
            precio_text = precio.text.strip() if precio else 'No disponible'
            descripcion_text = descripcion.text.strip() if descripcion else 'Sin descripción'
            imagen_url = imagen['src'] if imagen and 'src' in imagen.attrs else 'Sin imagen'

            # Almacenar productos con nombre y precio válidos
            if nombre_text != 'Sin nombre' and precio_text != 'No disponible':
                # Almacenar también la posición y la paginación
                productos.append([nombre_text, precio_text, descripcion_text, imagen_url, productos_extraidos + 1, url])
                productos_extraidos += 1  # Aumentar el contador

            if productos_extraidos >= 1000:
                logging.info(f'Se ha alcanzado el límite de 1000 productos en la URL: {url}')
                break

        # Verificar si hemos llegado al final de la página
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            logging.info(f'No se encontraron más productos en la URL: {url}')
            break
        last_height = new_height

# Cerrar el navegador Edge
driver.quit()
logging.info('Extracción completada, cerrando el navegador.')

# Guardar los productos en un archivo CSV
csv_file = 'productosE-commerce_d1.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Nombre', 'Precio', 'Descripción', 'Imagen', 'Posición', 'Paginación'])  # Encabezados
    writer.writerows(productos)  # Escribir datos extraídos

logging.info(f'Los productos han sido extraídos y guardados en "{csv_file}"')
print(f"Los productos han sido extraídos y guardados en '{csv_file}'")
