from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, CheckConstraint



class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    author = Column(String)
    release_year = Column(Integer)
    ISBN = Column(String, unique=True, default = '')
    stock = Column(Integer, CheckConstraint("stock >= 0"))

