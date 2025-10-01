import string
import random

CARACTERES_ESPECIALES = "!@#$%^&*()-_=+[]{};:,.<>?/"

def generar_contrasena(longitud):

    if longitud < 8:
        print("Longitud de contraseña no segura")
        return ""

    letras_minusculas = string.ascii_lowercase
    letras_mayusculas = string.ascii_uppercase
    numeros = string.digits
    simbolos = CARACTERES_ESPECIALES  # Usamos la constante definida arriba
    todos_los_caracteres = letras_minusculas + letras_mayusculas + numeros + simbolos
    
    contrasena = [random.choice(letras_minusculas), 
                  random.choice(letras_mayusculas),
                  random.choice(numeros),
                  random.choice(simbolos)]

    
    contrasena += random.choices(todos_los_caracteres, k=longitud-4)

    random.shuffle(contrasena)

    return ''.join(contrasena)

longitud = int(input("Ingrese la longitud de su contraseña: "))

print("contraseña generada: ", generar_contrasena(longitud))