# pip install pycryptodome
# python encrypt_file.py picture.jpg picture.jpg.enc -p "password"
# python tests/encryption/encrypt_file.py tests/encryption/picture.jpg tests/encryption/picture.jpg.enc -p "password"
# !/usr/bin/env python3 encrypt_file.py picture.jpg picture.jpg.enc -p "password"
"""
Encrypt a file (e.g. image) with a password using AES-256-GCM.
Output file format: b"ENCR" + salt(16) + nonce(12) + tag(16) + ciphertext
"""

import argparse
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

MAGIC = b"ENCR"          # 4 bytes marker
SALT_SIZE = 16           # for PBKDF2
NONCE_SIZE = 12          # recommended for GCM
KEY_LEN = 32             # 256-bit AES
PBKDF2_ITERS = 200_000  # iterations (tune for your platform)

def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=KEY_LEN, count=PBKDF2_ITERS, hmac_hash_module=None)

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

    print(f"Encrypted {in_path} -> {out_path}")

def main():
    ap = argparse.ArgumentParser(description="Encrypt a file with a password (AES-256-GCM)")
    ap.add_argument("input", help="input file (e.g. picture.jpg)")
    ap.add_argument("output", help="output encrypted file")
    ap.add_argument("-p", "--password", required=True, help="password (use a strong one)")
    args = ap.parse_args()
    encrypt_file(args.input, args.output, args.password)

if __name__ == "__main__":
    main()
