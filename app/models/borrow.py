from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float


class Borrow(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey('readerms.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    is_active = Column(Boolean, default=True)