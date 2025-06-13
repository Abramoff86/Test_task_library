from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean



class Reader(Base):
    __tablename__ = 'readerms'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)