from models import db
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from security import decode_token
from src.repositories.user_repository import UserRepository


def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


# Extrai o token "Bearer <token>" do header Authorization. O tokenUrl aponta
# para /auth/token (form-data), que e o que o botao "Authorize" do Swagger usa.
# O frontend continua usando /auth/login (JSON).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    """Valida o JWT e retorna o usuario logado (sub = user_id)."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = decode_token(token)
    if user_id is None:
        raise credentials_exception

    user = UserRepository(session).get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user
