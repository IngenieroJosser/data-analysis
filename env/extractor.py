import time
import csv
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuro el logging para que me permita hacer seguimiento de todo el proceso de extracción
logging.basicConfig(
    filename='extraccion_productos.log',  # Este es el archivo donde voy a guardar los logs
    level=logging.INFO,  # Quiero un nivel de logs INFO para poder seguir los pasos
    format='%(asctime)s - %(levelname)s - %(message)s'  # Este es el formato que usaré para los logs
)

# Inicializo el navegador Microsoft Edge
driver = webdriver.Edge()

# Defino las URLs que voy a recorrer
urls = [
    "https://domicilios.tiendasd1.com/ca/extraordinarios/EXTRAORDINARIOS",
    "https://domicilios.tiendasd1.com/ca/congelados/CONGELADOS",
    "https://domicilios.tiendasd1.com/ca/alimentos-y-despensa/ALIMENTOS%20Y%20DESPENSA",
    "https://domicilios.tiendasd1.com/ca/aseo-hogar/ASEO%20HOGAR",
    "https://domicilios.tiendasd1.com/ca/aseo-y-cuidado-personal/ASEO%20Y%20CUIDADO%20PERSONAL",
    "https://domicilios.tiendasd1.com/ca/lacteos/LÁCTEOS",
    "https://domicilios.tiendasd1.com/ca/mascotas/MASCOTAS"
]

# Aquí voy a ir almacenando los productos que extraiga
productos = []

for url in urls:
    logging.info(f'Extrayendo productos de la URL: {url}')  # Registro que inicio la extracción para cada URL
    try:
        # Navego a la página
        driver.get(url)

        # Espero a que se cargue la sección de productos
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles__StyledCard-sc-3jvmda-0'))
        )
        
        # Inicializo el contador de productos extraídos para esta URL
        productos_extraidos = 0

        # Hago un primer scroll para saber el tamaño de la página
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Recorro la página mientras no haya extraído más de 1000 productos
        while productos_extraidos < 1000:
            # Hago scroll hacia abajo para cargar más productos
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Le doy tiempo a la página para cargar el contenido

            # Obtengo el HTML actualizado de la página
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # Verifico si hay nuevos productos para extraer
            nuevos_productos = soup.select('div.styles__StyledCard-sc-3jvmda-0')
            if not nuevos_productos:
                logging.info(f'No se encontraron más productos en la URL: {url}')
                break

            # Extraigo los datos de cada producto
            for index, product in enumerate(nuevos_productos):
                nombre = product.select_one('p.CardName__CardNameStyles-sc-147zxke-0')
                precio = product.select_one('p.CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0')
                descripcion = product.select_one('p.styles_PumStyles-sc-omx4ld-0')
                imagen = product.select_one('img')  # Busco la imagen del producto

                # Si no encuentro el `src`, trato de obtener el `data-src` o `srcset`
                if imagen:
                    imagen_url = imagen.get('src') or imagen.get('data-src') or imagen.get('srcset', 'Sin imagen')
                else:
                    imagen_url = 'Sin imagen'

                # Limpio los textos y me aseguro de no almacenar productos sin nombre o precio
                nombre_text = nombre.text.strip() if nombre else 'Sin nombre'
                precio_text = precio.text.strip() if precio else 'No disponible'
                descripcion_text = descripcion.text.strip() if descripcion else 'Sin descripción'

                # Si el producto tiene nombre y precio, lo almaceno
                if nombre_text != 'Sin nombre' and precio_text != 'No disponible':
                    productos.append([nombre_text, precio_text, descripcion_text, imagen_url, productos_extraidos + 1, url])
                    productos_extraidos += 1  # Incremento el contador

                # Verifico si ya alcancé los 1000 productos
                if productos_extraidos >= 1000:
                    logging.info(f'Se ha alcanzado el límite de 1000 productos en la URL: {url}')
                    break

            # Verifico si he llegado al final de la página
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.info(f'No se encontraron más productos al hacer scroll en la URL: {url}')
                break
            last_height = new_height

    except Exception as e:
        logging.error(f"Error al acceder a {url}: {e}")

# Cierro el navegador Edge cuando termino de extraer todos los productos
driver.quit()
logging.info('Extracción completada, cerrando el navegador.')

# Guardo los productos que extraje en un archivo CSV
csv_file = 'productosExtraidos_D1.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Nombre', 'Precio', 'Descripción', 'Imagen', 'Posición', 'Paginación'])  # Defino los encabezados del CSV
    writer.writerows(productos)  # Escribo todos los productos extraídos en el archivo

logging.info(f'Los productos han sido extraídos y guardados en "{csv_file}"')
print(f"Los productos han sido extraídos y guardados en '{csv_file}'")
