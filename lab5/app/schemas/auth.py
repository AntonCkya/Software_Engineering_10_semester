from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(...)


class LoginRequest(BaseModel):
    login: str = Field(...)
    password: str = Field(...)


class RegisterRequest(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6, max_length=128)
