# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["User"]


class User(BaseModel):
    id: str

    email: str

    username: str

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
