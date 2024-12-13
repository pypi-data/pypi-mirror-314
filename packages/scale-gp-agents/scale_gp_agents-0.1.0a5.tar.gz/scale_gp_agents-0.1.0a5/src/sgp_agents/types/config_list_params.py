# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ConfigListParams"]


class ConfigListParams(TypedDict, total=False):
    config_type: Required[Literal["workflow", "plan", "state_machine"]]

    account_id: Optional[str]
