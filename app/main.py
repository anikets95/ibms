from typing import List

import ollama
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, crud, database

app = FastAPI()


@app.post("/books", response_model=schemas.Book)
async def add_book(book: schemas.BookCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_book(db, book)


@app.get("/books", response_model=List[schemas.Book])
async def get_all_books(db: AsyncSession = Depends(database.get_db)):
    return await crud.get_books(db)


@app.get("/books/{book_id}", response_model=schemas.Book)
async def get_book(book_id: int, db: AsyncSession = Depends(database.get_db)):
    book = await crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(book_id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(database.get_db)):
    updated_book = await crud.update_book(db, book_id, book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(database.get_db)):
    success = await crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}


@app.post("/books/{book_id}/reviews", response_model=schemas.Review)
async def add_review(book_id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.add_review(db, review, book_id, user_id=1)


@app.get("/books/{book_id}/reviews", response_model=List[schemas.Review])
async def get_reviews(book_id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_reviews(db, book_id)


@app.get("/books/{book_id}/summary")
async def get_summary_and_rating(book_id: int, db: AsyncSession = Depends(database.get_db)):
    book = await crud.get_book(db, book_id)
    reviews = await crud.get_reviews(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    rating = sum([review.rating for review in reviews]) / len(reviews) if reviews else 0

    return {"summary": book.summary, "rating": rating}


@app.post("/recommendations")
async def generate_summary(book_content: schemas.BookCreate):
    # Call to Llama3 model for generating the summary can go here
    pass


@app.post("/generate-summary")
async def generate_summary(book: schemas.BookContent):
    try:
        # Connect to the locally running Llama3 model via Ollama
        result = ollama.chat("llama3",
                             f"Summarize this book: {book.title} authored by : {book.author}")
        return {"summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/register")
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_user(db, user.username, user.password)
