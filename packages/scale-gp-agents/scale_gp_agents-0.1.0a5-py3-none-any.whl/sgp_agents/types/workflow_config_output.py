# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal

from .._compat import PYDANTIC_V2
from .._models import BaseModel

__all__ = ["WorkflowConfigOutput"]


class WorkflowConfigOutput(BaseModel):
    workflow: Union[List["NodeItemOutput"], str]

    id: Optional[str] = None

    account_id: Optional[str] = None

    application_variant_id: Optional[str] = None

    base_url: Optional[str] = None

    concurrency_default: Optional[bool] = None

    datasets: Optional[List[object]] = None

    egp_api_key_override: Optional[str] = None

    egp_ui_evaluation: Optional[object] = None

    evaluations: Optional[List["NodeItemOutput"]] = None

    final_output_nodes: Optional[List[str]] = None

    nodes_to_log: Union[str, List[str], None] = None

    num_workers: Optional[int] = None

    streaming_nodes: Optional[List[str]] = None

    subtype: Optional[Literal["chat", "report"]] = None

    type: Optional[Literal["workflow", "plan", "state_machine"]] = None

    user_input: Optional[object] = None


from .node_item_output import NodeItemOutput

if PYDANTIC_V2:
    WorkflowConfigOutput.model_rebuild()
else:
    WorkflowConfigOutput.update_forward_refs()  # type: ignore
