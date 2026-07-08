from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import Book, BookUpdateModel
from src.books.service import BookService
from src.db.main import get_session
import uuid
from src.auth.dependencies import AccessTokenBearer

router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()

@router.get("/", response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_details: dict = Depends(access_token_bearer),
) -> List[Book]:
    books = await book_service.get_all_books(session)
    return books

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(
    book_data: Book, 
    session: AsyncSession = Depends(get_session),
    user_details: dict = Depends(access_token_bearer)
) -> dict:
    new_book = book_data.model_dump()
    await book_service.create_a_book(new_book, session)
    return new_book

@router.get("/{book_uid}", response_model=Book)
async def get_book(
    book_uid: uuid.UUID, 
    session: AsyncSession = Depends(get_session), 
    user_details: dict = Depends(access_token_bearer)
) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@router.patch("/{book_uid}", response_model=Book)
async def update_book(
    book_uid: uuid.UUID, 
    book_update_data: BookUpdateModel, 
    session: AsyncSession = Depends(get_session), 
    user_details: dict = Depends(access_token_bearer)
) -> dict:
    book = await book_service.update_book(book_uid, book_update_data, session)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: uuid.UUID, 
    session: AsyncSession = Depends(get_session),
    user_details: dict = Depends(access_token_bearer)
):
    book = await book_service.delete_book(book_id, session)
    if book:
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

