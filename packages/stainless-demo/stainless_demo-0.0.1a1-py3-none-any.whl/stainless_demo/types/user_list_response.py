# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .user import User
from .._models import BaseModel

__all__ = ["UserListResponse"]


class UserListResponse(BaseModel):
    total: Optional[int] = None

    users: Optional[List[User]] = None
