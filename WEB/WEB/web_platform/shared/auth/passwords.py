from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordHash:
    algo: str
    salt_hex: str
    iterations: int
    hash_hex: str

    def serialize(self) -> str:
        return f"{self.algo}${self.iterations}${self.salt_hex}${self.hash_hex}"

    @staticmethod
    def parse(value: str) -> "PasswordHash":
        algo, iters, salt_hex, hash_hex = value.split("$", 3)
        return PasswordHash(algo=algo, iterations=int(iters), salt_hex=salt_hex, hash_hex=hash_hex)


def hash_password(password: str, iterations: int = 200_000) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    ph = PasswordHash(algo="pbkdf2_sha256", salt_hex=salt.hex(), iterations=iterations, hash_hex=dk.hex())
    return ph.serialize()


def verify_password(password: str, stored: str) -> bool:
    ph = PasswordHash.parse(stored)
    if ph.algo != "pbkdf2_sha256":
        return False
    salt = bytes.fromhex(ph.salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ph.iterations)
    return hmac.compare_digest(dk.hex(), ph.hash_hex)


