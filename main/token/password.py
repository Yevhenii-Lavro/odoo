from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(entered_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(entered_password, hashed_password)


def get_password_hash(entered_password: str) -> str:
    return pwd_context.hash(entered_password)
