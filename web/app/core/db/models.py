from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), unique=True, nullable=False)
    created = Column(DateTime(), server_default=func.now())


class File(Base):
    __tablename__ = 'user_files'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    full_text = Column(Text, nullable=False)
    hash = Column(String(256), nullable=False)
    path_to_pdf = Column(String(1024))
    created = Column(DateTime(), server_default=func.now())
    updated = Column(DateTime(), onupdate=func.now())
