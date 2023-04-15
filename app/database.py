from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 'postgresql://<Username>:<Password>@<IP Address>/<hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:passwordofdatabase@localhost/postgres'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Dependency of Sqlalchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()