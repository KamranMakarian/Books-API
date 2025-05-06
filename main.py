from fastapi import FastAPI, HTTPException
import schemas
import database
from typing import List

app = FastAPI()

@app.get("/") # Home route is always defined as a slash
def get_root():
    return "Welcome to the books api!"

@app.post("/book/")
def create_book(request: schemas.BookAuthorPayload):
    try:
        database.add_book(convert_into_book_db_model(request.book), convert_into_author_db_model(request.author))
        return {
            "message": "New book and author added",
            "book": {
                "title": request.book.title,
                "pages": request.book.number_of_pages
            },
            "author": {
                "first_name": request.author.first_name,
                "last_name": request.author.last_name
            }
        }
    except ValueError as e:
        # Handle known validation errors (like duplicates)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch anything unexpected
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/book/{book_id}", response_model=schemas.BookAuthorResponse)
def get_book(book_id: int):
    try:
        book_info = database.get_book(book_id)
        if book_info is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book_info
    except HTTPException:
        raise  # let FastAPI handle it as-is
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    
@app.get("/books", response_model=List[schemas.BookAuthorResponse])
def get_all_books():
    return database.get_all_books()

@app.put("/book/{book_id}", response_model=schemas.BookAuthorResponse)
def update_book(book_id: int, request: schemas.BookUpdate):
    try:
        updated = database.update_book(
            book_id,
            new_title=request.title,
            new_pages=request.number_of_pages
        )
        if updated is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    try:
        deleted = database.delete_book(book_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": f"Book {book_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/books/search", response_model=List[schemas.BookAuthorResponse])
def search_books(title: str):
    try:
        return database.search_books_by_title(title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# Request payload schema is in schemas.py file and database book schema is defined in database.py.
# Therefore we have to convert the request data to database schema format.

def convert_into_book_db_model(book: schemas.Book) -> database.Book:
    return database.Book(title=book.title, number_of_pages=book.number_of_pages)

def convert_into_author_db_model(author: schemas.Author) -> database.Author:
    return database.Author(first_name=author.first_name, last_name=author.last_name)