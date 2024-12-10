# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import datetime
from typing import Union
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["CongressMemberTradeListParams"]


class CongressMemberTradeListParams(TypedDict, total=False):
    date: Annotated[Union[str, datetime.date], PropertyInfo(format="iso8601")]
    """A trading date in the format of YYYY-MM-DD.

    This is optional and by default the last trading date.
    """

    limit: int
    """How many items to return. Default&colon; 100. Max&colon; 200. Min&colon; 1."""
