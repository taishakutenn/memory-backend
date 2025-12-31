import os

from dotenv import load_dotenv

load_dotenv()

# База данных
DATABASE_URL=os.getenv("DATABASE_URL")
DATABASE_URL_ALEMBIC=os.getenv("DATABASE_URL_ALEMBIC")
DATABASE_USER=os.getenv("DATABASE_USER")
DATABASE_PORT=os.getenv("DATABASE_PORT")
DATABASE_BD_NAME=os.getenv("DATABASE_BD_NAME")
DATABASE_PASS=os.getenv("DATABASE_PASS")

# Jwt, безапосность
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))