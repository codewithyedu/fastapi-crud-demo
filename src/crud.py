from sqlalchemy.orm import Session
from uuid import uuid4

from . import models, schemas


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.name == user_name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    user_id = str(uuid4())

    db_user = models.User(
        id=user_id,
        name=user.name,
        password=fake_hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.User, payload: schemas.UserUpdate):
    new_name = payload.name
    user.name = new_name
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: schemas.User):
    db.delete(user)
    db.commit()
