from sqlalchemy     import create_engine, Column, String, Integer, ForeignKey, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import ChoiceType
from enum import Enum

#create the connection to the database engine
db = create_engine()#aqui dentro vai o endereço do banco, se for da aws coloca o link de la e se for local coloca de acordo com o banco

#create the base of the database
base = declarative_base()

#create class the classes/tables of the db
#users
#tasks

class User(base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Task(base):
    __tablename__ = "tasks"

    TASK_STATUS = (
        ("TODO", "TO DO"),
        ("IN_PROGRESS", "IN PROGRESS"),
        ("COMPLETED", "COMPLETED")
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False)
    status = Column("status", ChoiceType(choices=TASK_STATUS))
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    type = Column("type", String)

    def __init__(self, title, user_id, type, status="TO_DO"):
        self.title = title
        self.status = status
        self. user_id = user_id
        self.type = type
