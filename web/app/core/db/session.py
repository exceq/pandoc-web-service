from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
DB_PORT = getenv("DB_PORT")

db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:{DB_PORT}/{POSTGRES_DB}"
print(db_url)
engine = create_engine(db_url, echo='debug')
session = sessionmaker(engine)
