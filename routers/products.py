import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from settings.db import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductRead, ProductUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]
