import time
import mysql.connector  # O puedes usar sqlite3 si decides SQLite
from bs4 import BeautifulSoup
from selenium import webdriver

# Inicializar el navegador Microsoft Edge
driver = webdriver.Edge()

# Inicializar la conexión a la base de datos
connection = None
cursor = None

try:
    # Conectar a la base de datos MySQL
    connection = mysql.connector.connect(
        host='localhost',          # Ejemplo: 'localhost'
        database='datalab',       # Cambia por tu base de datos
        user='root',              # Cambia por tu usuario de MySQL
        password=''               # Cambia por tu contraseña de MySQL
    )
    cursor = connection.cursor()

    # Crear tabla si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255),
        precio VARCHAR(50),
        descripcion TEXT,
        imagen VARCHAR(255),
        posicion INT,
        paginacion VARCHAR(255)
    )
    ''')

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
    for url in urls:
        driver.get(url)
        time.sleep(3)

        last_height = driver.execute_script("return document.body.scrollHeight")
        productos_extraidos = 0

        while productos_extraidos < 1000:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            for index, product in enumerate(soup.select('div.styles__StyledCard-sc-3jvmda-0')):
                nombre = product.select_one('p.CardName__CardNameStyles-sc-147zxke-0')
                precio = product.select_one('p.CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0')
                descripcion = product.select_one('p.styles_PumStyles-sc-omx4ld-0')
                imagen = product.select_one('img')

                nombre_text = nombre.text.strip() if nombre else 'Sin nombre'
                precio_text = precio.text.strip() if precio else 'No disponible'
                descripcion_text = descripcion.text.strip() if descripcion else 'Sin descripción'
                imagen_url = imagen['src'] if imagen and 'src' in imagen.attrs else 'Sin imagen'

                if nombre_text != 'Sin nombre' and precio_text != 'No disponible':
                    cursor.execute('''
                    INSERT INTO productos (nombre, precio, descripcion, imagen, posicion, paginacion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (nombre_text, precio_text, descripcion_text, imagen_url, productos_extraidos + 1, url))
                    productos_extraidos += 1

                if productos_extraidos >= 1000:
                    break

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

except Exception as e:
    print(f"Error: {e}")
finally:
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.commit()
        connection.close()
    driver.quit()

print("Los productos han sido extraídos y guardados en la base de datos.")
