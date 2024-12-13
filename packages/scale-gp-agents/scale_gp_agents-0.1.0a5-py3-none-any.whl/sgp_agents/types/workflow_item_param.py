# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Required, TypedDict

__all__ = ["WorkflowItemParam"]


class WorkflowItemParam(TypedDict, total=False):
    workflow_name: Required[str]

    workflow_alias: Optional[str]

    workflow_inputs: Optional[Dict[str, Union[str, Dict[str, Union[str, object]]]]]
