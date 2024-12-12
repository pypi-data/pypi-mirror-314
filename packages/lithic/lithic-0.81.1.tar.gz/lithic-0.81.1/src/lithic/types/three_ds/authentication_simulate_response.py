# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["AuthenticationSimulateResponse"]


class AuthenticationSimulateResponse(BaseModel):
    token: Optional[str] = None
    """
    A unique token to reference this transaction with later calls to void or clear
    the authorization.
    """
