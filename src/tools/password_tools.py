import re
import uuid

from passlib.context import CryptContext

__crypto = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_password_strength(password: str) -> str:
    has_8_characters = len(password) >= 8
    has_at_least_one_digit = re.search(r"\d", password) is not None
    has_at_least_one_uppercase = re.search(r"[A-Z]", password) is not None
    has_at_least_one_lowercase = re.search(r"[a-z]", password) is not None
    has_at_least_one_symbol = (
            re.search(r"[ @!#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is not None
    )

    strong_password = all(
        [
            has_8_characters,
            has_at_least_one_digit,
            has_at_least_one_uppercase,
            has_at_least_one_lowercase,
            has_at_least_one_symbol
        ]
    )

    if not strong_password:
        raise ValueError(
            "Password must contain a minimum of 8 characters, at least "
            "one digit, one uppercase, one lowercase and one symbol"
        )
    return password


def verify_password(password: str, salt: str, hashed_password: str) -> bool:
    return __crypto.verify(password + salt, hashed_password)


def get_salt() -> str:
    return uuid.uuid4().hex


def get_hash(string: str) -> str:
    return __crypto.hash(string)
