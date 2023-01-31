from .models import User
from sqlmodel import Session, select


async def find_existed_user(user_id: str, db: Session) -> User | None:
    """
    A method to fetch a user info given an email.

    Args:
        email (EmailStr) : A given user email.
        session (AsyncSession) : SqlAlchemy session object.

    Returns:
        Dict[str, Any]: a dict object that contains info about a user.
    """
    user = db.get(User, user_id)
    return user


def get_user(email: str, db: Session) -> User | None:
    """
    A method to fetch a user info given an email.

    Args:
        email (EmailStr) : A given user email.
        session (AsyncSession) : SqlAlchemy session object.

    Returns:
        Dict[str, Any]: a dict object that contains info about a user.
    """
    statement = select(User).where(User.email == email)
    results = db.exec(statement)
    user = results.first()
    return user


async def create_user(user: User, db: Session) -> User:
    """
    A method to insert a user into the users table.

    Args:
        user (UserCreate) : A user schema object that contains all info about a user.
        session (AsyncSession) : SqlAlchemy session object.

    Returns:
        Result: Database result.
    """
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
