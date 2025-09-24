# encrypt_folder.py
# pip install pyinstaller
# pyinstaller --onefile --noconsole encrypt_folder.py

"""
Este programa encripta todos los archivos de la carpeta donde se ejecute,
usando AES-256-GCM y una contraseña fija definida en el código.
Los archivos encriptados se guardan en una subcarpeta llamada "encrypted".
"""

import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

# --- Configuración ---
MAGIC = b"ENCR"
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_LEN = 32
PBKDF2_ITERS = 200_000

# ⚠️ Contraseña fija (puedes cambiarla o pedirla al usuario)
PASSWORD = "MiSuperPasswordSegura"

# --- Función para derivar clave ---
def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=KEY_LEN, count=PBKDF2_ITERS, hmac_hash_module=None)

# --- Función de encriptado de un archivo ---
def encrypt_file(in_path: str, out_path: str, password: str):
    salt = get_random_bytes(SALT_SIZE)
    key = derive_key(password.encode('utf-8'), salt)
    nonce = get_random_bytes(NONCE_SIZE)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    with open(in_path, 'rb') as f:
        plaintext = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    with open(out_path, 'wb') as f:
        f.write(MAGIC)
        f.write(salt)
        f.write(nonce)
        f.write(tag)
        f.write(ciphertext)

    print(f"Encriptado: {in_path} -> {out_path}")

# --- Encriptar todos los archivos de la carpeta ---
def encrypt_all_in_folder(folder: str, password: str):
    encrypted_folder = os.path.join(folder, "encrypted")
    os.makedirs(encrypted_folder, exist_ok=True)

    for filename in os.listdir(folder):
        in_path = os.path.join(folder, filename)
        if os.path.isfile(in_path) and filename != os.path.basename(__file__):  # evitar auto-encriptar script
            out_path = os.path.join(encrypted_folder, filename + ".enc")
            encrypt_file(in_path, out_path, password)

    print("\n✅ Todos los archivos han sido encriptados en la carpeta 'encrypted'.")

# --- Punto de entrada ---
if __name__ == "__main__":
    current_folder = os.getcwd()
    encrypt_all_in_folder(current_folder, PASSWORD)
    input("\nPresiona ENTER para salir...")  # para que no se cierre la ventana al hacer doble clic
