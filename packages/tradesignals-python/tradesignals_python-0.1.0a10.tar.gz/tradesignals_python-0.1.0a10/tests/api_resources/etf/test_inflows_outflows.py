# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from tests.utils import assert_matches_type
from tradesignals import Tradesignals, AsyncTradesignals
from tradesignals.types.etf import InflowsOutflowListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInflowsOutflows:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Tradesignals) -> None:
        inflows_outflow = client.etf.inflows_outflows.list(
            "ticker",
        )
        assert_matches_type(Optional[InflowsOutflowListResponse], inflows_outflow, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Tradesignals) -> None:
        inflows_outflow = client.etf.inflows_outflows.list(
            "ticker",
        )
        assert_matches_type(Optional[InflowsOutflowListResponse], inflows_outflow, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Tradesignals) -> None:
        response = client.etf.inflows_outflows.with_raw_response.list(
            "ticker",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inflows_outflow = response.parse()
        assert_matches_type(Optional[InflowsOutflowListResponse], inflows_outflow, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Tradesignals) -> None:
        with client.etf.inflows_outflows.with_streaming_response.list(
            "ticker",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inflows_outflow = response.parse()
            assert_matches_type(Optional[InflowsOutflowListResponse], inflows_outflow, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Tradesignals) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `ticker` but received ''"):
            client.etf.inflows_outflows.with_raw_response.list(
                "",
            )


class TestAsyncInflowsOutflows:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncTradesignals) -> None:
        inflows_outflow = await async_client.etf.inflows_outflows.list(
            "ticker",
        )
        assert_matches_type(Optional[InflowsOutflowListResponse], inflows_outflow, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncTradesignals) -> None:
        inflows_outflow = await async_client.etf.inflows_outflows.list(
            "ticker",
        )
        assert_matches_type(Optional[InflowsOutflowListResponse], inflows_outflow, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncTradesignals) -> None:
        response = await async_client.etf.inflows_outflows.with_raw_response.list(
            "ticker",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inflows_outflow = await response.parse()
        assert_matches_type(Optional[InflowsOutflowListResponse], inflows_outflow, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncTradesignals) -> None:
        async with async_client.etf.inflows_outflows.with_streaming_response.list(
            "ticker",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inflows_outflow = await response.parse()
            assert_matches_type(Optional[InflowsOutflowListResponse], inflows_outflow, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncTradesignals) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `ticker` but received ''"):
            await async_client.etf.inflows_outflows.with_raw_response.list(
                "",
            )
