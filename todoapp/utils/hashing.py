from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def generate_password_hash(raw: str) -> str:
    return password_context.hash(raw)


def check_password_hash(raw: str, hashed: str) -> bool:
    return password_context.verify(raw, hashed)
