# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import datetime

import httpx

from ..types import testing_start_params, testing_update_params
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
from ..types.testing_start_response import TestingStartResponse
from ..types.testing_update_response import TestingUpdateResponse

__all__ = ["TestingResource", "AsyncTestingResource"]


class TestingResource(SyncAPIResource):
    __test__ = False

    @cached_property
    def with_raw_response(self) -> TestingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#accessing-raw-response-data-eg-headers
        """
        return TestingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TestingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#with_streaming_response
        """
        return TestingResourceWithStreamingResponse(self)

    def update(
        self,
        *,
        id: str | NotGiven = NOT_GIVEN,
        contents: Iterable[testing_update_params.Content] | NotGiven = NOT_GIVEN,
        test_id: str | NotGiven = NOT_GIVEN,
        time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestingUpdateResponse:
        """
        Updates an existing test with responses.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/testing/update",
            body=maybe_transform(
                {
                    "id": id,
                    "contents": contents,
                    "test_id": test_id,
                    "time": time,
                },
                testing_update_params.TestingUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestingUpdateResponse,
        )

    def start(
        self,
        *,
        test_data: testing_start_params.TestData,
        id: str | NotGiven = NOT_GIVEN,
        user_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestingStartResponse:
        """
        Starts a new test.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/testing/start",
            body=maybe_transform(
                {
                    "test_data": test_data,
                    "id": id,
                    "user_id": user_id,
                },
                testing_start_params.TestingStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestingStartResponse,
        )


class AsyncTestingResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTestingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTestingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTestingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#with_streaming_response
        """
        return AsyncTestingResourceWithStreamingResponse(self)

    async def update(
        self,
        *,
        id: str | NotGiven = NOT_GIVEN,
        contents: Iterable[testing_update_params.Content] | NotGiven = NOT_GIVEN,
        test_id: str | NotGiven = NOT_GIVEN,
        time: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestingUpdateResponse:
        """
        Updates an existing test with responses.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/testing/update",
            body=await async_maybe_transform(
                {
                    "id": id,
                    "contents": contents,
                    "test_id": test_id,
                    "time": time,
                },
                testing_update_params.TestingUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestingUpdateResponse,
        )

    async def start(
        self,
        *,
        test_data: testing_start_params.TestData,
        id: str | NotGiven = NOT_GIVEN,
        user_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TestingStartResponse:
        """
        Starts a new test.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/testing/start",
            body=await async_maybe_transform(
                {
                    "test_data": test_data,
                    "id": id,
                    "user_id": user_id,
                },
                testing_start_params.TestingStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestingStartResponse,
        )


class TestingResourceWithRawResponse:
    __test__ = False

    def __init__(self, testing: TestingResource) -> None:
        self._testing = testing

        self.update = to_raw_response_wrapper(
            testing.update,
        )
        self.start = to_raw_response_wrapper(
            testing.start,
        )


class AsyncTestingResourceWithRawResponse:
    def __init__(self, testing: AsyncTestingResource) -> None:
        self._testing = testing

        self.update = async_to_raw_response_wrapper(
            testing.update,
        )
        self.start = async_to_raw_response_wrapper(
            testing.start,
        )


class TestingResourceWithStreamingResponse:
    __test__ = False

    def __init__(self, testing: TestingResource) -> None:
        self._testing = testing

        self.update = to_streamed_response_wrapper(
            testing.update,
        )
        self.start = to_streamed_response_wrapper(
            testing.start,
        )


class AsyncTestingResourceWithStreamingResponse:
    def __init__(self, testing: AsyncTestingResource) -> None:
        self._testing = testing

        self.update = async_to_streamed_response_wrapper(
            testing.update,
        )
        self.start = async_to_streamed_response_wrapper(
            testing.start,
        )
