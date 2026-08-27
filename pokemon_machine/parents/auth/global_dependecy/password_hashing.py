from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# bcrypt has a hard 72-byte limit on password length
_BCRYPT_MAX_BYTES = 72


def _hash_password(password: str) -> str:
    truncated = password.encode("utf-8")[:_BCRYPT_MAX_BYTES]
    return pwd_context.hash(truncated)


def _verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    truncated = plain_password.encode("utf-8")[:_BCRYPT_MAX_BYTES]
    return pwd_context.verify(truncated, hashed_password)


# ERROR IS HERE