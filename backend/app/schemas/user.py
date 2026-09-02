from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=150)
    designation: Optional[str] = Field(default="Statistical Professional", max_length=150)
    department: Optional[str] = Field(default="MoSPI", max_length=150)
    organization: Optional[str] = Field(default="Government of India", max_length=150)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)  # email
    password: str = Field(..., min_length=1, max_length=128)

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=150)
    designation: Optional[str] = Field(None, max_length=150)
    department: Optional[str] = Field(None, max_length=150)
    organization: Optional[str] = Field(None, max_length=150)

class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class TokenData(BaseModel):
    user_id: Optional[int] = None

