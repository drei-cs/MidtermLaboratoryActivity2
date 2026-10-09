from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

import models
import schemas
import crud
from database import engine, get_db


# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="Library Book Inventory API")


# 1. CREATE CATEGORY
@app.post(
    "/categories/",
    response_model=schemas.CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_category(db, category)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# 2. GET ALL CATEGORIES
@app.get(
    "/categories/",
    response_model=list[schemas.CategoryResponse]
)
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


# 3. CREATE BOOK
@app.post(
    "/books/",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    category = crud.get_category(db, book.category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category ID does not exist"
        )

    try:
        return crud.create_book(db, book)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# 4. GET ALL BOOKS WITH OPTIONAL CATEGORY FILTER
@app.get(
    "/books/",
    response_model=list[schemas.BookResponse]
)
def read_books(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if category_id is not None:
        if category_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid category ID"
            )

        category = crud.get_category(db, category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

    return crud.get_books(db, category_id)


# 5. GET BOOK BY ID
@app.get(
    "/books/{book_id}",
    response_model=schemas.BookResponse
)
def read_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = crud.get_book(db, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return book


# 6. UPDATE BOOK
@app.put(
    "/books/{book_id}",
    response_model=schemas.BookResponse
)
def update_book(
    book_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    existing_book = crud.get_book(db, book_id)

    if existing_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    category = crud.get_category(db, book.category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category ID does not exist"
        )

    try:
        return crud.update_book(
            db,
            book_id,
            book.model_dump()
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# 7. DELETE BOOK
@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_book(db, book_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return {"message": "Book deleted successfully"}