from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int


BOOKS = [
    Book(1, 'Computer Science Pro', 'CodingWithRoby', 'A very nice book', 5),
    Book(2, 'Be Fast With FastAPI', 'CodingWithRoby', 'A great book', 5),
    Book(3, 'Master With Endpoints', 'CodingWithRoby', 'An awesome book', 5),
    Book(4, 'HP1', 'Author1', 'Book Description 1', 2),
    Book(5, 'HP2', 'Author2', 'Book Description 2', 3),
    Book(6, 'HP3', 'Author3', 'Book Description 3', 4),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    print(type(new_book))
    BOOKS.append(new_book)
