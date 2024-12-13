# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PostListParams"]


class PostListParams(TypedDict, total=False):
    limit: int

    page: int

    user_id: Annotated[str, PropertyInfo(alias="userId")]
