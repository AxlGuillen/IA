# Cargar el archivo JSON
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Utiliza el backend sin interfaz gráfica
import matplotlib.pyplot as plt

with open('./game-dataset/1.json') as f:
    data = json.load(f)

# Convertir los datos en un DataFrame de Pandas
df = pd.DataFrame(data)

# Separar las columnas de entrada y salida
df[['desplazamiento', 'velocidad']] = pd.DataFrame(df['input'].tolist(), index=df.index)
df['saltando'] = df['output'].apply(lambda x: x[0])  # Extraer el primer elemento de output

# Graficar con colores para indicar el estado (suelo o aire)
plt.figure(figsize=(10, 6))
# Usar el parámetro 'c' para asignar colores en función del estado
colors = ['blue' if status == 1 else 'red' for status in df['saltando']]
plt.scatter(df['desplazamiento'], df['velocidad'], c=colors, alpha=0.7)
plt.title('Desplazamiento y Velocidad con Estado de Suelo o Aire')
plt.xlabel('Desplazamiento')
plt.ylabel('Velocidad')
plt.grid(True)
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, label='Suelo (1)'),
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Aire (0)')])
plt.savefig('grafico_suelo_aire.png')
print("El gráfico se ha guardado como 'grafico_suelo_aire.png'.")
