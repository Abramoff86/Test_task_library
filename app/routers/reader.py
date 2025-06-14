from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.auth import get_current_user


from app.backend.db_depends import get_db
from app.schemas import CreateReader
from app.models.reader import Reader


router = APIRouter(prefix='/readerms', tags=['readerms'])


@router.get('/')
async def get_all_readerms(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user:
        readerms = await db.scalars(select(Reader).where(Reader.is_active == True))
        if readerms:
            return readerms.all()

        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no readerms'
        )

@router.get('/{reader_id}')
async def get_reader(db: Annotated[AsyncSession, Depends(get_db)], reader_id: int, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user:
        reader = await db.scalar(select(Reader).where(Reader.id == reader_id, Reader.is_active == True))
        if reader is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Reader not found'
            )
        return reader


@router.post('/')
async def create_reader(db: Annotated[AsyncSession, Depends(get_db)], create_reader: CreateReader):
    reader = await db.scalar(select(Reader).where(Reader.email==create_reader.email))
    if reader:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='email already exists'
    )
    await db.execute(insert(Reader).values(username=create_reader.username,
                                            email=create_reader.email,
                                           ))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.delete('/{reader_id}')
async def delete_reader(db: Annotated[AsyncSession, Depends(get_db)], reader_id: int, get_user: Annotated[dict, Depends(get_current_user)]):
    reader = await db.scalar(select(Reader).where(Reader.id == reader_id, Reader.is_active == True))
    if reader is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no reader found'
             )
    if get_user:
        reader.is_active = False
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Product delete is successful'
        }







