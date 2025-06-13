from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean



class Librarian(Base):
    __tablename__ = 'librarians'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
