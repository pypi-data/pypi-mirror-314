# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional

from .._models import BaseModel

__all__ = ["WorkflowItem"]


class WorkflowItem(BaseModel):
    workflow_name: str

    workflow_alias: Optional[str] = None

    workflow_inputs: Optional[Dict[str, Union[str, Dict[str, Union[str, object]]]]] = None
