# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from haizelabs_api import HaizeLabs, AsyncHaizeLabs
from haizelabs_api.types import TestingStartResponse, TestingUpdateResponse
from haizelabs_api._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTesting:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: HaizeLabs) -> None:
        testing = client.testing.update()
        assert_matches_type(TestingUpdateResponse, testing, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: HaizeLabs) -> None:
        testing = client.testing.update(
            id="id",
            contents=[
                {
                    "id": "id",
                    "algorithm": "algorithm",
                    "behavior": {"description": "description"},
                    "content_group_ids": ["string"],
                    "content_type": "BASE",
                    "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "generate_end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "generate_start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "input_detections": [
                        {
                            "content_id": "content_id",
                            "detected": True,
                            "detector_id": "detector_id",
                            "end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                            "score": 0,
                            "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                            "detector_data": {
                                "name": "name",
                                "regex": "regex",
                                "user_id": "user_id",
                                "id": "id",
                                "created": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "detector_type": "TEXT_MATCHING",
                                "last_updated": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "input_messages": [
                        {
                            "content": "string",
                            "role": "system",
                            "name": "name",
                        }
                    ],
                    "metadata": {},
                    "output_detections": [
                        {
                            "content_id": "content_id",
                            "detected": True,
                            "detector_id": "detector_id",
                            "end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                            "score": 0,
                            "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                            "detector_data": {
                                "name": "name",
                                "regex": "regex",
                                "user_id": "user_id",
                                "id": "id",
                                "created": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "detector_type": "TEXT_MATCHING",
                                "last_updated": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "output_messages": [
                        {
                            "content": "string",
                            "role": "system",
                            "name": "name",
                        }
                    ],
                    "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "status": "GENERATING_CONTENT",
                    "test_id": "test_id",
                    "time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "user_id": "user_id",
                }
            ],
            test_id="test_id",
            time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(TestingUpdateResponse, testing, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: HaizeLabs) -> None:
        response = client.testing.with_raw_response.update()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        testing = response.parse()
        assert_matches_type(TestingUpdateResponse, testing, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: HaizeLabs) -> None:
        with client.testing.with_streaming_response.update() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            testing = response.parse()
            assert_matches_type(TestingUpdateResponse, testing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_start(self, client: HaizeLabs) -> None:
        testing = client.testing.start(
            test_data={
                "name": "name",
                "user_id": "user_id",
            },
        )
        assert_matches_type(TestingStartResponse, testing, path=["response"])

    @parametrize
    def test_method_start_with_all_params(self, client: HaizeLabs) -> None:
        testing = client.testing.start(
            test_data={
                "name": "name",
                "user_id": "user_id",
                "id": "id",
                "algorithm_status": [
                    {
                        "name": "name",
                        "status": "COMPLETE",
                    }
                ],
                "behaviors": [{"description": "description"}],
                "content": [
                    {
                        "id": "id",
                        "algorithm": "algorithm",
                        "behavior": {"description": "description"},
                        "content_group_ids": ["string"],
                        "content_type": "BASE",
                        "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "generate_end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "generate_start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "input_detections": [
                            {
                                "content_id": "content_id",
                                "detected": True,
                                "detector_id": "detector_id",
                                "end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "score": 0,
                                "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "detector_data": {
                                    "name": "name",
                                    "regex": "regex",
                                    "user_id": "user_id",
                                    "id": "id",
                                    "created": parse_datetime("2019-12-27T18:11:19.117Z"),
                                    "detector_type": "TEXT_MATCHING",
                                    "last_updated": parse_datetime("2019-12-27T18:11:19.117Z"),
                                },
                            }
                        ],
                        "input_messages": [
                            {
                                "content": "string",
                                "role": "system",
                                "name": "name",
                            }
                        ],
                        "metadata": {},
                        "output_detections": [
                            {
                                "content_id": "content_id",
                                "detected": True,
                                "detector_id": "detector_id",
                                "end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "score": 0,
                                "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "detector_data": {
                                    "name": "name",
                                    "regex": "regex",
                                    "user_id": "user_id",
                                    "id": "id",
                                    "created": parse_datetime("2019-12-27T18:11:19.117Z"),
                                    "detector_type": "TEXT_MATCHING",
                                    "last_updated": parse_datetime("2019-12-27T18:11:19.117Z"),
                                },
                            }
                        ],
                        "output_messages": [
                            {
                                "content": "string",
                                "role": "system",
                                "name": "name",
                            }
                        ],
                        "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "status": "GENERATING_CONTENT",
                        "test_id": "test_id",
                        "time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "user_id": "user_id",
                    }
                ],
                "content_group_ids": ["string"],
                "detector_ids": ["string"],
                "end_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                "start_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                "status": "COMPLETE",
                "target_model": {
                    "model_id": "model_id",
                    "id": "id",
                    "api_key": "api_key",
                    "base_url": "base_url",
                    "generation_params": {
                        "id": "id",
                        "max_tokens": 1,
                        "system_message": "system_message",
                        "temperature": 0,
                        "user_id": "user_id",
                    },
                    "model_provider": "model_provider",
                    "model_type": "STANDARD",
                    "name": "name",
                    "time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "user_id": "user_id",
                },
                "test_type": "RED_TEAMING",
            },
            id="id",
            user_id="user_id",
        )
        assert_matches_type(TestingStartResponse, testing, path=["response"])

    @parametrize
    def test_raw_response_start(self, client: HaizeLabs) -> None:
        response = client.testing.with_raw_response.start(
            test_data={
                "name": "name",
                "user_id": "user_id",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        testing = response.parse()
        assert_matches_type(TestingStartResponse, testing, path=["response"])

    @parametrize
    def test_streaming_response_start(self, client: HaizeLabs) -> None:
        with client.testing.with_streaming_response.start(
            test_data={
                "name": "name",
                "user_id": "user_id",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            testing = response.parse()
            assert_matches_type(TestingStartResponse, testing, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTesting:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_update(self, async_client: AsyncHaizeLabs) -> None:
        testing = await async_client.testing.update()
        assert_matches_type(TestingUpdateResponse, testing, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncHaizeLabs) -> None:
        testing = await async_client.testing.update(
            id="id",
            contents=[
                {
                    "id": "id",
                    "algorithm": "algorithm",
                    "behavior": {"description": "description"},
                    "content_group_ids": ["string"],
                    "content_type": "BASE",
                    "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "generate_end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "generate_start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "input_detections": [
                        {
                            "content_id": "content_id",
                            "detected": True,
                            "detector_id": "detector_id",
                            "end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                            "score": 0,
                            "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                            "detector_data": {
                                "name": "name",
                                "regex": "regex",
                                "user_id": "user_id",
                                "id": "id",
                                "created": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "detector_type": "TEXT_MATCHING",
                                "last_updated": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "input_messages": [
                        {
                            "content": "string",
                            "role": "system",
                            "name": "name",
                        }
                    ],
                    "metadata": {},
                    "output_detections": [
                        {
                            "content_id": "content_id",
                            "detected": True,
                            "detector_id": "detector_id",
                            "end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                            "score": 0,
                            "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                            "detector_data": {
                                "name": "name",
                                "regex": "regex",
                                "user_id": "user_id",
                                "id": "id",
                                "created": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "detector_type": "TEXT_MATCHING",
                                "last_updated": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "output_messages": [
                        {
                            "content": "string",
                            "role": "system",
                            "name": "name",
                        }
                    ],
                    "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "status": "GENERATING_CONTENT",
                    "test_id": "test_id",
                    "time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "user_id": "user_id",
                }
            ],
            test_id="test_id",
            time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(TestingUpdateResponse, testing, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncHaizeLabs) -> None:
        response = await async_client.testing.with_raw_response.update()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        testing = await response.parse()
        assert_matches_type(TestingUpdateResponse, testing, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncHaizeLabs) -> None:
        async with async_client.testing.with_streaming_response.update() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            testing = await response.parse()
            assert_matches_type(TestingUpdateResponse, testing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_start(self, async_client: AsyncHaizeLabs) -> None:
        testing = await async_client.testing.start(
            test_data={
                "name": "name",
                "user_id": "user_id",
            },
        )
        assert_matches_type(TestingStartResponse, testing, path=["response"])

    @parametrize
    async def test_method_start_with_all_params(self, async_client: AsyncHaizeLabs) -> None:
        testing = await async_client.testing.start(
            test_data={
                "name": "name",
                "user_id": "user_id",
                "id": "id",
                "algorithm_status": [
                    {
                        "name": "name",
                        "status": "COMPLETE",
                    }
                ],
                "behaviors": [{"description": "description"}],
                "content": [
                    {
                        "id": "id",
                        "algorithm": "algorithm",
                        "behavior": {"description": "description"},
                        "content_group_ids": ["string"],
                        "content_type": "BASE",
                        "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "generate_end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "generate_start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "input_detections": [
                            {
                                "content_id": "content_id",
                                "detected": True,
                                "detector_id": "detector_id",
                                "end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "score": 0,
                                "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "detector_data": {
                                    "name": "name",
                                    "regex": "regex",
                                    "user_id": "user_id",
                                    "id": "id",
                                    "created": parse_datetime("2019-12-27T18:11:19.117Z"),
                                    "detector_type": "TEXT_MATCHING",
                                    "last_updated": parse_datetime("2019-12-27T18:11:19.117Z"),
                                },
                            }
                        ],
                        "input_messages": [
                            {
                                "content": "string",
                                "role": "system",
                                "name": "name",
                            }
                        ],
                        "metadata": {},
                        "output_detections": [
                            {
                                "content_id": "content_id",
                                "detected": True,
                                "detector_id": "detector_id",
                                "end_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "score": 0,
                                "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "detector_data": {
                                    "name": "name",
                                    "regex": "regex",
                                    "user_id": "user_id",
                                    "id": "id",
                                    "created": parse_datetime("2019-12-27T18:11:19.117Z"),
                                    "detector_type": "TEXT_MATCHING",
                                    "last_updated": parse_datetime("2019-12-27T18:11:19.117Z"),
                                },
                            }
                        ],
                        "output_messages": [
                            {
                                "content": "string",
                                "role": "system",
                                "name": "name",
                            }
                        ],
                        "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "status": "GENERATING_CONTENT",
                        "test_id": "test_id",
                        "time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "user_id": "user_id",
                    }
                ],
                "content_group_ids": ["string"],
                "detector_ids": ["string"],
                "end_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                "start_date": parse_datetime("2019-12-27T18:11:19.117Z"),
                "status": "COMPLETE",
                "target_model": {
                    "model_id": "model_id",
                    "id": "id",
                    "api_key": "api_key",
                    "base_url": "base_url",
                    "generation_params": {
                        "id": "id",
                        "max_tokens": 1,
                        "system_message": "system_message",
                        "temperature": 0,
                        "user_id": "user_id",
                    },
                    "model_provider": "model_provider",
                    "model_type": "STANDARD",
                    "name": "name",
                    "time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "user_id": "user_id",
                },
                "test_type": "RED_TEAMING",
            },
            id="id",
            user_id="user_id",
        )
        assert_matches_type(TestingStartResponse, testing, path=["response"])

    @parametrize
    async def test_raw_response_start(self, async_client: AsyncHaizeLabs) -> None:
        response = await async_client.testing.with_raw_response.start(
            test_data={
                "name": "name",
                "user_id": "user_id",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        testing = await response.parse()
        assert_matches_type(TestingStartResponse, testing, path=["response"])

    @parametrize
    async def test_streaming_response_start(self, async_client: AsyncHaizeLabs) -> None:
        async with async_client.testing.with_streaming_response.start(
            test_data={
                "name": "name",
                "user_id": "user_id",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            testing = await response.parse()
            assert_matches_type(TestingStartResponse, testing, path=["response"])

        assert cast(Any, response.is_closed) is True
