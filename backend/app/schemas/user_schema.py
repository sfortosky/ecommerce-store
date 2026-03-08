from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

# Local user signup
class UserCreate(UserBase):
    password: str

# OAuth user signup
class UserOAuthCreate(UserBase):
    oauth_provider: str
    oauth_id: str
    is_oauth_user: bool = True

# User return model
class UserOut(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data model
class TokenData(BaseModel):
    email: Optional[str] = None