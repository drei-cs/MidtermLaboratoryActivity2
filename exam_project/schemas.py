from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Category Schemas
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Category name cannot be empty")
        return value


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Book Schemas
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=1, max_length=20)
    publication_year: Optional[int] = Field(
        default=None, ge=1, le=9999
    )
    stock_quantity: int = Field(default=1, ge=0)
    category_id: int = Field(..., gt=0)

    @field_validator("title", "isbn")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value


class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str
    publication_year: Optional[int] = None
    stock_quantity: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)