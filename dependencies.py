from models import db
from sqlalchemy.orm import sessionmaker

def get_session():
    Session = sessionmaker(bind=db)
    return Session()
