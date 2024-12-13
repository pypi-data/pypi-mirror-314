# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .workflow_item_param import WorkflowItemParam
from .compound_condition_input_param import CompoundConditionInputParam

__all__ = [
    "PlanConfigInputParam",
    "Plan",
    "PlanBranchConfigInput",
    "PlanBranchConfigInputConditionalWorkflow",
    "PlanLoopConfigInput",
    "PlanLoopConfigInputLoopInputs",
    "PlanLoopConfigInputLoopInputsSelfEdge",
    "Workflows",
    "WorkflowsWorkflowInput",
]


class PlanBranchConfigInputConditionalWorkflow(TypedDict, total=False):
    condition: Required[Literal["if", "elif", "else"]]

    workflow_name: Required[str]

    condition_input_var: Optional[str]

    condition_tree: Optional[CompoundConditionInputParam]
    """Representation of a compound boolean statement, i.e.

    a negation, conjunction, or disjunction of UnaryConditions
    """

    operator: Optional[str]

    reference_var: Optional[str]

    workflow_alias: Optional[str]

    workflow_inputs: Optional[Dict[str, Union[str, Dict[str, Union[str, object]]]]]

    workflow_nodes: List[str]


class PlanBranchConfigInput(TypedDict, total=False):
    branch: Required[str]

    conditional_workflows: Required[Iterable[PlanBranchConfigInputConditionalWorkflow]]

    merge_outputs: Dict[str, List[str]]

    save_merge_to_memory: Dict[str, str]


class PlanLoopConfigInputLoopInputsSelfEdge(TypedDict, total=False):
    node_name: Required[str]

    default_source: Optional[str]

    default_value: Optional[object]


PlanLoopConfigInputLoopInputs: TypeAlias = Union[str, PlanLoopConfigInputLoopInputsSelfEdge]


class PlanLoopConfigInput(TypedDict, total=False):
    condition: Required[CompoundConditionInputParam]
    """Representation of a compound boolean statement, i.e.

    a negation, conjunction, or disjunction of UnaryConditions
    """

    max_iter: Required[int]

    name: Required[str]

    workflow: Required[WorkflowItemParam]
    """
    Representation of an instance of an abstract Workflow Attributes: workflow_name:
    Key in the map of workflows defined at the top of a plan config workflow_alias:
    Alias of the abstract workflow in the graph. If None, defaults to workflow_name.
    Use in order to re-use the same abstract workflow in multiple portions of the
    graph. workflow_inputs: Inputs to the workflow can be: 1) empty if this workflow
    does not receive input from another workflow, 2) a dictionary mapping another
    workflow's outputs or a branch's merged outputs to this workflows input keys For
    case 2, inputs can be a mapping from: a) str to str b) str to dict(str, str) c)
    str to dict(str, dict(str, str))
    """

    loop_inputs: Dict[str, PlanLoopConfigInputLoopInputs]

    merge_outputs: Dict[str, str]


Plan: TypeAlias = Union[WorkflowItemParam, PlanBranchConfigInput, PlanLoopConfigInput]


class WorkflowsWorkflowInput(TypedDict, total=False):
    name: Required[str]

    nodes: Required[Iterable["NodeItemInputParam"]]


Workflows: TypeAlias = Union[WorkflowsWorkflowInput, str, Iterable["NodeItemInputParam"]]


class PlanConfigInputParam(TypedDict, total=False):
    plan: Required[Iterable[Plan]]

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

    workflows: Dict[str, Workflows]


from .node_item_input_param import NodeItemInputParam
