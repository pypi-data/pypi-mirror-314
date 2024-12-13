# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._compat import PYDANTIC_V2
from .._models import BaseModel
from .unary_condition import UnaryCondition

__all__ = ["CompoundConditionOutput", "Condition"]

Condition: TypeAlias = Union[UnaryCondition, "CompoundConditionOutput"]


class CompoundConditionOutput(BaseModel):
    conditions: Optional[List[Condition]] = None

    input_names: Optional[List[str]] = None

    logical_operator: Optional[Literal["ALL", "ANY", "NOT"]] = None


if PYDANTIC_V2:
    CompoundConditionOutput.model_rebuild()
else:
    CompoundConditionOutput.update_forward_refs()  # type: ignore
