from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

class UserSignupModel(BaseModel):
    username: str = Field(min_length=3, max_length=10)
    email: str = Field(min_length=5, max_length=50)
    first_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=8)

class UserLoginModel(BaseModel):
    email: str
    password: str