# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from haizelabs_api import HaizeLabs, AsyncHaizeLabs
from haizelabs_api.types import JudgeCallResponse
from haizelabs_api._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestJudges:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_call(self, client: HaizeLabs) -> None:
        judge = client.judges.call(
            judge_ids=["string"],
        )
        assert_matches_type(JudgeCallResponse, judge, path=["response"])

    @parametrize
    def test_method_call_with_all_params(self, client: HaizeLabs) -> None:
        judge = client.judges.call(
            judge_ids=["string"],
            id="id",
            behavior="behavior",
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
            content_id="content_id",
            judge_input=True,
            user_id="user_id",
        )
        assert_matches_type(JudgeCallResponse, judge, path=["response"])

    @parametrize
    def test_raw_response_call(self, client: HaizeLabs) -> None:
        response = client.judges.with_raw_response.call(
            judge_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        judge = response.parse()
        assert_matches_type(JudgeCallResponse, judge, path=["response"])

    @parametrize
    def test_streaming_response_call(self, client: HaizeLabs) -> None:
        with client.judges.with_streaming_response.call(
            judge_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            judge = response.parse()
            assert_matches_type(JudgeCallResponse, judge, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncJudges:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_call(self, async_client: AsyncHaizeLabs) -> None:
        judge = await async_client.judges.call(
            judge_ids=["string"],
        )
        assert_matches_type(JudgeCallResponse, judge, path=["response"])

    @parametrize
    async def test_method_call_with_all_params(self, async_client: AsyncHaizeLabs) -> None:
        judge = await async_client.judges.call(
            judge_ids=["string"],
            id="id",
            behavior="behavior",
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
            content_id="content_id",
            judge_input=True,
            user_id="user_id",
        )
        assert_matches_type(JudgeCallResponse, judge, path=["response"])

    @parametrize
    async def test_raw_response_call(self, async_client: AsyncHaizeLabs) -> None:
        response = await async_client.judges.with_raw_response.call(
            judge_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        judge = await response.parse()
        assert_matches_type(JudgeCallResponse, judge, path=["response"])

    @parametrize
    async def test_streaming_response_call(self, async_client: AsyncHaizeLabs) -> None:
        async with async_client.judges.with_streaming_response.call(
            judge_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            judge = await response.parse()
            assert_matches_type(JudgeCallResponse, judge, path=["response"])

        assert cast(Any, response.is_closed) is True
