# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._compat import PYDANTIC_V2
from .._models import BaseModel
from .unary_condition import UnaryCondition
from .compound_condition_output import CompoundConditionOutput

__all__ = [
    "ConfigCreateResponse",
    "Config",
    "ConfigStateMachineConfigOutput",
    "ConfigStateMachineConfigOutputMachine",
    "ConfigStateMachineConfigOutputMachineNextNode",
    "ConfigStateMachineConfigOutputMachineNextNodeCase",
    "ConfigStateMachineConfigOutputMachineNextNodeCaseCondition",
    "ConfigStateMachineConfigOutputAutoAggregatatorConfig",
    "Graph",
    "GraphEdge",
    "GraphNode",
    "GraphNodeEdge",
    "GraphNodeNode",
    "GraphNodeNodeEdge",
]

ConfigStateMachineConfigOutputMachineNextNodeCaseCondition: TypeAlias = Union[UnaryCondition, CompoundConditionOutput]


class ConfigStateMachineConfigOutputMachineNextNodeCase(BaseModel):
    condition: ConfigStateMachineConfigOutputMachineNextNodeCaseCondition
    """Representation of a boolean function with a single input e.g.

    the condition specified by input_name: x operator: 'contains' ref_value: 'c'
    would evaluate to True if x == 'cat' Operators are defined in the constant
    function store CONDITIONAL_ACTION_MAP
    """

    value: str


class ConfigStateMachineConfigOutputMachineNextNode(BaseModel):
    default: str

    cases: Optional[List[ConfigStateMachineConfigOutputMachineNextNodeCase]] = None


class ConfigStateMachineConfigOutputMachine(BaseModel):
    next_node: ConfigStateMachineConfigOutputMachineNextNode
    """A switch statement for state machines to select the next state to execute."""

    workflow_config: "WorkflowConfigOutput"

    write_to_state: Optional[Dict[str, str]] = None


class ConfigStateMachineConfigOutputAutoAggregatatorConfig(BaseModel):
    aggregate_inputs_workflow_config: Optional["WorkflowConfigOutput"] = None

    ask_inputs_workflow_config: Optional["WorkflowConfigOutput"] = None


class ConfigStateMachineConfigOutput(BaseModel):
    machine: Dict[str, ConfigStateMachineConfigOutputMachine]

    starting_node: str

    id: Optional[str] = None

    account_id: Optional[str] = None

    application_variant_id: Optional[str] = None

    auto_aggregatator_config: Optional[ConfigStateMachineConfigOutputAutoAggregatatorConfig] = None

    base_url: Optional[str] = None

    concurrency_default: Optional[bool] = None

    datasets: Optional[List[object]] = None

    done_string: Optional[str] = None

    egp_api_key_override: Optional[str] = None

    egp_ui_evaluation: Optional[object] = None

    evaluations: Optional[List["NodeItemOutput"]] = None

    final_output_nodes: Optional[List[str]] = None

    initial_state: Optional[object] = None

    nodes_to_log: Union[str, List[str], None] = None

    num_workers: Optional[int] = None

    streaming_nodes: Optional[List[str]] = None

    subtype: Optional[Literal["chat", "report"]] = None

    type: Optional[Literal["workflow", "plan", "state_machine"]] = None

    user_input: Optional[object] = None


Config: TypeAlias = Union["PlanConfigOutput", "WorkflowConfigOutput", ConfigStateMachineConfigOutput]


class GraphEdge(BaseModel):
    from_node: str

    to_node: str


class GraphNodeEdge(BaseModel):
    from_node: str

    to_node: str


class GraphNodeNodeEdge(BaseModel):
    from_node: str

    to_node: str


class GraphNodeNode(BaseModel):
    type: str

    id: Optional[str] = None

    config: Optional[object] = None

    edges: Optional[List[GraphNodeNodeEdge]] = None

    name: Optional[str] = None

    nodes: Optional[List[object]] = None


class GraphNode(BaseModel):
    type: str

    id: Optional[str] = None

    config: Optional[object] = None

    edges: Optional[List[GraphNodeEdge]] = None

    name: Optional[str] = None

    nodes: Optional[List[GraphNodeNode]] = None


class Graph(BaseModel):
    type: str

    id: Optional[str] = None

    config: Optional[object] = None

    edges: Optional[List[GraphEdge]] = None

    name: Optional[str] = None

    nodes: Optional[List[GraphNode]] = None


class ConfigCreateResponse(BaseModel):
    config: Config
    """Representation of a plan, i.e. a composition of workflows and branch complexes

    Public attributes: workflows: maps a workflow "name" to either a workflow yaml
    file or an inline workflow definition plan: representation of the graph
    connecting workflows / branch complexes

    Private attributes: helper_workflows: a list of workflows created by default, in
    order to support loops and other control flow features
    """

    graph: Graph

    user_inputs: object


from .node_item_output import NodeItemOutput
from .plan_config_output import PlanConfigOutput
from .workflow_config_output import WorkflowConfigOutput

if PYDANTIC_V2:
    ConfigCreateResponse.model_rebuild()
    ConfigStateMachineConfigOutput.model_rebuild()
    ConfigStateMachineConfigOutputMachine.model_rebuild()
    ConfigStateMachineConfigOutputMachineNextNode.model_rebuild()
    ConfigStateMachineConfigOutputMachineNextNodeCase.model_rebuild()
    ConfigStateMachineConfigOutputAutoAggregatatorConfig.model_rebuild()
    Graph.model_rebuild()
    GraphEdge.model_rebuild()
    GraphNode.model_rebuild()
    GraphNodeEdge.model_rebuild()
    GraphNodeNode.model_rebuild()
    GraphNodeNodeEdge.model_rebuild()
else:
    ConfigCreateResponse.update_forward_refs()  # type: ignore
    ConfigStateMachineConfigOutput.update_forward_refs()  # type: ignore
    ConfigStateMachineConfigOutputMachine.update_forward_refs()  # type: ignore
    ConfigStateMachineConfigOutputMachineNextNode.update_forward_refs()  # type: ignore
    ConfigStateMachineConfigOutputMachineNextNodeCase.update_forward_refs()  # type: ignore
    ConfigStateMachineConfigOutputAutoAggregatatorConfig.update_forward_refs()  # type: ignore
    Graph.update_forward_refs()  # type: ignore
    GraphEdge.update_forward_refs()  # type: ignore
    GraphNode.update_forward_refs()  # type: ignore
    GraphNodeEdge.update_forward_refs()  # type: ignore
    GraphNodeNode.update_forward_refs()  # type: ignore
    GraphNodeNodeEdge.update_forward_refs()  # type: ignore
