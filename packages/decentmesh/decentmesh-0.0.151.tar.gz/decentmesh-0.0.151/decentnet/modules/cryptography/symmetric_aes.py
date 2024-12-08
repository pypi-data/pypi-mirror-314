import concurrent.futures
import warnings
from typing import Optional

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from argon2.low_level import Type, hash_secret

from decentnet.consensus.beam_constants import DEFAULT_AES_SALT_SIZE, BEAM_AES_ENCRYPTION_KEY_SIZE, \
    DEFAULT_AES_GCM_NONCE_SIZE


class AESCipher:
    def __init__(self, password: bytes, key_size: int = BEAM_AES_ENCRYPTION_KEY_SIZE,
                 salt: Optional[bytes] = None):
        """
        Initializes the AESCipher with key reuse, nonce optimization, and optional salt.
        Warns if AES-NI is not enabled.
        """
        if key_size not in (128, 192, 256):
            raise ValueError("Key size must be 128, 192, or 256 bits.")

        self.password = password
        self.key_size = key_size
        self.salt = salt if salt is not None else get_random_bytes(DEFAULT_AES_SALT_SIZE)
        self.key = AESCipher.derive_key(password, self.salt, key_size)  # Precompute key

        if not AESCipher.is_aes_ni_enabled():
            warnings.warn(
                "AES-NI hardware acceleration is not enabled. "
                "Performance may be suboptimal. Ensure your environment supports it."
            )

    @staticmethod
    def derive_key(password: bytes, salt: bytes, key_length: int) -> bytes:
        """
        Derives a cryptographic key using Argon2 with optimized parameters.
        """
        return hash_secret(
            password,
            salt,
            time_cost=1,  # Lower time cost for faster derivation
            memory_cost=8,  # Balanced memory usage
            parallelism=1,  # Single-threaded for simplicity
            hash_len=key_length // 8,
            type=Type.ID  # Argon2id
        )

    @staticmethod
    def is_aes_ni_enabled() -> bool:
        """
        Checks if AES-NI is enabled on the system.
        """
        try:
            with open("/proc/cpuinfo", "r") as cpuinfo:
                return "aes" in cpuinfo.read()
        except FileNotFoundError:
            return False  # Assume AES-NI is not available if /proc/cpuinfo is inaccessible

    def encrypt_chunk(self, chunk: bytes) -> bytes:
        """
        Encrypts a single chunk using AES-GCM.
        """
        nonce = get_random_bytes(DEFAULT_AES_GCM_NONCE_SIZE)  # GCM nonce size
        cipher = AES.new(self.key[:self.key_size // 8], AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(chunk)
        return nonce + tag + ciphertext

    def decrypt_chunk(self, chunk: bytes) -> bytes:
        """
        Decrypts a single chunk using AES-GCM.
        """
        nonce = chunk[:DEFAULT_AES_GCM_NONCE_SIZE]
        tag = chunk[DEFAULT_AES_GCM_NONCE_SIZE:28]
        ciphertext = chunk[28:]
        cipher = AES.new(self.key[:self.key_size // 8], AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)

    def encrypt(self, plaintext: bytes, chunk_size: int = 1024 * 1024) -> bytes:
        """
        Encrypts data, parallelizing only if the plaintext size exceeds 1 MB.
        """
        if len(plaintext) <= chunk_size:  # Small data, encrypt in a single chunk
            return self.encrypt_chunk(plaintext)

        # For large data, split into chunks and process in parallel
        chunks = [plaintext[i:i + chunk_size] for i in range(0, len(plaintext), chunk_size)]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            encrypted_chunks = executor.map(self.encrypt_chunk, chunks)
        return b"".join(encrypted_chunks)

    def decrypt(self, encrypted_data: bytes, chunk_size: int = 1024 * 1024 + 28) -> bytes:
        """
        Decrypts data, parallelizing only if the encrypted data size exceeds 1 MB.
        """
        if len(encrypted_data) <= chunk_size:  # Small data, decrypt in a single chunk
            return self.decrypt_chunk(encrypted_data)

        # For large data, split into chunks and process in parallel
        chunks = [encrypted_data[i:i + chunk_size] for i in range(0, len(encrypted_data), chunk_size)]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            decrypted_chunks = executor.map(self.decrypt_chunk, chunks)
        return b"".join(decrypted_chunks)
