from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: Optional[int]
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int

    class Config:
        schema_extra = {
            'example': {
                'title': 'A New Book',
                'author': 'CodingWithFrancine',
                'description': 'A New description of a book',
                'rating': 5,
                'published_date': '2012'

            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'CodingWithRoby', 'A very nice book', 5, 2019),
    Book(2, 'Be Fast With FastAPI', 'CodingWithRoby', 'A great book', 5, 2019),
    Book(3, 'Master With Endpoints', 'CodingWithRoby', 'An awesome book', 5, 2020),
    Book(4, 'HP1', 'Author1', 'Book Description 1', 2, 2020),
    Book(5, 'HP2', 'Author2', 'Book Description 2', 3, 2022),
    Book(6, 'HP3', 'Author3', 'Book Description 3', 4, 2023),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
async def read_by_book_by_rating(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
        return books_to_return


@app.get("/books/publish/")
async def find_book_by_published_date(published_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    print(type(new_book))
    BOOKS.append(new_book)


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    # This code has the same meaning as below:
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1

    return book


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
