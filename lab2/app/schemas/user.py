from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class UserResponse(BaseModel):
    id: str
    login: str
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime


class UserSearchByMaskRequest(BaseModel):
    first_name_mask: Optional[str] = None
    last_name_mask: Optional[str] = None


class UserList(BaseModel):
    users: List[UserResponse]
    total: int
