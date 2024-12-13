# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .jinja_node_template_param import JinjaNodeTemplateParam
from .compound_condition_input_param import CompoundConditionInputParam

__all__ = [
    "NodeItemInputParam",
    "Config",
    "ConfigNodeConfig",
    "ConfigBatchedNodeConfig",
    "ConfigChunkEvaluationNodeConfig",
    "ConfigRerankerNodeConfig",
    "ConfigRetrieverNodeConfig",
    "ConfigCitationNodeConfig",
    "ConfigCitationNodeConfigCitationContext",
    "ConfigSearchCitationNodeConfig",
    "ConfigCodeExecutionConfig",
    "ConfigConditionNodeConfigInput",
    "ConfigDataTransformNodeConfig",
    "ConfigCreateMessagesNodeConfig",
    "ConfigCreateMessagesNodeConfigMessageConfig",
    "ConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages",
    "ConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages",
    "ConfigInsertMessagesConfig",
    "ConfigRemoveMessageConfig",
    "ConfigGetMessageConfig",
    "ConfigTokenizerChatTemplateConfig",
    "ConfigGenerationNodeConfig",
    "ConfigGenerationNodeConfigRetryConfig",
    "ConfigChatGenerationNodeConfig",
    "ConfigChatGenerationNodeConfigRetryConfig",
    "ConfigGenerationWithCitationsNodeConfig",
    "ConfigGenerationWithCitationsNodeConfigRetryConfig",
    "ConfigChatGenerationWithCitationsNodeConfig",
    "ConfigChatGenerationWithCitationsNodeConfigRetryConfig",
    "ConfigResponseParserNodeConfig",
    "ConfigJinjaNodeConfig",
    "ConfigProcessingNodeConfig",
    "ConfigProcessingNodeConfigFunctionSpecs",
    "ConfigRegexMatchNodeConfig",
    "ConfigSqlExecutorNodeConfig",
    "ConfigStaticNodeConfig",
    "ConfigLlmEngineNodeConfig",
    "ConfigLlmEngineNodeConfigBatchSysKwargs",
]


class ConfigNodeConfig(TypedDict, total=False):
    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigBatchedNodeConfig(TypedDict, total=False):
    batch_size: Required[int]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    split_approx_evenly: bool

    type_hints: Optional[object]


class ConfigChunkEvaluationNodeConfig(TypedDict, total=False):
    top_k_thresholds: Required[Iterable[int]]

    fuzzy_match_threshold: float

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    require_all: bool

    type_hints: Optional[object]


class ConfigRerankerNodeConfig(TypedDict, total=False):
    num_to_return: Required[int]

    scorers: Required[Iterable[object]]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    score_threshold: Optional[float]

    type_hints: Optional[object]


class ConfigRetrieverNodeConfig(TypedDict, total=False):
    num_to_return: Required[int]

    exact_knn_search: Optional[bool]

    knowledge_base_id: Optional[str]

    knowledge_base_name: Optional[str]

    metadata: Optional[Dict[str, Optional[str]]]

    min_results_per_knowledge_base: int

    node_metadata: Optional[List[str]]

    num_retriever_workers: int

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigCitationNodeConfigCitationContext(TypedDict, total=False):
    generate_with_llm: bool

    metric: Optional[str]

    min_similarity: Optional[float]

    score: Optional[Literal["precision", "recall", "fmeasure"]]


class ConfigCitationNodeConfig(TypedDict, total=False):
    citation_type: Required[Literal["rouge", "model_defined"]]

    citation_context: ConfigCitationNodeConfigCitationContext

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    s3_path_override: Optional[str]

    type_hints: Optional[object]


class ConfigSearchCitationNodeConfig(TypedDict, total=False):
    end_search_regex: Required[str]

    search_regex: Required[str]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigCodeExecutionConfig(TypedDict, total=False):
    files: Required[Dict[str, str]]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    output_artifacts_dir: Optional[str]

    type_hints: Optional[object]


class ConfigConditionNodeConfigInput(TypedDict, total=False):
    condition: Required[CompoundConditionInputParam]
    """Representation of a compound boolean statement, i.e.

    a negation, conjunction, or disjunction of UnaryConditions
    """

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigDataTransformNodeConfig(TypedDict, total=False):
    action: Required[str]

    additional_inputs: object

    apply_to_dictlist_leaves: bool

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages(TypedDict, total=False):
    role_value_pairs: Required[Iterable[Dict[str, str]]]


class ConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages(TypedDict, total=False):
    content: Required[str]

    role: Required[str]


ConfigCreateMessagesNodeConfigMessageConfig: TypeAlias = Union[
    ConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages,
    ConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages,
]


class ConfigCreateMessagesNodeConfig(TypedDict, total=False):
    message_configs: Required[Iterable[ConfigCreateMessagesNodeConfigMessageConfig]]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigInsertMessagesConfig(TypedDict, total=False):
    index: Required[int]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigRemoveMessageConfig(TypedDict, total=False):
    index: Required[int]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigGetMessageConfig(TypedDict, total=False):
    index: Required[int]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigTokenizerChatTemplateConfig(TypedDict, total=False):
    llm_model: Required[str]

    add_generation_prompt: bool

    kwargs: object

    max_length: Optional[int]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    padding: bool

    truncation: bool

    type_hints: Optional[object]


class ConfigGenerationNodeConfigRetryConfig(TypedDict, total=False):
    backoff: int

    delay: int

    exceptions: List[Literal["SGPClientError", "APITimeoutError", "InternalServerError", "RateLimitError", "Exception"]]

    tries: int


class ConfigGenerationNodeConfig(TypedDict, total=False):
    llm_model: str

    llm_model_deployment: Optional[str]

    llm_model_instance: Optional[str]

    max_tokens: int

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    retry_config: ConfigGenerationNodeConfigRetryConfig

    stop_sequences: Optional[List[str]]

    strip_whitespace: bool

    temperature: float

    tool_name: Optional[str]

    type_hints: Optional[object]


class ConfigChatGenerationNodeConfigRetryConfig(TypedDict, total=False):
    backoff: int

    delay: int

    exceptions: List[Literal["SGPClientError", "APITimeoutError", "InternalServerError", "RateLimitError", "Exception"]]

    tries: int


class ConfigChatGenerationNodeConfig(TypedDict, total=False):
    memory_strategy: Required[object]

    instructions: Optional[str]

    llm_model: str

    llm_model_deployment: Optional[str]

    llm_model_instance: Optional[str]

    max_tokens: int

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    retry_config: ConfigChatGenerationNodeConfigRetryConfig

    stop_sequences: Optional[List[str]]

    strip_whitespace: bool

    temperature: float

    tool_name: Optional[str]

    type_hints: Optional[object]


class ConfigGenerationWithCitationsNodeConfigRetryConfig(TypedDict, total=False):
    backoff: int

    delay: int

    exceptions: List[Literal["SGPClientError", "APITimeoutError", "InternalServerError", "RateLimitError", "Exception"]]

    tries: int


class ConfigGenerationWithCitationsNodeConfig(TypedDict, total=False):
    regex_pattern: Required[str]

    regex_replace: Required[str]

    llm_model: str

    llm_model_deployment: Optional[str]

    llm_model_instance: Optional[str]

    max_tokens: int

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    retry_config: ConfigGenerationWithCitationsNodeConfigRetryConfig

    stop_sequences: Optional[List[str]]

    strip_whitespace: bool

    temperature: float

    tool_name: Optional[str]

    type_hints: Optional[object]


class ConfigChatGenerationWithCitationsNodeConfigRetryConfig(TypedDict, total=False):
    backoff: int

    delay: int

    exceptions: List[Literal["SGPClientError", "APITimeoutError", "InternalServerError", "RateLimitError", "Exception"]]

    tries: int


class ConfigChatGenerationWithCitationsNodeConfig(TypedDict, total=False):
    memory_strategy: Required[object]

    regex_pattern: Required[str]

    regex_replace: Required[str]

    instructions: Optional[str]

    llm_model: str

    llm_model_deployment: Optional[str]

    llm_model_instance: Optional[str]

    max_tokens: int

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    retry_config: ConfigChatGenerationWithCitationsNodeConfigRetryConfig

    stop_sequences: Optional[List[str]]

    strip_whitespace: bool

    temperature: float

    tool_name: Optional[str]

    type_hints: Optional[object]


