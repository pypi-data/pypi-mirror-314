# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from stainless_demo import StainlessDemo, AsyncStainlessDemo
from stainless_demo.types import User, UserListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: StainlessDemo) -> None:
        user = client.users.create(
            email="john.doe@example.com",
            username="johndoe",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: StainlessDemo) -> None:
        user = client.users.create(
            email="john.doe@example.com",
            username="johndoe",
            password="password",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: StainlessDemo) -> None:
        response = client.users.with_raw_response.create(
            email="john.doe@example.com",
            username="johndoe",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: StainlessDemo) -> None:
        with client.users.with_streaming_response.create(
            email="john.doe@example.com",
            username="johndoe",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: StainlessDemo) -> None:
        user = client.users.retrieve(
            "userId",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: StainlessDemo) -> None:
        response = client.users.with_raw_response.retrieve(
            "userId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: StainlessDemo) -> None:
        with client.users.with_streaming_response.retrieve(
            "userId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: StainlessDemo) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: StainlessDemo) -> None:
        user = client.users.update(
            user_id="userId",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: StainlessDemo) -> None:
        user = client.users.update(
            user_id="userId",
            email="dev@stainlessapi.com",
            password="password",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: StainlessDemo) -> None:
        response = client.users.with_raw_response.update(
            user_id="userId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: StainlessDemo) -> None:
        with client.users.with_streaming_response.update(
            user_id="userId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: StainlessDemo) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.with_raw_response.update(
                user_id="",
            )

    @parametrize
    def test_method_list(self, client: StainlessDemo) -> None:
        user = client.users.list()
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: StainlessDemo) -> None:
        user = client.users.list(
            limit=0,
            page=0,
        )
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: StainlessDemo) -> None:
        response = client.users.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: StainlessDemo) -> None:
        with client.users.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserListResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUsers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncStainlessDemo) -> None:
        user = await async_client.users.create(
            email="john.doe@example.com",
            username="johndoe",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncStainlessDemo) -> None:
        user = await async_client.users.create(
            email="john.doe@example.com",
            username="johndoe",
            password="password",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncStainlessDemo) -> None:
        response = await async_client.users.with_raw_response.create(
            email="john.doe@example.com",
            username="johndoe",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncStainlessDemo) -> None:
        async with async_client.users.with_streaming_response.create(
            email="john.doe@example.com",
            username="johndoe",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncStainlessDemo) -> None:
        user = await async_client.users.retrieve(
            "userId",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncStainlessDemo) -> None:
        response = await async_client.users.with_raw_response.retrieve(
            "userId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncStainlessDemo) -> None:
        async with async_client.users.with_streaming_response.retrieve(
            "userId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncStainlessDemo) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncStainlessDemo) -> None:
        user = await async_client.users.update(
            user_id="userId",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncStainlessDemo) -> None:
        user = await async_client.users.update(
            user_id="userId",
            email="dev@stainlessapi.com",
            password="password",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncStainlessDemo) -> None:
        response = await async_client.users.with_raw_response.update(
            user_id="userId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncStainlessDemo) -> None:
        async with async_client.users.with_streaming_response.update(
            user_id="userId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncStainlessDemo) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.with_raw_response.update(
                user_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncStainlessDemo) -> None:
        user = await async_client.users.list()
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncStainlessDemo) -> None:
        user = await async_client.users.list(
            limit=0,
            page=0,
        )
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncStainlessDemo) -> None:
        response = await async_client.users.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncStainlessDemo) -> None:
        async with async_client.users.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserListResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True
