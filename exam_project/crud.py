from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Category, Book
from schemas import CategoryCreate, BookCreate


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.model_dump())
    db.add(db_category)

    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Category name already exists") from exc


def get_categories(db: Session):
    return db.query(Category).order_by(Category.id).all()


def get_category(db: Session, category_id: int):
    return (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )


def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.model_dump())
    db.add(db_book)

    try:
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError as exc:
        db.rollback()
        raise ValueError(
            "ISBN already exists or invalid book data"
        ) from exc


def get_books(db: Session, category_id: int | None = None):
    query = db.query(Book)

    if category_id is not None:
        query = query.filter(Book.category_id == category_id)

    return query.order_by(Book.id).all()


def get_book(db: Session, book_id: int):
    return (
        db.query(Book)
        .filter(Book.id == book_id)
        .first()
    )


def update_book(db: Session, book_id: int, book_data: dict):
    db_book = get_book(db, book_id)

    if db_book is None:
        return None

    for key, value in book_data.items():
        setattr(db_book, key, value)

    try:
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError as exc:
        db.rollback()
        raise ValueError(
            "Duplicate ISBN or invalid book data"
        ) from exc


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)

    if db_book is None:
        return False

    db.delete(db_book)
    db.commit()
    return True