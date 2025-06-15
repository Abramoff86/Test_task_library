from datetime import date
from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, Boolean, Date


class Borrow(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey('readerms.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    borrow_date = Column(Date, default=date.today())
    return_date = Column(Date, default=None)
    is_active = Column(Boolean, default=True)