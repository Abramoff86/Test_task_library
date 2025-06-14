from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.auth import get_current_user


from app.backend.db_depends import get_db
from app.schemas import CreateBook
from app.models.book import Book


router = APIRouter(prefix='/books', tags=['books'])


@router.get('/')
async def get_all_books(db: Annotated[AsyncSession, Depends(get_db)]):
    books = await db.scalars(select(Book).where(Book.stock > 0))
    if books:
        return books.all()

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='There are no books'
    )

@router.get('/{book_id}')
async def get_all_books(db: Annotated[AsyncSession, Depends(get_db)], book_id: int):
    book = await db.scalar(select(Book).where(Book.id == book_id, Book.stock > 0))
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return book


@router.post('/')
async def create_books(db: Annotated[AsyncSession, Depends(get_db)], create_book: CreateBook, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user:
        if create_book.ISBN:
            ISBN_book = await db.scalar(select(Book).where(Book.ISBN == create_book.ISBN))
            if ISBN_book:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='ISBN already exists'
                )
        if create_book.stock < 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='the number cannot be less than 0'
            )
        await db.execute(insert(Book).values(name=create_book.name,
                                            author=create_book.author,
                                            release_year=create_book.release_year,
                                            ISBN=create_book.ISBN,
                                            stock=create_book.stock,
                                             ))
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




@router.delete('/detail/{book_id}')
async def delete_books(db: Annotated[AsyncSession, Depends(get_db)], book_id: int,
                         get_user: Annotated[dict, Depends(get_current_user)]):
    book_delete = await db.scalar(select(Book).where(Book.id == book_id))
    if book_delete is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no book found'
             )
    if get_user:
        await db.delete(book_delete)
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Book delete is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have not enough permission for this action'
        )

@router.put('/detail/{book_id}')
async def update_product(db: Annotated[AsyncSession, Depends(get_db)], book_id: int,
                         update_book_model: CreateBook, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user:
        if update_book_model.ISBN:
            ISBN_book = await db.scalar(select(Book).where(Book.ISBN == create_book.ISBN))
            if ISBN_book:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='ISBN already exists'
                )
        if update_book_model.stock < 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='the number cannot be less than 0'
            )
        book_update = await db.scalar(select(Book).where(Book.id == book_id))
        if book_update is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no book found'
            )
        book_update.name = update_book_model.name
        book_update.author = update_book_model.author
        book_update.release_year = update_book_model.release_year
        book_update.ISBN = update_book_model.ISBN
        book_update.stock = update_book_model.stock

        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Book update is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have not enough permission for this action'
        )
