# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

from .unary_condition_param import UnaryConditionParam

__all__ = ["CompoundConditionInputParam", "Condition"]

Condition: TypeAlias = Union[UnaryConditionParam, "CompoundConditionInputParam"]


class CompoundConditionInputParam(TypedDict, total=False):
    conditions: Optional[Iterable[Condition]]

    input_names: List[str]

    logical_operator: Literal["ALL", "ANY", "NOT"]
