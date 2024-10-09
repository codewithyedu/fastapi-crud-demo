from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from . import schemas, crud, models
from .db import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users", response_model=schemas.User)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_name(db=db, user_name=payload.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with same username already exists",
        )

    new_user = crud.create_user(db=db, user=payload)
    return new_user


@router.get("/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@router.get("/users/{id}", response_model=schemas.User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.put("/users/{id}", response_model=schemas.User)
def update_user(
    user_id: str, payload: schemas.UserUpdate, db: Session = Depends(get_db)
):
    if crud.get_user_by_name(db=db, user_name=payload.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with same username already exists",
        )

    db_user = crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = crud.update_user(db=db, user=db_user, payload=payload)

    return updated_user


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    crud.delete_user(user=db_user, db=db)
