# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Post"]


class Post(BaseModel):
    id: str

    content: str

    title: str

    user_id: str = FieldInfo(alias="userId")

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[datetime] = FieldInfo(alias="updatedAt", default=None)
