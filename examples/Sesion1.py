# ============================================
#      SCRIPT DE EJEMPLOS BÁSICOS DE PYTHON
# ============================================

# 1. Comentarios y sintaxis básica
# Este es un comentario de una línea
"""
Este es un comentario
de múltiples líneas
"""

# Python usa indentación para definir bloques
if True:
    print("Esto se ejecuta porque la condición es True")  # Indentación de 4 espacios

# 2. Variables y tipos de datos
# Variables de diferentes tipos
nombre = "Abimael"        # String
edad = 25                  # Entero
altura = 1.75              # Float
es_estudiante = True       # Booleano
nota = None                # Valor nulo
frutas = ["manzana", "banana", "cereza"]   # Lista
persona = {"nombre": "Abimael", "edad": 25}  # Diccionario
colores = ("rojo", "verde", "azul")        # Tupla

# Mostrar variables
print(nombre, edad, altura, es_estudiante, nota)
print("Lista:", frutas)
print("Diccionario:", persona)
print("Tupla:", colores)

# 3. print() y concatenación
# Concatenar strings usando +
print("Hola, mi nombre es " + nombre + " y tengo " + str(edad) + " años.")

# Formateo con f-strings (más moderno)
print(f"Hola, mi nombre es {nombre}, mido {altura} metros y es estudiante? {es_estudiante}")

# 4. Operadores aritméticos
a = 10
b = 3

print("Suma:", a + b)
print("Resta:", a - b)
print("Multiplicación:", a * b)
print("División:", a / b)      # Resultado float
print("División entera:", a // b)
print("Módulo (resto):", a % b)
print("Potencia:", a ** b)

# 5. Operadores de asignación
x = 5
print("Valor inicial de x:", x)

x += 2    # Equivale a x = x + 2
print("Después de x += 2:", x)

x -= 1    # Equivale a x = x - 1
print("Después de x -= 1:", x)

x *= 3
print("Después de x *= 3:", x)

x /= 2
print("Después de x /= 2:", x)

x %= 4
print("Después de x %= 4:", x)
