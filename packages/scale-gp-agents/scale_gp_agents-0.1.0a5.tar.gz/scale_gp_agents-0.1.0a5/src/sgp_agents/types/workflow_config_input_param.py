# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["WorkflowConfigInputParam"]


class WorkflowConfigInputParam(TypedDict, total=False):
    workflow: Required[Union[Iterable["NodeItemInputParam"], str]]

    id: Optional[str]

    account_id: Optional[str]

    application_variant_id: Optional[str]

    base_url: Optional[str]

    concurrency_default: bool

    datasets: Optional[Iterable[object]]

    egp_api_key_override: Optional[str]

    egp_ui_evaluation: Optional[object]

    evaluations: Optional[Iterable["NodeItemInputParam"]]

    final_output_nodes: Optional[List[str]]

    nodes_to_log: Union[str, List[str], None]

    num_workers: Optional[int]

    streaming_nodes: Optional[List[str]]

    subtype: Optional[Literal["chat", "report"]]

    type: Optional[Literal["workflow", "plan", "state_machine"]]

    user_input: object


from .node_item_input_param import NodeItemInputParam
