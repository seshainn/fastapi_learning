from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookUpdateModel, BookCreateModel
from sqlmodel import select
from .models import Book
import uuid

class BookService:

    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(Book.created_at.desc())
        result = await session.exec(statement)
        return result.all()
    
    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book else None
    async def create_a_book(self, book_data: BookCreateModel, session: AsyncSession):
        new_book = Book(**book_data)
        session.add(new_book)
        await session.commit()
        return new_book
    
    async def update_book(self, book_uid: uuid.UUID, book_update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        if not book_to_update:
            return None
        for field, value in book_update_data.model_dump().items():
            setattr(book_to_update, field, value)
        await session.commit()
        return book_to_update
    
    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if not book_to_delete:
            return None
        await session.delete(book_to_delete)
        await session.commit()
        return book_to_delete
        
