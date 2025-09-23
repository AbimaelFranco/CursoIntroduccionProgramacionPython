#!/usr/bin/env python3
# python decrypt_file.py picture.jpg.enc picture_restored.jpg -p "MyStrongPassword123!"
# python tests/encryption/decrypt_file.py tests/encryption/picture.jpg.enc tests/encryption/picture_restored.jpg -p "password"
"""
Decrypt a file created by encrypt_file.py
Expects file format: b"ENCR" + salt(16) + nonce(12) + tag(16) + ciphertext
"""

import argparse
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

MAGIC = b"ENCR"
SALT_SIZE = 16
NONCE_SIZE = 12
TAG_SIZE = 16
KEY_LEN = 32
PBKDF2_ITERS = 200_000

def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=KEY_LEN, count=PBKDF2_ITERS, hmac_hash_module=None)

def decrypt_file(in_path: str, out_path: str, password: str):
    with open(in_path, 'rb') as f:
        data = f.read()

    if len(data) < 4 + SALT_SIZE + NONCE_SIZE + TAG_SIZE:
        raise ValueError("Input file too small or corrupt")

    off = 0
    magic = data[off:off+4]; off += 4
    if magic != MAGIC:
        raise ValueError("File does not appear to be encrypted by this tool (bad magic)")

    salt = data[off:off+SALT_SIZE]; off += SALT_SIZE
    nonce = data[off:off+NONCE_SIZE]; off += NONCE_SIZE
    tag = data[off:off+TAG_SIZE]; off += TAG_SIZE
    ciphertext = data[off:]

    key = derive_key(password.encode('utf-8'), salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError as e:
        raise ValueError("Decryption failed. Wrong password or file corrupted.") from e

    with open(out_path, 'wb') as f:
        f.write(plaintext)

    print(f"Decrypted {in_path} -> {out_path}")

def main():
    ap = argparse.ArgumentParser(description="Decrypt a file encrypted with AES-256-GCM")
    ap.add_argument("input", help="input encrypted file")
    ap.add_argument("output", help="output (decrypted) file")
    ap.add_argument("-p", "--password", required=True, help="password used to encrypt")
    args = ap.parse_args()
    decrypt_file(args.input, args.output, args.password)

if __name__ == "__main__":
    main()
