# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from haizelabs_api import HaizeLabs, AsyncHaizeLabs
from haizelabs_api._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMonitoring:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_log_overload_1(self, client: HaizeLabs) -> None:
        monitoring = client.monitoring.log()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_method_log_with_all_params_overload_1(self, client: HaizeLabs) -> None:
        monitoring = client.monitoring.log(
            id="id",
            caller_id="caller_id",
            content={
                "id": "id",
                "content_group_ids": ["string"],
                "content_type": "BASE",
                "end": parse_datetime("2019-12-27T18:11:19.117Z"),
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
                "time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "user_id": "user_id",
            },
            end=parse_datetime("2019-12-27T18:11:19.117Z"),
            metadata={},
            name="name",
            parent_id="parent_id",
            span_type="DETECTOR",
            start=parse_datetime("2019-12-27T18:11:19.117Z"),
            tags={},
            trace_id="trace_id",
            user_id="user_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_raw_response_log_overload_1(self, client: HaizeLabs) -> None:
        response = client.monitoring.with_raw_response.log()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        monitoring = response.parse()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_streaming_response_log_overload_1(self, client: HaizeLabs) -> None:
        with client.monitoring.with_streaming_response.log() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            monitoring = response.parse()
            assert_matches_type(object, monitoring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_log_overload_2(self, client: HaizeLabs) -> None:
        monitoring = client.monitoring.log()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_method_log_with_all_params_overload_2(self, client: HaizeLabs) -> None:
        monitoring = client.monitoring.log(
            id="id",
            end=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            root_content={
                "id": "id",
                "content_group_ids": ["string"],
                "content_type": "BASE",
                "end": parse_datetime("2019-12-27T18:11:19.117Z"),
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
                "time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "user_id": "user_id",
            },
            start=parse_datetime("2019-12-27T18:11:19.117Z"),
            user_id="user_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_raw_response_log_overload_2(self, client: HaizeLabs) -> None:
        response = client.monitoring.with_raw_response.log()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        monitoring = response.parse()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_streaming_response_log_overload_2(self, client: HaizeLabs) -> None:
        with client.monitoring.with_streaming_response.log() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            monitoring = response.parse()
            assert_matches_type(object, monitoring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_log_overload_3(self, client: HaizeLabs) -> None:
        monitoring = client.monitoring.log()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_method_log_with_all_params_overload_3(self, client: HaizeLabs) -> None:
        monitoring = client.monitoring.log(
            id="id",
            content_group_ids=["string"],
            content_type="BASE",
            end=parse_datetime("2019-12-27T18:11:19.117Z"),
            input_detections=[
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
            input_messages=[
                {
                    "content": "string",
                    "role": "system",
                    "name": "name",
                }
            ],
            metadata={},
            output_detections=[
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
            output_messages=[
                {
                    "content": "string",
                    "role": "system",
                    "name": "name",
                }
            ],
            start=parse_datetime("2019-12-27T18:11:19.117Z"),
            time=parse_datetime("2019-12-27T18:11:19.117Z"),
            user_id="user_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_raw_response_log_overload_3(self, client: HaizeLabs) -> None:
        response = client.monitoring.with_raw_response.log()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        monitoring = response.parse()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_streaming_response_log_overload_3(self, client: HaizeLabs) -> None:
        with client.monitoring.with_streaming_response.log() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            monitoring = response.parse()
            assert_matches_type(object, monitoring, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMonitoring:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_log_overload_1(self, async_client: AsyncHaizeLabs) -> None:
        monitoring = await async_client.monitoring.log()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_method_log_with_all_params_overload_1(self, async_client: AsyncHaizeLabs) -> None:
        monitoring = await async_client.monitoring.log(
            id="id",
            caller_id="caller_id",
            content={
                "id": "id",
                "content_group_ids": ["string"],
                "content_type": "BASE",
                "end": parse_datetime("2019-12-27T18:11:19.117Z"),
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
                "time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "user_id": "user_id",
            },
            end=parse_datetime("2019-12-27T18:11:19.117Z"),
            metadata={},
            name="name",
            parent_id="parent_id",
            span_type="DETECTOR",
            start=parse_datetime("2019-12-27T18:11:19.117Z"),
            tags={},
            trace_id="trace_id",
            user_id="user_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_raw_response_log_overload_1(self, async_client: AsyncHaizeLabs) -> None:
        response = await async_client.monitoring.with_raw_response.log()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        monitoring = await response.parse()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_streaming_response_log_overload_1(self, async_client: AsyncHaizeLabs) -> None:
        async with async_client.monitoring.with_streaming_response.log() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            monitoring = await response.parse()
            assert_matches_type(object, monitoring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_log_overload_2(self, async_client: AsyncHaizeLabs) -> None:
        monitoring = await async_client.monitoring.log()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_method_log_with_all_params_overload_2(self, async_client: AsyncHaizeLabs) -> None:
        monitoring = await async_client.monitoring.log(
            id="id",
            end=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            root_content={
                "id": "id",
                "content_group_ids": ["string"],
                "content_type": "BASE",
                "end": parse_datetime("2019-12-27T18:11:19.117Z"),
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
                "time": parse_datetime("2019-12-27T18:11:19.117Z"),
                "user_id": "user_id",
            },
            start=parse_datetime("2019-12-27T18:11:19.117Z"),
            user_id="user_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_raw_response_log_overload_2(self, async_client: AsyncHaizeLabs) -> None:
        response = await async_client.monitoring.with_raw_response.log()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        monitoring = await response.parse()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_streaming_response_log_overload_2(self, async_client: AsyncHaizeLabs) -> None:
        async with async_client.monitoring.with_streaming_response.log() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            monitoring = await response.parse()
            assert_matches_type(object, monitoring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_log_overload_3(self, async_client: AsyncHaizeLabs) -> None:
        monitoring = await async_client.monitoring.log()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_method_log_with_all_params_overload_3(self, async_client: AsyncHaizeLabs) -> None:
        monitoring = await async_client.monitoring.log(
            id="id",
            content_group_ids=["string"],
            content_type="BASE",
            end=parse_datetime("2019-12-27T18:11:19.117Z"),
            input_detections=[
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
            input_messages=[
                {
                    "content": "string",
                    "role": "system",
                    "name": "name",
                }
            ],
            metadata={},
            output_detections=[
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
            output_messages=[
                {
                    "content": "string",
                    "role": "system",
                    "name": "name",
                }
            ],
            start=parse_datetime("2019-12-27T18:11:19.117Z"),
            time=parse_datetime("2019-12-27T18:11:19.117Z"),
            user_id="user_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_raw_response_log_overload_3(self, async_client: AsyncHaizeLabs) -> None:
        response = await async_client.monitoring.with_raw_response.log()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        monitoring = await response.parse()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_streaming_response_log_overload_3(self, async_client: AsyncHaizeLabs) -> None:
        async with async_client.monitoring.with_streaming_response.log() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            monitoring = await response.parse()
            assert_matches_type(object, monitoring, path=["response"])

        assert cast(Any, response.is_closed) is True
