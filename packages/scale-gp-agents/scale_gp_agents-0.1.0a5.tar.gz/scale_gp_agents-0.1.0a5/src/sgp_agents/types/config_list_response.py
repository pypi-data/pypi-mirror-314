# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._compat import PYDANTIC_V2
from .._models import BaseModel
from .unary_condition import UnaryCondition
from .node_item_output import NodeItemOutput
from .plan_config_output import PlanConfigOutput
from .workflow_config_output import WorkflowConfigOutput
from .compound_condition_output import CompoundConditionOutput

__all__ = [
    "ConfigListResponse",
    "ConfigListResponseItem",
    "ConfigListResponseItemStateMachineConfigOutput",
    "ConfigListResponseItemStateMachineConfigOutputMachine",
    "ConfigListResponseItemStateMachineConfigOutputMachineNextNode",
    "ConfigListResponseItemStateMachineConfigOutputMachineNextNodeCase",
    "ConfigListResponseItemStateMachineConfigOutputMachineNextNodeCaseCondition",
    "ConfigListResponseItemStateMachineConfigOutputAutoAggregatatorConfig",
]

ConfigListResponseItemStateMachineConfigOutputMachineNextNodeCaseCondition: TypeAlias = Union[
    UnaryCondition, CompoundConditionOutput
]


class ConfigListResponseItemStateMachineConfigOutputMachineNextNodeCase(BaseModel):
    condition: ConfigListResponseItemStateMachineConfigOutputMachineNextNodeCaseCondition
    """Representation of a boolean function with a single input e.g.

    the condition specified by input_name: x operator: 'contains' ref_value: 'c'
    would evaluate to True if x == 'cat' Operators are defined in the constant
    function store CONDITIONAL_ACTION_MAP
    """

    value: str


class ConfigListResponseItemStateMachineConfigOutputMachineNextNode(BaseModel):
    default: str

    cases: Optional[List[ConfigListResponseItemStateMachineConfigOutputMachineNextNodeCase]] = None


class ConfigListResponseItemStateMachineConfigOutputMachine(BaseModel):
    next_node: ConfigListResponseItemStateMachineConfigOutputMachineNextNode
    """A switch statement for state machines to select the next state to execute."""

    workflow_config: "WorkflowConfigOutput"

    write_to_state: Optional[Dict[str, str]] = None


class ConfigListResponseItemStateMachineConfigOutputAutoAggregatatorConfig(BaseModel):
    aggregate_inputs_workflow_config: Optional["WorkflowConfigOutput"] = None

    ask_inputs_workflow_config: Optional["WorkflowConfigOutput"] = None


class ConfigListResponseItemStateMachineConfigOutput(BaseModel):
    machine: Dict[str, ConfigListResponseItemStateMachineConfigOutputMachine]

    starting_node: str

    id: Optional[str] = None

    account_id: Optional[str] = None

    application_variant_id: Optional[str] = None

    auto_aggregatator_config: Optional[ConfigListResponseItemStateMachineConfigOutputAutoAggregatatorConfig] = None

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


ConfigListResponseItem: TypeAlias = Union[
    PlanConfigOutput, WorkflowConfigOutput, ConfigListResponseItemStateMachineConfigOutput
]

ConfigListResponse: TypeAlias = List[ConfigListResponseItem]

if PYDANTIC_V2:
    ConfigListResponseItemStateMachineConfigOutput.model_rebuild()
    ConfigListResponseItemStateMachineConfigOutputMachine.model_rebuild()
    ConfigListResponseItemStateMachineConfigOutputMachineNextNode.model_rebuild()
    ConfigListResponseItemStateMachineConfigOutputMachineNextNodeCase.model_rebuild()
    ConfigListResponseItemStateMachineConfigOutputAutoAggregatatorConfig.model_rebuild()
else:
    ConfigListResponseItemStateMachineConfigOutput.update_forward_refs()  # type: ignore
    ConfigListResponseItemStateMachineConfigOutputMachine.update_forward_refs()  # type: ignore
    ConfigListResponseItemStateMachineConfigOutputMachineNextNode.update_forward_refs()  # type: ignore
    ConfigListResponseItemStateMachineConfigOutputMachineNextNodeCase.update_forward_refs()  # type: ignore
    ConfigListResponseItemStateMachineConfigOutputAutoAggregatatorConfig.update_forward_refs()  # type: ignore
