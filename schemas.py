# from pydantic import BaseModel

# class Book(BaseModel):
#     title: str
#     number_of_pages: int

# class Author(BaseModel):
#     first_name: str
#     last_name: str

# class BookAuthorPayload(BaseModel):
#     book: Book
#     author: Author

from pydantic import BaseModel

# Request models
class Book(BaseModel):
    title: str
    number_of_pages: int

class Author(BaseModel):
    first_name: str
    last_name: str

class BookAuthorPayload(BaseModel):
    book: Book
    author: Author

# Response models
class BookResponse(BaseModel):
    title: str
    number_of_pages: int

class AuthorResponse(BaseModel):
    first_name: str
    last_name: str

class BookAuthorResponse(BaseModel):
    book: BookResponse
    author: AuthorResponse

# Update model
class BookUpdate(BaseModel):
    title: str
    number_of_pages: int
