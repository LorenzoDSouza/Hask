import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

# ----- Auth / JWT -----
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTE", "30"))

# ----- Frontend -----
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# ----- Password hashing -----
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
