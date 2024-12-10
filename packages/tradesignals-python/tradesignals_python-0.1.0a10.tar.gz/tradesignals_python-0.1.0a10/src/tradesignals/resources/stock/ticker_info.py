# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.stock.ticker_info_response import TickerInfoResponse

__all__ = ["TickerInfoResource", "AsyncTickerInfoResource"]


class TickerInfoResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TickerInfoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/macanderson/tradesignals-python#accessing-raw-response-data-eg-headers
        """
        return TickerInfoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TickerInfoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/macanderson/tradesignals-python#with_streaming_response
        """
        return TickerInfoResourceWithStreamingResponse(self)

    def list(
        self,
        ticker: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TickerInfoResponse:
        """
        Returns general information about the given ticker.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not ticker:
            raise ValueError(f"Expected a non-empty value for `ticker` but received {ticker!r}")
        return self._get(
            f"/api/stock/{ticker}/info",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TickerInfoResponse,
        )


class AsyncTickerInfoResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTickerInfoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/macanderson/tradesignals-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTickerInfoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTickerInfoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/macanderson/tradesignals-python#with_streaming_response
        """
        return AsyncTickerInfoResourceWithStreamingResponse(self)

    async def list(
        self,
        ticker: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TickerInfoResponse:
        """
        Returns general information about the given ticker.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not ticker:
            raise ValueError(f"Expected a non-empty value for `ticker` but received {ticker!r}")
        return await self._get(
            f"/api/stock/{ticker}/info",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TickerInfoResponse,
        )


class TickerInfoResourceWithRawResponse:
    def __init__(self, ticker_info: TickerInfoResource) -> None:
        self._ticker_info = ticker_info

        self.list = to_raw_response_wrapper(
            ticker_info.list,
        )


class AsyncTickerInfoResourceWithRawResponse:
    def __init__(self, ticker_info: AsyncTickerInfoResource) -> None:
        self._ticker_info = ticker_info

        self.list = async_to_raw_response_wrapper(
            ticker_info.list,
        )


class TickerInfoResourceWithStreamingResponse:
    def __init__(self, ticker_info: TickerInfoResource) -> None:
        self._ticker_info = ticker_info

        self.list = to_streamed_response_wrapper(
            ticker_info.list,
        )


class AsyncTickerInfoResourceWithStreamingResponse:
    def __init__(self, ticker_info: AsyncTickerInfoResource) -> None:
        self._ticker_info = ticker_info

        self.list = async_to_streamed_response_wrapper(
            ticker_info.list,
        )
