import pandas as pd  # Importar pandas para manipulación de datos
import mysql.connector  # Importar el conector MySQL para conectarse a la base de datos
from sklearn.preprocessing import StandardScaler  # Importar el escalador
from sklearn.cluster import KMeans  # Importar KMeans
import matplotlib.pyplot as plt  # Importar matplotlib para visualización

# Conecto a la base de datos
connection = mysql.connector.connect(
    host='localhost',
    database='dataLab',
    user='root',
    password=''
)

# Leer datos de la tabla 'productos'
query = "SELECT nombre, precio, categoria, puntuacion FROM productos"
df = pd.read_sql(query, connection)  # Cargar los datos en un DataFrame

# Preprocesamiento
# Normalizar características
scaler = StandardScaler()
df[['precio', 'Posición']] = scaler.fit_transform(df[['precio', 'Posición']])

# Determinar el número óptimo de clusters usando el método del codo
wcss = []  # Lista para almacenar la suma de distancias cuadradas
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(df[['precio', 'Posición']])
    wcss.append(kmeans.inertia_)  # Inertia: suma de distancias cuadradas

# Graficar el método del codo
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss)
plt.title('Método del Codo')
plt.xlabel('Número de Clusters')
plt.ylabel('WCSS')
plt.show()

# Elegir el número óptimo de clusters (por ejemplo, 4)
k_optimo = 4
kmeans = KMeans(n_clusters=k_optimo, random_state=42)
df['Cluster'] = kmeans.fit_predict(df[['precio', 'puntuacion']])  # Agregar etiquetas de cluster al DataFrame

# Mostrar productos agrupados
for i in range(k_optimo):
    print(f"Cluster {i}:")
    print(df[df['Cluster'] == i][['nombre', 'precio', 'Posición']])
    print("\n")

# Cerrar la conexión a la base de datos
connection.close()  # Cerrar la conexión a la base de datos
