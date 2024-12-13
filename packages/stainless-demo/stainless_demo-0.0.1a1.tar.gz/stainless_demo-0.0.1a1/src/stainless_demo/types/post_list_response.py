# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .post import Post
from .._models import BaseModel

__all__ = ["PostListResponse"]


class PostListResponse(BaseModel):
    posts: Optional[List[Post]] = None

    total: Optional[int] = None
