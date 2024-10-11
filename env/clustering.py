import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Primero, leo los datos desde mi archivo CSV
df = pd.read_csv('productosE-commerce_d1.csv')

# Me aseguro de que la columna de precios sea numérica, quitando el símbolo de dólar y las comas
df['Precio'] = df['Precio'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Ahora, necesito normalizar las características (Precio y Posición) para que estén en la misma escala
scaler = StandardScaler()
df[['Precio', 'Posición']] = scaler.fit_transform(df[['Precio', 'Posición']])

# Uso el método del codo para determinar cuántos clusters serían óptimos
wcss = []  # Aquí voy a guardar las sumas de las distancias cuadradas dentro de los clusters
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(df[['Precio', 'Posición']])
    wcss.append(kmeans.inertia_)  # Guardo la inercia, que es la suma de distancias dentro de los clusters

# Grafico el método del codo para ver dónde está el punto óptimo
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss)
plt.title('Método del Codo')
plt.xlabel('Número de Clusters')
plt.ylabel('WCSS')  # Aquí es donde grafico las distancias cuadradas dentro del cluster
plt.show()

# Basándome en el gráfico del codo, elijo el número óptimo de clusters (por ejemplo, 4)
k_optimo = 4
kmeans = KMeans(n_clusters=k_optimo, random_state=42)
df['Cluster'] = kmeans.fit_predict(df[['Precio', 'Posición']])  # Agrego las etiquetas de cluster a mi DataFrame

# Finalmente, muestro los productos agrupados por cluster
for i in range(k_optimo):
    print(f"Cluster {i}:")
    print(df[df['Cluster'] == i][['Nombre', 'Precio', 'Posición']])
    print("\n")
