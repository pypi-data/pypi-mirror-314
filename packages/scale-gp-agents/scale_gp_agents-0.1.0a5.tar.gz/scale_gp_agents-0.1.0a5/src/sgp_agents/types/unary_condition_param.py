# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["UnaryConditionParam"]


class UnaryConditionParam(TypedDict, total=False):
    condition_input_var: Required[str]

    operator: Required[str]

    reference_var: object
