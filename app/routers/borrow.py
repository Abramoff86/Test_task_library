from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from app.models import Book, Reader
from app.routers.auth import get_current_user


from app.backend.db_depends import get_db
from app.schemas import CreateBorrow
from app.models.borrow import Borrow


router = APIRouter(prefix='/borrow', tags=['borrow'])



@router.post("/take")
async def create_borrow(db: Annotated[AsyncSession, Depends(get_db)], create_borrow: CreateBorrow, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user:
        book = await db.scalar(select(Book).where(Book.id == create_borrow.book_id, Book.stock > 0))
        if not book:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='The book is missing'
            )
        reader = await db.scalar(select(Reader).where(Reader.id == create_borrow.reader_id, Reader.is_active == True))
        if not reader:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='The reader is absent'
            )
        pool = await db.scalars(select(Borrow).where(Borrow.reader_id == create_borrow.reader_id, Borrow.is_active == True))
        if len(pool.all()) >= 3:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Maximum books taken'
            )

        await db.execute(insert(Borrow).values(reader_id=create_borrow.reader_id, book_id=create_borrow.book_id))

        book.stock = book.stock - 1

        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not authorized to use this method'
        )

@router.post("/return")
async def delete_borrow(db: Annotated[AsyncSession, Depends(get_db)], create_borrow: CreateBorrow, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user:
        book = await db.scalar(select(Book).where(Book.id == create_borrow.book_id))
        if not book:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='The book is missing'
            )
        reader = await db.scalar(select(Reader).where(Reader.id == create_borrow.reader_id, Reader.is_active == True))
        if not reader:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='The reader is absent'
            )

        brow = await db.scalar(select(Borrow).where(Borrow.reader_id == create_borrow.reader_id, Borrow.is_active == True, Borrow.book_id == create_borrow.book_id))
        if not brow:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Reservation found'
            )
        brow.is_active = False
        brow.return_date = date.today()

        book.stock = book.stock + 1

        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not authorized to use this method'
        )


@router.get("/take/{reader_id}")
async def get_all_books(db: Annotated[AsyncSession, Depends(get_db)], reader_id: int):
    reader = await db.scalar(select(Reader).where(Reader.id == reader_id))
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_40r_FORBIDDEN,
            detail='Reader not found'
        )
    bor = await db.scalars(select(Borrow.book_id).where(Borrow.is_active == True, Borrow.reader_id == reader_id))
    pool = bor.all()
    print(pool)
    if bor:
        book = await db.scalars(select(Book).where(Book.id.in_(pool)))
        return book.all()

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='There are no borrow'
    )