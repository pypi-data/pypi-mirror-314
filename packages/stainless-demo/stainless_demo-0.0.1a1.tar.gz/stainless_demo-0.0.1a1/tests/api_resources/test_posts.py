# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from stainless_demo import StainlessDemo, AsyncStainlessDemo
from stainless_demo.types import Post, PostListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPosts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: StainlessDemo) -> None:
        post = client.posts.create(
            content="Hello, world! This is my first blog post.",
            title="My First Blog Post",
            user_id="user_123",
        )
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: StainlessDemo) -> None:
        post = client.posts.create(
            content="Hello, world! This is my first blog post.",
            title="My First Blog Post",
            user_id="user_123",
            metadata={
                "tags": "bar",
                "views": "bar",
                "featured": "bar",
            },
        )
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: StainlessDemo) -> None:
        response = client.posts.with_raw_response.create(
            content="Hello, world! This is my first blog post.",
            title="My First Blog Post",
            user_id="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        post = response.parse()
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: StainlessDemo) -> None:
        with client.posts.with_streaming_response.create(
            content="Hello, world! This is my first blog post.",
            title="My First Blog Post",
            user_id="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            post = response.parse()
            assert_matches_type(Post, post, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: StainlessDemo) -> None:
        post = client.posts.retrieve(
            "postId",
        )
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: StainlessDemo) -> None:
        response = client.posts.with_raw_response.retrieve(
            "postId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        post = response.parse()
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: StainlessDemo) -> None:
        with client.posts.with_streaming_response.retrieve(
            "postId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            post = response.parse()
            assert_matches_type(Post, post, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: StainlessDemo) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `post_id` but received ''"):
            client.posts.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: StainlessDemo) -> None:
        post = client.posts.update(
            post_id="postId",
        )
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: StainlessDemo) -> None:
        post = client.posts.update(
            post_id="postId",
            content="content",
            metadata={
                "tags": "bar",
                "views": "bar",
                "featured": "bar",
            },
            title="title",
        )
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: StainlessDemo) -> None:
        response = client.posts.with_raw_response.update(
            post_id="postId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        post = response.parse()
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: StainlessDemo) -> None:
        with client.posts.with_streaming_response.update(
            post_id="postId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            post = response.parse()
            assert_matches_type(Post, post, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: StainlessDemo) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `post_id` but received ''"):
            client.posts.with_raw_response.update(
                post_id="",
            )

    @parametrize
    def test_method_list(self, client: StainlessDemo) -> None:
        post = client.posts.list()
        assert_matches_type(PostListResponse, post, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: StainlessDemo) -> None:
        post = client.posts.list(
            limit=0,
            page=0,
            user_id="userId",
        )
        assert_matches_type(PostListResponse, post, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: StainlessDemo) -> None:
        response = client.posts.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        post = response.parse()
        assert_matches_type(PostListResponse, post, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: StainlessDemo) -> None:
        with client.posts.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            post = response.parse()
            assert_matches_type(PostListResponse, post, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: StainlessDemo) -> None:
        post = client.posts.delete(
            "postId",
        )
        assert post is None

    @parametrize
    def test_raw_response_delete(self, client: StainlessDemo) -> None:
        response = client.posts.with_raw_response.delete(
            "postId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        post = response.parse()
        assert post is None

    @parametrize
    def test_streaming_response_delete(self, client: StainlessDemo) -> None:
        with client.posts.with_streaming_response.delete(
            "postId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            post = response.parse()
            assert post is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: StainlessDemo) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `post_id` but received ''"):
            client.posts.with_raw_response.delete(
                "",
            )


class TestAsyncPosts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncStainlessDemo) -> None:
        post = await async_client.posts.create(
            content="Hello, world! This is my first blog post.",
            title="My First Blog Post",
            user_id="user_123",
        )
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncStainlessDemo) -> None:
        post = await async_client.posts.create(
            content="Hello, world! This is my first blog post.",
            title="My First Blog Post",
            user_id="user_123",
            metadata={
                "tags": "bar",
                "views": "bar",
                "featured": "bar",
            },
        )
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncStainlessDemo) -> None:
        response = await async_client.posts.with_raw_response.create(
            content="Hello, world! This is my first blog post.",
            title="My First Blog Post",
            user_id="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        post = await response.parse()
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncStainlessDemo) -> None:
        async with async_client.posts.with_streaming_response.create(
            content="Hello, world! This is my first blog post.",
            title="My First Blog Post",
            user_id="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            post = await response.parse()
            assert_matches_type(Post, post, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncStainlessDemo) -> None:
        post = await async_client.posts.retrieve(
            "postId",
        )
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncStainlessDemo) -> None:
        response = await async_client.posts.with_raw_response.retrieve(
            "postId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        post = await response.parse()
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncStainlessDemo) -> None:
        async with async_client.posts.with_streaming_response.retrieve(
            "postId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            post = await response.parse()
            assert_matches_type(Post, post, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncStainlessDemo) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `post_id` but received ''"):
            await async_client.posts.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncStainlessDemo) -> None:
        post = await async_client.posts.update(
            post_id="postId",
        )
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncStainlessDemo) -> None:
        post = await async_client.posts.update(
            post_id="postId",
            content="content",
            metadata={
                "tags": "bar",
                "views": "bar",
                "featured": "bar",
            },
            title="title",
        )
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncStainlessDemo) -> None:
        response = await async_client.posts.with_raw_response.update(
            post_id="postId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        post = await response.parse()
        assert_matches_type(Post, post, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncStainlessDemo) -> None:
        async with async_client.posts.with_streaming_response.update(
            post_id="postId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            post = await response.parse()
            assert_matches_type(Post, post, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncStainlessDemo) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `post_id` but received ''"):
            await async_client.posts.with_raw_response.update(
                post_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncStainlessDemo) -> None:
        post = await async_client.posts.list()
        assert_matches_type(PostListResponse, post, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncStainlessDemo) -> None:
        post = await async_client.posts.list(
            limit=0,
            page=0,
            user_id="userId",
        )
        assert_matches_type(PostListResponse, post, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncStainlessDemo) -> None:
        response = await async_client.posts.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        post = await response.parse()
        assert_matches_type(PostListResponse, post, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncStainlessDemo) -> None:
        async with async_client.posts.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            post = await response.parse()
            assert_matches_type(PostListResponse, post, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncStainlessDemo) -> None:
        post = await async_client.posts.delete(
            "postId",
        )
        assert post is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncStainlessDemo) -> None:
        response = await async_client.posts.with_raw_response.delete(
            "postId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        post = await response.parse()
        assert post is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncStainlessDemo) -> None:
        async with async_client.posts.with_streaming_response.delete(
            "postId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            post = await response.parse()
            assert post is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncStainlessDemo) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `post_id` but received ''"):
            await async_client.posts.with_raw_response.delete(
                "",
            )
