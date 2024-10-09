import pandas as pd  # Importa la biblioteca pandas para manipulación de datos
import mysql.connector  # Importa el conector MySQL para conectarse a la base de datos
import matplotlib.pyplot as plt  # Importa matplotlib para visualización de gráficos
import seaborn as sns  # Importa seaborn para visualización de datos

# Aqui me conecto a la base de datos
connection = mysql.connector.connect(
    host='localhost',
    database='dataLab',
    user='root',
    password=''
)

# Leo datos de la tabla 'productos' en la base de datos
query = "SELECT nombre, precio, descripcion, imagen, posicion, paginacion FROM productos"
df = pd.read_sql(query, connection)  # Cargar los datos en un DataFrame de pandas


# Análisis básico de precios
# Convierto la columna de precios a tipo numérico (removiendo símbolos y comas)
df['precio'] = df['precio'].str.replace('$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

# Calculo estadísticas descriptivas de los precios
precio_min = df['precio'].min()  # Precio mínimo
precio_max = df['precio'].max()  # Precio máximo
precio_medio = df['precio'].mean()  # Precio promedio
precio_median = df['precio'].median()  # Precio mediano

# Imprimir estadísticas de precios
print(f"Precio Mínimo: {precio_min}")
print(f"Precio Máximo: {precio_max}")
print(f"Precio Promedio: {precio_medio}")
print(f"Precio Mediano: {precio_median}")

# Generar insights clave
# 1. Comparación de Precios por Producto
top_productos = df.nlargest(10, 'precio')  # Obtener los 10 productos más caros
plt.figure(figsize=(10, 6))  # Configurar el tamaño de la figura
sns.barplot(x='nombre', y='precio', data=top_productos)  # Crear gráfico de barras
plt.title('Top 10 Productos por Precio')  # Título del gráfico
plt.xticks(rotation=45)  # Rotar las etiquetas del eje x
plt.show()  # Mostrar el gráfico

# 2. Distribución de Precios
plt.figure(figsize=(10, 6))  # Configurar el tamaño de la figura
sns.histplot(df['precio'], bins=20, kde=True)  # Crear un histograma con una curva KDE
plt.title('Distribución de Precios de Productos')  # Título del gráfico
plt.xlabel('Precio')  # Etiqueta del eje x
plt.ylabel('Frecuencia')  # Etiqueta del eje y
plt.show()  # Mostrar el gráfico

# 3. Análisis Adicional (Distribución de Descripciones de Productos)
# Este ejemplo muestra la frecuencia de las descripciones de productos
top_descripciones = df['descripcion'].value_counts().head(10)  # Obtener las 10 descripciones más comunes
top_descripciones.plot(kind='bar')  # Crear gráfico de barras
plt.title('Top 10 Descripciones de Productos')  # Título del gráfico
plt.xticks(rotation=45)  # Rotar las etiquetas del eje x
plt.ylabel('Frecuencia')  # Etiqueta del eje y
plt.show()  # Mostrar el gráfico

# Cerrar la conexión a la base de datos
connection.close()  # Cerrar la conexión a la base de datos
