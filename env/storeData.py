import time
import mysql.connector  # O puedo usar sqlite3 si decido usar SQLite
from bs4 import BeautifulSoup
from selenium import webdriver

# Aquí inicializo el navegador Microsoft Edge
driver = webdriver.Edge()

# Inicializo la conexión a la base de datos
connection = None
cursor = None

try:
    # Me conecto a la base de datos MySQL
    connection = mysql.connector.connect(
        host='localhost',
        database='datalab',
        user='root',
        password=''
    )
    cursor = connection.cursor()

    # Creo la tabla si no existe
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

    # Defino la lista de URLs que voy a recorrer
    urls = [
        "https://domicilios.tiendasd1.com/ca/extraordinarios/EXTRAORDINARIOS",
        "https://domicilios.tiendasd1.com/ca/congelados/CONGELADOS",
        "https://domicilios.tiendasd1.com/ca/alimentos-y-despensa/ALIMENTOS%20Y%20DESPENSA",
        "https://domicilios.tiendasd1.com/ca/aseo-hogar/ASEO%20HOGAR",
        "https://domicilios.tiendasd1.com/ca/aseo-y-cuidado-personal/ASEO%20Y%20CUIDADO%20PERSONAL",
        "https://domicilios.tiendasd1.com/ca/lacteos/LÁCTEOS",
        "https://domicilios.tiendasd1.com/ca/mascotas/MASCOTAS"
    ]

    # Recorro todas las URLs
    for url in urls:
        driver.get(url)  # Navego a la URL actual
        time.sleep(3)  # Espero 3 segundos para que la página cargue

        # Tomo la altura de la página antes de hacer scroll
        last_height = driver.execute_script("return document.body.scrollHeight")
        productos_extraidos = 0  # Inicializo el contador de productos

        # Hago scroll y extraigo productos hasta llegar a 1000 o no haya más para extraer
        while productos_extraidos < 1000:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Hago scroll al final de la página
            time.sleep(3)  # Le doy tiempo a la página para cargar el contenido

            # Extraigo el contenido HTML de la página
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # Recorro los productos que aparecen en la página
            for index, product in enumerate(soup.select('div.styles__StyledCard-sc-3jvmda-0')):
                # Extraigo los detalles del producto
                nombre = product.select_one('p.CardName__CardNameStyles-sc-147zxke-0')
                precio = product.select_one('p.CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0')
                descripcion = product.select_one('p.styles_PumStyles-sc-omx4ld-0')
                imagen = product.select_one('img')

                # Limpio los textos y verifico si existen los datos
                nombre_text = nombre.text.strip() if nombre else 'Sin nombre'
                precio_text = precio.text.strip() if precio else 'No disponible'
                descripcion_text = descripcion.text.strip() if descripcion else 'Sin descripción'
                imagen_url = imagen['src'] if imagen and 'src' in imagen.attrs else 'Sin imagen'

                # Inserto en la base de datos si tiene nombre y precio
                if nombre_text != 'Sin nombre' and precio_text != 'No disponible':
                    cursor.execute('''
                    INSERT INTO productos (nombre, precio, descripcion, imagen, posicion, paginacion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (nombre_text, precio_text, descripcion_text, imagen_url, productos_extraidos + 1, url))
                    productos_extraidos += 1  # Incremento el contador

                # Si llego a 1000 productos, detengo el ciclo
                if productos_extraidos >= 1000:
                    break

            # Verifico si el scroll llegó al final de la página
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height  # Actualizo la altura para el siguiente ciclo

# Capturo cualquier error que ocurra
except Exception as e:
    print(f"Error: {e}")
finally:
    # Cierro el cursor y la conexión si existen
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.commit()  # Hago commit de los cambios en la base de datos
        connection.close()

    # Cierro el navegador al terminar
    driver.quit()

print("Los productos han sido extraídos y guardados en la base de datos.")
