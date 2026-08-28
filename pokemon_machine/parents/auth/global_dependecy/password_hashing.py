from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()  # parameter default sudah cukup aman, bisa di-tune


def _hash_password(password: str) -> str:
    return ph.hash(password)


def _verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False