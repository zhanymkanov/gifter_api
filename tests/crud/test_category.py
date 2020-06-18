from sqlalchemy.orm import Session

from app import crud
from app.schemas.category import CategoryCreate, CategoryUpdate
from tests.utils import random_lower_string


def test_category_create(db: Session) -> None:
    title, slug = random_lower_string(), random_lower_string()
    category_in = CategoryCreate(title=title, slug=slug)
    category = crud.category.create(db=db, obj_in=category_in)

    assert category.id is not None
    assert category.title == title
    assert category.slug == slug
    crud.category.remove(db=db, id=category.id)


def test_category_get(db: Session) -> None:
    title, slug = random_lower_string(), random_lower_string()
    category_in = CategoryCreate(title=title, slug=slug)

    category = crud.category.create(db=db, obj_in=category_in)
    category_stored = crud.category.get(db=db, id=category.id)

    assert category.id == category_stored.id
    assert category.slug == category_stored.slug
    assert category.created_at == category_stored.created_at
    crud.category.remove(db=db, id=category.id)


def test_category_update(db: Session) -> None:
    title, slug = random_lower_string(), random_lower_string()
    new_title, new_slug = random_lower_string(), random_lower_string()

    category_in = CategoryCreate(title=title, slug=slug)
    category_updated = CategoryUpdate(title=new_title, slug=new_slug)

    category = crud.category.create(db=db, obj_in=category_in)
    old_updated_at = category.updated_at

    crud.category.update(db=db, db_obj=category, obj_in=category_updated)
    new_updated_at = category.updated_at

    assert category.title == new_title
    assert category.slug == new_slug
    assert new_updated_at > old_updated_at
    crud.category.remove(db=db, id=category.id)


def test_category_remove(db: Session) -> None:
    title, slug = random_lower_string(), random_lower_string()
    category_in = CategoryCreate(title=title, slug=slug)

    category = crud.category.create(db=db, obj_in=category_in)
    category_removed = crud.category.remove(db=db, id=category.id)

    assert crud.category.get(db=db, id=category_removed.id) is None
    assert category.id == category_removed.id
