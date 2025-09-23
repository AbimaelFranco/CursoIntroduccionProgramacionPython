#!/usr/bin/env python3
# python decrypt_file.py picture.jpg.enc picture_restored.jpg -p "MyStrongPassword123!"
# python tests/encryption/decrypt_file.py tests/encryption/picture.jpg.enc tests/encryption/picture_restored.jpg -p "password"
"""
Este programa desencripta un archivo previamente encriptado con AES-256-GCM.
Formato esperado del archivo encriptado:
b"ENCR" + salt(16) + nonce(12) + tag(16) + ciphertext
"""

# --- Importación de librerías ---
import argparse  # Para leer argumentos desde la terminal
from Crypto.Cipher import AES  # Para usar el algoritmo de encriptación AES
from Crypto.Protocol.KDF import PBKDF2  # Para derivar la clave a partir de la contraseña


# --- Constantes usadas en el proceso de desencriptación ---
MAGIC = b"ENCR"       # Marca especial al inicio del archivo encriptado
SALT_SIZE = 16        # Tamaño de la "sal" (valor aleatorio añadido para mayor seguridad)
NONCE_SIZE = 12       # Valor único usado por AES-GCM
TAG_SIZE = 16         # Tamaño del tag de autenticación (verifica que no haya alteraciones)
KEY_LEN = 32          # Longitud de la clave (32 bytes = 256 bits para AES-256)
PBKDF2_ITERS = 200_000  # Número de iteraciones para derivar la clave (más alto = más seguro)


# --- Función para generar la clave a partir de la contraseña y la sal ---
def derive_key(password: str, salt: bytes) -> bytes:
    """
    Genera una clave segura usando PBKDF2 a partir de:
    - La contraseña del usuario
    - La sal (salt) guardada en el archivo encriptado
    """
    return PBKDF2(password, salt, dkLen=KEY_LEN, count=PBKDF2_ITERS, hmac_hash_module=None)


# --- Función principal de desencriptación ---
def decrypt_file(in_path: str, out_path: str, password: str):
    """
    Lee un archivo encriptado y lo convierte de nuevo en su forma original,
    siempre que la contraseña proporcionada sea la correcta.
    """

    # Abrir y leer todo el archivo encriptado en memoria (modo binario)
    with open(in_path, 'rb') as f:
        data = f.read()

    # Verificar que el archivo tenga al menos el tamaño mínimo esperado
    if len(data) < 4 + SALT_SIZE + NONCE_SIZE + TAG_SIZE:
        raise ValueError("El archivo es demasiado pequeño o está dañado")

    # --- Extraer las partes del archivo encriptado ---
    off = 0
    magic = data[off:off+4]; off += 4   # Leer los primeros 4 bytes (marca MAGIC)
    if magic != MAGIC:
        raise ValueError("El archivo no fue encriptado con este programa")

    salt = data[off:off+SALT_SIZE]; off += SALT_SIZE  # Extraer la sal
    nonce = data[off:off+NONCE_SIZE]; off += NONCE_SIZE  # Extraer el nonce
    tag = data[off:off+TAG_SIZE]; off += TAG_SIZE  # Extraer el tag de autenticación
    ciphertext = data[off:]  # El resto del archivo es el texto encriptado

    # --- Generar la clave real a partir de la contraseña y la sal ---
    key = derive_key(password.encode('utf-8'), salt)

    # Crear un objeto AES en modo GCM para desencriptar
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    try:
        # Intentar desencriptar y verificar integridad con el tag
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError as e:
        # Si la contraseña es incorrecta o el archivo fue manipulado, fallará
        raise ValueError("Fallo en la desencriptación. Contraseña incorrecta o archivo corrupto.") from e

    # Guardar el archivo original desencriptado
    with open(out_path, 'wb') as f:
        f.write(plaintext)

    print(f"Archivo desencriptado correctamente: {in_path} -> {out_path}")


# --- Función que conecta todo con la terminal ---
def main():
    """
    Maneja los argumentos pasados por consola y llama a la función de desencriptar.
    """
    ap = argparse.ArgumentParser(description="Desencripta un archivo protegido con AES-256-GCM")
    ap.add_argument("input", help="Archivo encriptado de entrada")
    ap.add_argument("output", help="Archivo de salida (desencriptado)")
    ap.add_argument("-p", "--password", required=True, help="Contraseña usada para encriptar")
    args = ap.parse_args()

    # Llamar a la función principal de desencriptación
    decrypt_file(args.input, args.output, args.password)


# --- Punto de entrada del programa ---
if __name__ == "__main__":
    main()