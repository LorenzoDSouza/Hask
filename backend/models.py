from sqlalchemy     import DateTime, create_engine, Column, String, Integer, ForeignKey, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import declarative_base, deferred
from dotenv import load_dotenv
from enum import Enum
import os

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

#create the connection to the database engine
db = create_engine(DATABASE_URL)
#create the base of the database
Base = declarative_base()

#create class the classes/tables of the db
#users
#tasks
class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False, unique=True)
    password = deferred(Column("password", String, nullable=False))

    # Google Calendar / OAuth integration. Preenchidos apos o fluxo OAuth.
    google_refresh_token = deferred(Column("google_refresh_token", String, nullable=True))
    calendar_connected = Column("calendar_connected", Boolean, nullable=False, default=False, server_default="false")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Task(Base):
    __tablename__ = "tasks"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False)
    status = Column(SQLAlchemyEnum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    category = Column("category", String)
    start_date_time = Column("start_date_time", DateTime, nullable=True)
    end_date_time = Column("end_date_time", DateTime, nullable=True)

    def __init__(self, title, user_id, category, start_date_time=None, end_date_time=None, status=TaskStatus.TODO):
        self.title = title
        self.status = status
        self.user_id = user_id
        self.category = category
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time