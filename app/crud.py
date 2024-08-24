from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import ollama
from app import models, schemas
from app.auth import get_password_hash
from app.models import User


async def create_book(db: AsyncSession, book: schemas.BookCreate):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)

    # Generate a summary using Llama3
    summary = ollama.chat("llama3", "Summarize this book: {book.title} authored by : {book.author}")
    new_book.summary = summary

    await db.commit()

    return new_book


async def get_books(db: AsyncSession):
    result = await db.execute(select(models.Book))
    return result.scalars().all()


async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Book).filter(models.Book.id == book_id))
    return result.scalar_one_or_none()


async def update_book(db: AsyncSession, book_id: int, book: schemas.BookUpdate):
    book_db = await get_book(db, book_id)
    if book_db:
        for key, value in book.model_dump().items():
            setattr(book_db, key, value)
        await db.commit()
        await db.refresh(book_db)
        return book_db
    return None


async def delete_book(db: AsyncSession, book_id: int):
    book_db = await get_book(db, book_id)
    if book_db:
        await db.delete(book_db)
        await db.commit()
        return True
    return False


async def add_review(db: AsyncSession, review: schemas.ReviewCreate, book_id: int, user_id: int):
    new_review = models.Review(**review.dict(), book_id=book_id, user_id=user_id)
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review


async def get_reviews(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Review).filter(models.Review.book_id == book_id))
    return result.scalars().all()


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def create_user(db: AsyncSession, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
