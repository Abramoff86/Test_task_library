from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship

from app.backend.db import Base


class Borrow(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True, index=True)
    readerm_id = Column(Integer, ForeignKey('readerms.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    is_active = Column(Boolean, default=True)