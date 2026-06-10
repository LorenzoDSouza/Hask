from models import User


class UserRepository:
    """Acesso a dados da entidade User. Sem regra de negocio."""

    def __init__(self, session):
        self.session = session

    def get_by_id(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def email_exists(self, email: str, exclude_id: int | None = None) -> bool:
        query = self.session.query(User).filter(User.email == email)
        if exclude_id is not None:
            query = query.filter(User.id != exclude_id)
        return query.first() is not None

    def list_all(self):
        return self.session.query(User).all()

    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def save(self, user: User) -> User:
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
