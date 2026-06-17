import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product
from schemas.product import ProductCreate, ProductRead, ProductUpdate
from settings.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


@router.get(
    path="/",
    response_model=list[ProductRead],
    tags=["Products"],
)
async def get_products(session: SessionDepend):
    try:
        result = await session.execute(select(Product))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get products")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get products",
        ) from exc


@router.get(
    path="/{product_id}",
    response_model=ProductRead,
    tags=["Products"],
)
async def get_product(product_id: int, session: SessionDepend):
    try:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        return product

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get product with id %d", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get product",
        ) from exc


@router.post(
    path="/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
)
async def create_product(product_data: ProductCreate, session: SessionDepend):
    try:
        new_product = Product(**product_data.model_dump())
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        return new_product

    except HTTPException:
        raise
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error: check if category_id exists.",
        ) from exc
    except Exception as exc:
        logger.exception("Failed to create product")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product",
        ) from exc


@router.put(
    path="/{product_id}",
    response_model=ProductRead,
    tags=["Products"],
)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: SessionDepend,
):
    try:
        result = await session.execute(select(Product).where(Product.id == product_id))
        existing_product = result.scalars().first()

        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        for field, value in product_update.model_dump(exclude_unset=True).items():
            setattr(existing_product, field, value)

        session.add(existing_product)
        await session.commit()
        await session.refresh(existing_product)
        return existing_product

    except HTTPException:
        raise
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error: check if category_id exists.",
        ) from exc
    except Exception as exc:
        logger.exception("Failed to update product with id %s", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product",
        ) from exc


@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Products"],
)
async def delete_product(product_id: int, session: SessionDepend):
    try:
        result = await session.execute(select(Product).where(Product.id == product_id))
        existing_product = result.scalars().first()

        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        await session.delete(existing_product)
        await session.commit()
        return None

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to delete product with id %s", product_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product",
        ) from exc
