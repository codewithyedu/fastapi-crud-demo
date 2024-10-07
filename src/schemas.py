from pydantic import BaseModel


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
