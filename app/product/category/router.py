from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from . import service
from .constants import ErrorCode
from .models import CategoryCreate, CategoryResponse

router = APIRouter()


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create(category_in: CategoryCreate, db: Session = Depends(get_db)):
    if service.get_by_title(db, title=category_in.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.CATEGORY_TITLE_ALREADY_EXISTS,
        )

    if service.get_by_slug(db, slug=category_in.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.CATEGORY_SLUG_ALREADY_EXISTS,
        )

    return service.create(db, category_in=category_in)
