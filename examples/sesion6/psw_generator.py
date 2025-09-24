import string
import random

# Definimos los caracteres especiales que queremos usar
CARACTERES_ESPECIALES = "!@#$%^&*()-_=+[]{};:,.<>?/"

def generar_contrasena(longitud: int) -> str:
    """
    Genera una contraseña segura aleatoria de la longitud indicada.
    
    La contraseña contiene letras mayúsculas, minúsculas, números y símbolos.

    Args:
        longitud (int): Cantidad de caracteres de la contraseña.

    Returns:
        str: Contraseña generada aleatoriamente.
    """
    if longitud < 4:
        raise ValueError("La longitud mínima recomendada es 4 caracteres.")
    
    # Conjuntos de caracteres
    letras_minusculas = string.ascii_lowercase
    letras_mayusculas = string.ascii_uppercase
    numeros = string.digits
    simbolos = CARACTERES_ESPECIALES  # Usamos la constante definida arriba
    
    # Aseguramos que haya al menos un carácter de cada tipo
    contrasena = [
        random.choice(letras_minusculas),
        random.choice(letras_mayusculas),
        random.choice(numeros),
        random.choice(simbolos)
    ]
    
    # Completamos el resto de la contraseña
    todos_los_caracteres = letras_minusculas + letras_mayusculas + numeros + simbolos
    contrasena += random.choices(todos_los_caracteres, k=longitud-4)
    
    # Mezclamos para que el orden sea aleatorio
    random.shuffle(contrasena)
    
    return ''.join(contrasena)

# Ejemplo de uso
if __name__ == "__main__":
    longitud = int(input("Ingrese la longitud deseada para la contraseña: "))
    print("Contraseña generada:", generar_contrasena(longitud))
