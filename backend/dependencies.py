from models import db, User
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError


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
) -> User:
    """
    Dependency que valida o JWT e retorna o usuario logado.
    Decodifica o `sub` gravado por create_token (auth_routes.create_token).
    """
    # Importado aqui dentro para evitar import circular com main.py.
    from main import SECRET_KEY, ALGORITHM

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except (JWTError, ValueError):
        raise credentials_exception

    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user
