import json
import matplotlib.pyplot as plt
import numpy as np

# Cargar datos desde el archivo JSON
with open('1.json', 'r') as file:
    datos = json.load(file)

# Extraer entradas y salidas
entradas = [item['input'] for item in datos]
salidas = [item['output'][0] for item in datos]

# Separar las entradas en dos listas para graficar
x = [entrada[0] for entrada in entradas]  # Primer valor de input
y = [entrada[1] for entrada in entradas]  # Segundo valor de input

# Crear un gráfico de dispersión
plt.figure(figsize=(10, 6))
scatter = plt.scatter(x, y, c=salidas, cmap='bwr', alpha=0.6)
plt.colorbar(scatter, label='Salida')
plt.xlabel('Input 1')
plt.ylabel('Input 2')
plt.title('Gráfica de Dispersión de Datos de Entrada')
plt.grid()
plt.show()
