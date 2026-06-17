from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.order import Order


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(20))
    hashed_password: Mapped[str] = mapped_column(String(200), server_default="")
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    role: Mapped[str] = mapped_column(String(20), default="user", server_default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationships
    orders: Mapped[List["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
