# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .unary_condition_param import UnaryConditionParam
from .compound_condition_input_param import CompoundConditionInputParam

__all__ = [
    "ConfigCreateParams",
    "Config",
    "ConfigStateMachineConfigInput",
    "ConfigStateMachineConfigInputMachine",
    "ConfigStateMachineConfigInputMachineNextNode",
    "ConfigStateMachineConfigInputMachineNextNodeCase",
    "ConfigStateMachineConfigInputMachineNextNodeCaseCondition",
    "ConfigStateMachineConfigInputAutoAggregatatorConfig",
]


class ConfigCreateParams(TypedDict, total=False):
    config: Required[Config]
    """Representation of a plan, i.e. a composition of workflows and branch complexes

    Public attributes: workflows: maps a workflow "name" to either a workflow yaml
    file or an inline workflow definition plan: representation of the graph
    connecting workflows / branch complexes

    Private attributes: helper_workflows: a list of workflows created by default, in
    order to support loops and other control flow features
    """


ConfigStateMachineConfigInputMachineNextNodeCaseCondition: TypeAlias = Union[
    UnaryConditionParam, CompoundConditionInputParam
]


class ConfigStateMachineConfigInputMachineNextNodeCase(TypedDict, total=False):
    condition: Required[ConfigStateMachineConfigInputMachineNextNodeCaseCondition]
    """Representation of a boolean function with a single input e.g.

    the condition specified by input_name: x operator: 'contains' ref_value: 'c'
    would evaluate to True if x == 'cat' Operators are defined in the constant
    function store CONDITIONAL_ACTION_MAP
    """

    value: Required[str]


class ConfigStateMachineConfigInputMachineNextNode(TypedDict, total=False):
    default: Required[str]

    cases: Iterable[ConfigStateMachineConfigInputMachineNextNodeCase]


class ConfigStateMachineConfigInputMachine(TypedDict, total=False):
    next_node: Required[ConfigStateMachineConfigInputMachineNextNode]
    """A switch statement for state machines to select the next state to execute."""

    workflow_config: Required["WorkflowConfigInputParam"]

    write_to_state: Dict[str, str]


class ConfigStateMachineConfigInputAutoAggregatatorConfig(TypedDict, total=False):
    aggregate_inputs_workflow_config: Optional["WorkflowConfigInputParam"]

    ask_inputs_workflow_config: Optional["WorkflowConfigInputParam"]


class ConfigStateMachineConfigInput(TypedDict, total=False):
    machine: Required[Dict[str, ConfigStateMachineConfigInputMachine]]

    starting_node: Required[str]

    id: Optional[str]

    account_id: Optional[str]

    application_variant_id: Optional[str]

    auto_aggregatator_config: Optional[ConfigStateMachineConfigInputAutoAggregatatorConfig]

    base_url: Optional[str]

    concurrency_default: bool

    datasets: Optional[Iterable[object]]

    done_string: str

    egp_api_key_override: Optional[str]

    egp_ui_evaluation: Optional[object]

    evaluations: Optional[Iterable["NodeItemInputParam"]]

    final_output_nodes: Optional[List[str]]

    initial_state: object

    nodes_to_log: Union[str, List[str], None]

    num_workers: Optional[int]

    streaming_nodes: Optional[List[str]]

    subtype: Optional[Literal["chat", "report"]]

    type: Optional[Literal["workflow", "plan", "state_machine"]]

    user_input: object


Config: TypeAlias = Union["PlanConfigInputParam", "WorkflowConfigInputParam", ConfigStateMachineConfigInput]

from .node_item_input_param import NodeItemInputParam
from .plan_config_input_param import PlanConfigInputParam
from .workflow_config_input_param import WorkflowConfigInputParam
