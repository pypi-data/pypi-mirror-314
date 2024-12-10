# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from .congress_member_trade import CongressMemberTrade

__all__ = ["CongressMemberTradeResponse"]


class CongressMemberTradeResponse(BaseModel):
    data: Optional[List[CongressMemberTrade]] = None
