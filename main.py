from fastapi import FastAPI, HTTPException
from database import BookDataBase
from data_model import BookCreate, Book

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup
    db = BookDataBase()
    try:
        db.create_table()
        print("Database table created successfully!")
    finally:
        db.close_connection()
    yield
    # Application shutdown
    print("FastAPI application is shutting down...")


app = FastAPI()


@app.get("/")
def read_root():
    return {"Message": "Welcome to CRUD API "}


@app.get("/allBooks")
def get_all_books():
    book_db = BookDataBase()
    try:
        books = book_db.get_book()
        return {"Books": books}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to get books: {str(e)}")
    finally:
        book_db.close_connection()


# CREATE BOOK
@app.post("/create_book")
def create_new_book(book: BookCreate):
    book_db = BookDataBase()
    try:
        book_id = book_db.create_book(book)
        return {"Message": "Book created successfully", "Book ID": book_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Book not created: {str(e)}")
    finally:
        book_db.close_connection()


@app.get("/book/{book_id}")
def get_book_by_id(book_id: int):

    book_db = BookDataBase()
    try:
        book = book_db.get_book_withid(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        return {"Message": "Book found successfully", "Book": book}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        book_db.close_connection()


@app.put("/updated_book/{book_id}")
def update_book_details(book_id: int, book: BookCreate):
    book_db = BookDataBase()
    try:
        # check wherter book exists
        existing_book = book_db.get_book_withid(book_id)
        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        # updated the book detaisl
        result = book_db.updated_book(book_id, book.title, book.author)
        if result == 0:
            raise HTTPException(status_code=404, detail="Book not updated")
        return {
            "Message": "Book updated successfully",
            "Book ID": book_id,
            "Title": book.title,
            "Author": book.author,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        book_db.close_connection()


# DELETE BOOK
@app.delete("/remove_book/{book_id}")
def delete_books(book_id: int):
    book_db = BookDataBase()
    try:
        result = book_db.remove_book(book_id)
        if result == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"Message": "Book deleted successfully", "Book ID": book_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Book not deleted: {str(e)}")

    finally:
        book_db.close_connection()
