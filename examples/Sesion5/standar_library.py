import math
import os
import random
import datetime

# Uso de math → calcular raíz cuadrada
numero = 25
raiz = math.sqrt(numero)
print(f"La raíz cuadrada de {numero} es {raiz}")

# Uso de os → mostrar el directorio actual
directorio_actual = os.getcwd()
print(f"Directorio actual: {directorio_actual}")

# Uso de random → elegir un número aleatorio entre 1 y 10
numero_aleatorio = random.randint(1, 10)
print(f"Número aleatorio generado: {numero_aleatorio}")

# Uso de datetime → obtener la fecha y hora actual
fecha_actual = datetime.datetime.now()
print(f"Fecha y hora actual: {fecha_actual}")