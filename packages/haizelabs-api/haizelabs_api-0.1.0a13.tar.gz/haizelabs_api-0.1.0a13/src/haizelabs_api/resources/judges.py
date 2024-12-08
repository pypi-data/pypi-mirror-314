# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

import httpx

from ..types import judge_call_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.judge_call_response import JudgeCallResponse

__all__ = ["JudgesResource", "AsyncJudgesResource"]


class JudgesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> JudgesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#accessing-raw-response-data-eg-headers
        """
        return JudgesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> JudgesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#with_streaming_response
        """
        return JudgesResourceWithStreamingResponse(self)

    def call(
        self,
        *,
        judge_ids: List[str],
        id: str | NotGiven = NOT_GIVEN,
        behavior: Optional[str] | NotGiven = NOT_GIVEN,
        content: Optional[judge_call_params.Content] | NotGiven = NOT_GIVEN,
        content_id: Optional[str] | NotGiven = NOT_GIVEN,
        judge_input: bool | NotGiven = NOT_GIVEN,
        user_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JudgeCallResponse:
        """
        Calls a judge.

        Args:
          content: A single piece of content in a test.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/judges/call",
            body=maybe_transform(
                {
                    "judge_ids": judge_ids,
                    "id": id,
                    "behavior": behavior,
                    "content": content,
                    "content_id": content_id,
                    "judge_input": judge_input,
                    "user_id": user_id,
                },
                judge_call_params.JudgeCallParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=JudgeCallResponse,
        )


class AsyncJudgesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncJudgesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#accessing-raw-response-data-eg-headers
        """
        return AsyncJudgesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncJudgesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#with_streaming_response
        """
        return AsyncJudgesResourceWithStreamingResponse(self)

    async def call(
        self,
        *,
        judge_ids: List[str],
        id: str | NotGiven = NOT_GIVEN,
        behavior: Optional[str] | NotGiven = NOT_GIVEN,
        content: Optional[judge_call_params.Content] | NotGiven = NOT_GIVEN,
        content_id: Optional[str] | NotGiven = NOT_GIVEN,
        judge_input: bool | NotGiven = NOT_GIVEN,
        user_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JudgeCallResponse:
        """
        Calls a judge.

        Args:
          content: A single piece of content in a test.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/judges/call",
            body=await async_maybe_transform(
                {
                    "judge_ids": judge_ids,
                    "id": id,
                    "behavior": behavior,
                    "content": content,
                    "content_id": content_id,
                    "judge_input": judge_input,
                    "user_id": user_id,
                },
                judge_call_params.JudgeCallParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=JudgeCallResponse,
        )


class JudgesResourceWithRawResponse:
    def __init__(self, judges: JudgesResource) -> None:
        self._judges = judges

        self.call = to_raw_response_wrapper(
            judges.call,
        )


class AsyncJudgesResourceWithRawResponse:
    def __init__(self, judges: AsyncJudgesResource) -> None:
        self._judges = judges

        self.call = async_to_raw_response_wrapper(
            judges.call,
        )


class JudgesResourceWithStreamingResponse:
    def __init__(self, judges: JudgesResource) -> None:
        self._judges = judges

        self.call = to_streamed_response_wrapper(
            judges.call,
        )


class AsyncJudgesResourceWithStreamingResponse:
    def __init__(self, judges: AsyncJudgesResource) -> None:
        self._judges = judges

        self.call = async_to_streamed_response_wrapper(
            judges.call,
        )
