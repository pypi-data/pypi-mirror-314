# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PostCreateParams"]


class PostCreateParams(TypedDict, total=False):
    content: Required[str]

    title: Required[str]

    user_id: Required[Annotated[str, PropertyInfo(alias="userId")]]

    metadata: Dict[str, object]
