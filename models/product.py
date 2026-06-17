from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, Numeric, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.category import Category
    from models.order_item import OrderItem


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(String(200))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(Integer)

    # Relationships
    category: Mapped["Category"] = relationship(back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
