import bcrypt


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(),
    ).decode()

    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
