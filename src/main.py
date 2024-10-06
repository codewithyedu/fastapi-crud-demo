from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from uuid import uuid4


app = FastAPI()


# Base model for User containing common fields
class UserBase(BaseModel):
    name: str


# Model used for updating user, inherits from UserBase (just name)
class UserUpdate(UserBase):
    pass


# Model used for creating a user, adds a password field
class UserCreate(UserBase):
    password: str


# Model representing the user after creation (response model), includes the user ID
class User(UserBase):
    id: str


# Temporary in-memory list to store users
users: list[User] = []


@app.post("/users", response_model=User)
def create_user(payload: UserCreate):
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


@app.get("/", response_model=list[User])
def get_users():
    return users


@app.get("/users/{id}", response_model=User)
def get_user(id: str):

    for user in users:

        if user["id"] == id:
            return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.put("/users/{id}", response_model=User)
def update_user(id: str, payload: UserUpdate):

    for user in users:

        if user["id"] == id:
            new_name = payload.name
            user["name"] = new_name
            return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str):

    for idx, user in enumerate(users):

        if user["id"] == id:
            users.pop(idx)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
