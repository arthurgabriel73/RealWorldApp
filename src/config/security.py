from passlib.context import CryptContext


CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(password: str, hash_password: str) -> bool:
    return CRYPTO.verify(password, hash_password)


def generate_hash_password(password: str) -> str:
    return CRYPTO.hash(password)
