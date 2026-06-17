from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(max_length=200)
    price: Decimal = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    category_id: int = Field(gt=0)


class ProductRead(BaseModel):
    id: int
    name: str
    price: Decimal
    stock: int
    category_id: int

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=200)
    price: Optional[Decimal] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = Field(default=None, gt=0)
