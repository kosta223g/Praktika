from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role: str = "user"

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone: str
    is_active: bool
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