class ConfigResponseParserNodeConfig(TypedDict, total=False):
    action: Required[str]

    reference_value: Required[object]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigJinjaNodeConfig(TypedDict, total=False):
    context_chunks_key: Optional[str]

    data_transformations: Dict[str, JinjaNodeTemplateParam]

    llm_model: Optional[str]

    log_output: bool

    log_prefix: str

    max_tokens: Optional[int]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    output_template: JinjaNodeTemplateParam
    """
    Base model for a Jinja template. Guaranteed to store a string that can be read
    in to Template().
    """

    type_hints: Optional[object]

    verbose: bool


class ConfigProcessingNodeConfigFunctionSpecs(TypedDict, total=False):
    kwargs: Required[object]

    path: Required[str]


class ConfigProcessingNodeConfig(TypedDict, total=False):
    function_specs: Required[Dict[str, ConfigProcessingNodeConfigFunctionSpecs]]

    return_key: Required[str]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigRegexMatchNodeConfig(TypedDict, total=False):
    pattern: Required[str]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]


class ConfigSqlExecutorNodeConfig(TypedDict, total=False):
    connector_kwargs: Required[Dict[str, str]]

    connector_type: Literal["snowflake"]

    log_queries: bool

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    return_type: Literal["df", "dicts", "markdown", "json", "str"]

    schema_remapping_file: Optional[str]

    secrets: List[str]

    type_hints: Optional[object]


class ConfigStaticNodeConfig(TypedDict, total=False):
    from_file: Union[Iterable[object], str, object, None]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    type_hints: Optional[object]

    value: Optional[object]


class ConfigLlmEngineNodeConfigBatchSysKwargs(TypedDict, total=False):
    checkpoint_path: Optional[str]

    labels: Optional[Dict[str, str]]

    num_shards: Optional[int]

    seed: Optional[int]


class ConfigLlmEngineNodeConfig(TypedDict, total=False):
    llm_model: Required[str]

    batch_run_mode: Literal["sync", "async"]

    batch_sys_kwargs: ConfigLlmEngineNodeConfigBatchSysKwargs

    frequency_penalty: Optional[float]

    guided_choice: Optional[List[str]]

    guided_json: Optional[object]

    guided_regex: Optional[str]

    include_stop_str_in_output: Optional[bool]

    max_tokens: Optional[int]

    node_metadata: Optional[List[str]]

    num_workers: Optional[int]

    presence_penalty: Optional[float]

    stop_sequences: Optional[List[str]]

    temperature: Optional[float]

    timeout: int

    top_k: Optional[int]

    top_p: Optional[float]

    type_hints: Optional[object]


Config: TypeAlias = Union[
    ConfigNodeConfig,
    ConfigBatchedNodeConfig,
    ConfigChunkEvaluationNodeConfig,
    ConfigRerankerNodeConfig,
    ConfigRetrieverNodeConfig,
    ConfigCitationNodeConfig,
    ConfigSearchCitationNodeConfig,
    ConfigCodeExecutionConfig,
    ConfigConditionNodeConfigInput,
    ConfigDataTransformNodeConfig,
    ConfigCreateMessagesNodeConfig,
    ConfigInsertMessagesConfig,
    ConfigRemoveMessageConfig,
    ConfigGetMessageConfig,
    ConfigTokenizerChatTemplateConfig,
    ConfigGenerationNodeConfig,
    ConfigChatGenerationNodeConfig,
    ConfigGenerationWithCitationsNodeConfig,
    ConfigChatGenerationWithCitationsNodeConfig,
    ConfigResponseParserNodeConfig,
    ConfigJinjaNodeConfig,
    ConfigProcessingNodeConfig,
    ConfigRegexMatchNodeConfig,
    ConfigSqlExecutorNodeConfig,
    ConfigStaticNodeConfig,
    ConfigLlmEngineNodeConfig,
]


class NodeItemInputParam(TypedDict, total=False):
    config: Required[Config]
    """A data model describing parameters for back-citation using ROUGE similarity.

    metric is the ROUGE metric to use (e.g. rouge1, rouge2, rougeLsum) score is one
    of "precision", "recall", "fmeasure"

    NOTE (john): copied directly from generation.py in order to subclass from
    NodeConfig.
    """

    name: Required[str]

    type: Required[str]

    inputs: Dict[str, Union[str, Dict[str, Union[str, object]]]]
