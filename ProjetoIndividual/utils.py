import hashlib
import os

ITERATIONS = 200_000
ALGORITHM = "sha256"
SECRET = "2e4a57467ba7e772bbdc2cbb4bc905122fd28eb295f0529f4707a62157862c6a"


def hash_password(password: str) -> str:
    salt = SECRET.encode()
    return hashlib.pbkdf2_hmac(ALGORITHM, password.encode(), salt, ITERATIONS).hex()


def verify_password(password: str, hashed_password: str) -> bool:
    salt = SECRET.encode()
    current_hashed_password = hashlib.pbkdf2_hmac(
        ALGORITHM, password.encode(), salt, ITERATIONS
    ).hex()
    return hashed_password == current_hashed_password


def generate_rand_token() -> str:
    return hashlib.sha256(os.urandom(32)).hexdigest()


def must_be_int(value: int | None) -> int:
    if value is None:
        raise ValueError("Valor deve ser um inteiro")
    return value
