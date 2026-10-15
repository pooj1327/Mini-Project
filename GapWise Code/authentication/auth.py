import bcrypt
from sqlalchemy.orm import Session
from database.models import User


# -----------------------------
# Password Functions
# -----------------------------

def hash_password(password: str) -> str:
    """
    Hash user password before storing in database.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify entered password.
    """
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


# -----------------------------
# User Functions
# -----------------------------

def get_user_by_email(db: Session, email: str):

    return db.query(User).filter(
        User.email == email
    ).first()


def create_user(
        db: Session,
        name: str,
        email: str,
        password: str
):

    hashed = hash_password(password)

    user = User(
        name=name,
        email=email,
        password=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user