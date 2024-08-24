from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookContent(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    review_text: str
    rating: int


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    book_id: int
    user_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str
