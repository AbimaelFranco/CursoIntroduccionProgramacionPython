# pip install pycryptodome
# python encrypt_file.py picture.jpg picture.jpg.enc -p "password"
# python tests/encryption/encrypt_file.py tests/encryption/picture.jpg tests/encryption/picture.jpg.enc -p "password"
# !/usr/bin/env python3 encrypt_file.py picture.jpg picture.jpg.enc -p "password"
"""
Este programa encripta un archivo (por ejemplo, una imagen .jpg o .png)
utilizando una contraseña y el algoritmo AES-256 en modo GCM.
El archivo resultante tiene este formato:
b"ENCR" + salt(16) + nonce(12) + tag(16) + ciphertext
"""

# --- Importación de librerías ---
import argparse  # Para leer argumentos desde la línea de comandos
from Crypto.Cipher import AES  # Para usar el algoritmo de encriptación AES
from Crypto.Protocol.KDF import PBKDF2  # Para derivar una clave a partir de la contraseña
from Crypto.Random import get_random_bytes  # Para generar valores aleatorios seguros


# --- Constantes de configuración ---
MAGIC = b"ENCR"          # Marca de 4 bytes que identifica que el archivo fue encriptado con este programa
SALT_SIZE = 16           # Tamaño de la "sal" usada en PBKDF2
NONCE_SIZE = 12          # Tamaño recomendado para el nonce en AES-GCM
KEY_LEN = 32             # Longitud de la clave (32 bytes = 256 bits = AES-256)
PBKDF2_ITERS = 200_000   # Iteraciones de PBKDF2 para mayor seguridad


# --- Función para generar la clave ---
def derive_key(password: str, salt: bytes) -> bytes:
    """
    A partir de la contraseña del usuario y de una 'sal' aleatoria,
    genera una clave segura de 256 bits usando PBKDF2.
    """
    return PBKDF2(password, salt, dkLen=KEY_LEN, count=PBKDF2_ITERS, hmac_hash_module=None)


# --- Función principal de encriptación ---
def encrypt_file(in_path: str, out_path: str, password: str):
    """
    Encripta un archivo y lo guarda en formato seguro:
    ENCR + salt + nonce + tag + contenido encriptado
    """

    # 1. Generar una sal aleatoria
    salt = get_random_bytes(SALT_SIZE)

    # 2. Derivar la clave usando la contraseña y la sal
    key = derive_key(password.encode('utf-8'), salt)

    # 3. Crear un nonce aleatorio para este archivo
    nonce = get_random_bytes(NONCE_SIZE)

    # 4. Crear un objeto AES en modo GCM con esa clave y nonce
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    # 5. Leer el contenido original del archivo (modo binario)
    with open(in_path, 'rb') as f:
        plaintext = f.read()

    # 6. Encriptar el contenido y generar un tag de autenticación
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    # 7. Guardar en el archivo de salida todos los datos necesarios
    with open(out_path, 'wb') as f:
        f.write(MAGIC)       # Marca que identifica el archivo encriptado
        f.write(salt)        # Guardar la sal
        f.write(nonce)       # Guardar el nonce
        f.write(tag)         # Guardar el tag de autenticación
        f.write(ciphertext)  # Guardar el contenido encriptado

    print(f"Archivo encriptado correctamente: {in_path} -> {out_path}")


# --- Función para manejar la línea de comandos ---
def main():
    """
    Lee los argumentos de la terminal y llama a la función de encriptación.
    """
    ap = argparse.ArgumentParser(description="Encripta un archivo con una contraseña (AES-256-GCM)")
    ap.add_argument("input", help="Archivo original de entrada (ej: picture.jpg)")
    ap.add_argument("output", help="Archivo encriptado de salida")
    ap.add_argument("-p", "--password", required=True, help="Contraseña (usa una fuerte)")
    args = ap.parse_args()

    # Llamar a la función principal
    encrypt_file(args.input, args.output, args.password)


# --- Punto de entrada ---
if __name__ == "__main__":
    main()