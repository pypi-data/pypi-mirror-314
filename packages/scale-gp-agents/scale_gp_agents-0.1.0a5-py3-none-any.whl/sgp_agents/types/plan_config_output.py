# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._compat import PYDANTIC_V2
from .._models import BaseModel
from .workflow_item import WorkflowItem
from .compound_condition_output import CompoundConditionOutput

__all__ = [
    "PlanConfigOutput",
    "Plan",
    "PlanBranchConfigOutput",
    "PlanBranchConfigOutputConditionalWorkflow",
    "PlanLoopConfigOutput",
    "PlanLoopConfigOutputLoopInputs",
    "PlanLoopConfigOutputLoopInputsSelfEdge",
    "Workflows",
    "WorkflowsWorkflowOutput",
]


class PlanBranchConfigOutputConditionalWorkflow(BaseModel):
    condition: Literal["if", "elif", "else"]

    workflow_name: str

    condition_input_var: Optional[str] = None

    condition_tree: Optional[CompoundConditionOutput] = None
    """Representation of a compound boolean statement, i.e.

    a negation, conjunction, or disjunction of UnaryConditions
    """

    operator: Optional[str] = None

    reference_var: Optional[str] = None

    workflow_alias: Optional[str] = None

    workflow_inputs: Optional[Dict[str, Union[str, Dict[str, Union[str, object]]]]] = None

    workflow_nodes: Optional[List[str]] = None


class PlanBranchConfigOutput(BaseModel):
    branch: str

    conditional_workflows: List[PlanBranchConfigOutputConditionalWorkflow]

    merge_outputs: Optional[Dict[str, List[str]]] = None

    save_merge_to_memory: Optional[Dict[str, str]] = None


class PlanLoopConfigOutputLoopInputsSelfEdge(BaseModel):
    node_name: str

    default_source: Optional[str] = None

    default_value: Optional[object] = None


PlanLoopConfigOutputLoopInputs: TypeAlias = Union[str, PlanLoopConfigOutputLoopInputsSelfEdge]


class PlanLoopConfigOutput(BaseModel):
    condition: CompoundConditionOutput
    """Representation of a compound boolean statement, i.e.

    a negation, conjunction, or disjunction of UnaryConditions
    """

    max_iter: int

    name: str

    workflow: WorkflowItem
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

    loop_inputs: Optional[Dict[str, PlanLoopConfigOutputLoopInputs]] = None

    merge_outputs: Optional[Dict[str, str]] = None


Plan: TypeAlias = Union[WorkflowItem, PlanBranchConfigOutput, PlanLoopConfigOutput]


class WorkflowsWorkflowOutput(BaseModel):
    name: str

    nodes: List["NodeItemOutput"]


Workflows: TypeAlias = Union[WorkflowsWorkflowOutput, str, List["NodeItemOutput"]]


class PlanConfigOutput(BaseModel):
    plan: List[Plan]

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

    workflows: Optional[Dict[str, Workflows]] = None


from .node_item_output import NodeItemOutput

if PYDANTIC_V2:
    PlanConfigOutput.model_rebuild()
    PlanBranchConfigOutput.model_rebuild()
    PlanBranchConfigOutputConditionalWorkflow.model_rebuild()
    PlanLoopConfigOutput.model_rebuild()
    PlanLoopConfigOutputLoopInputsSelfEdge.model_rebuild()
    WorkflowsWorkflowOutput.model_rebuild()
else:
    PlanConfigOutput.update_forward_refs()  # type: ignore
    PlanBranchConfigOutput.update_forward_refs()  # type: ignore
    PlanBranchConfigOutputConditionalWorkflow.update_forward_refs()  # type: ignore
    PlanLoopConfigOutput.update_forward_refs()  # type: ignore
    PlanLoopConfigOutputLoopInputsSelfEdge.update_forward_refs()  # type: ignore
    WorkflowsWorkflowOutput.update_forward_refs()  # type: ignore
