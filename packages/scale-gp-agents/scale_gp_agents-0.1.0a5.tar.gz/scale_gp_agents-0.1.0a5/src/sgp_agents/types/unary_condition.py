# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["UnaryCondition"]


class UnaryCondition(BaseModel):
    condition_input_var: str

    operator: str

    reference_var: Optional[object] = None
