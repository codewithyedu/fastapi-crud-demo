from fastapi import APIRouter, HTTPException, status
from uuid import uuid4

from . import schemas


# Temporary in-memory list to store users
users: list[schemas.User] = []

router = APIRouter()


@router.post("/users", response_model=schemas.User)
def create_user(payload: schemas.UserCreate):
    new_user = payload.model_dump()
    username = new_user["name"]

    for user in users:

        if user["name"] == username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

    new_user["id"] = str(uuid4())

    # Simulate password hashing (use proper hashing in production)
    hashed_password = new_user["password"] + "added_some_hash"
    new_user["password"] = hashed_password

    users.append(new_user)

    return new_user


@router.get("/", response_model=list[schemas.User])
def get_users():
    return users


@router.get("/users/{id}", response_model=schemas.User)
def get_user(id: str):

    for user in users:

        if user["id"] == id:
            return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/users/{id}", response_model=schemas.User)
def update_user(id: str, payload: schemas.UserUpdate):

    for user in users:

        if user["id"] == id:
            new_name = payload.name
            user["name"] = new_name
            return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str):

    for idx, user in enumerate(users):

        if user["id"] == id:
            users.pop(idx)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
