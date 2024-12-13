# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._compat import PYDANTIC_V2
from .._models import BaseModel
from .jinja_node_template import JinjaNodeTemplate
from .compound_condition_output import CompoundConditionOutput

__all__ = [
    "NodeItemOutput",
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
    "ConfigConditionNodeConfigOutput",
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


class ConfigNodeConfig(BaseModel):
    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigBatchedNodeConfig(BaseModel):
    batch_size: int

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    split_approx_evenly: Optional[bool] = None

    type_hints: Optional[object] = None


class ConfigChunkEvaluationNodeConfig(BaseModel):
    top_k_thresholds: List[int]

    fuzzy_match_threshold: Optional[float] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    require_all: Optional[bool] = None

    type_hints: Optional[object] = None


class ConfigRerankerNodeConfig(BaseModel):
    num_to_return: int

    scorers: List[object]

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    score_threshold: Optional[float] = None

    type_hints: Optional[object] = None


class ConfigRetrieverNodeConfig(BaseModel):
    num_to_return: int

    exact_knn_search: Optional[bool] = None

    knowledge_base_id: Optional[str] = None

    knowledge_base_name: Optional[str] = None

    metadata: Optional[Dict[str, Optional[str]]] = None

    min_results_per_knowledge_base: Optional[int] = None

    node_metadata: Optional[List[str]] = None

    num_retriever_workers: Optional[int] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigCitationNodeConfigCitationContext(BaseModel):
    generate_with_llm: Optional[bool] = None

    metric: Optional[str] = None

    min_similarity: Optional[float] = None

    score: Optional[Literal["precision", "recall", "fmeasure"]] = None


class ConfigCitationNodeConfig(BaseModel):
    citation_type: Literal["rouge", "model_defined"]

    citation_context: Optional[ConfigCitationNodeConfigCitationContext] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    s3_path_override: Optional[str] = None

    type_hints: Optional[object] = None


class ConfigSearchCitationNodeConfig(BaseModel):
    end_search_regex: str

    search_regex: str

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigCodeExecutionConfig(BaseModel):
    files: Dict[str, str]

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    output_artifacts_dir: Optional[str] = None

    type_hints: Optional[object] = None


class ConfigConditionNodeConfigOutput(BaseModel):
    condition: CompoundConditionOutput
    """Representation of a compound boolean statement, i.e.

    a negation, conjunction, or disjunction of UnaryConditions
    """

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigDataTransformNodeConfig(BaseModel):
    action: str

    additional_inputs: Optional[object] = None

    apply_to_dictlist_leaves: Optional[bool] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages(BaseModel):
    role_value_pairs: List[Dict[str, str]]


class ConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages(BaseModel):
    content: str

    role: str


ConfigCreateMessagesNodeConfigMessageConfig: TypeAlias = Union[
    ConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages,
    ConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages,
]


class ConfigCreateMessagesNodeConfig(BaseModel):
    message_configs: List[ConfigCreateMessagesNodeConfigMessageConfig]

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigInsertMessagesConfig(BaseModel):
    index: int

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigRemoveMessageConfig(BaseModel):
    index: int

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigGetMessageConfig(BaseModel):
    index: int

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigTokenizerChatTemplateConfig(BaseModel):
    llm_model: str

    add_generation_prompt: Optional[bool] = None

    kwargs: Optional[object] = None

    max_length: Optional[int] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    padding: Optional[bool] = None

    truncation: Optional[bool] = None

    type_hints: Optional[object] = None


class ConfigGenerationNodeConfigRetryConfig(BaseModel):
    backoff: Optional[int] = None

    delay: Optional[int] = None

    exceptions: Optional[
        List[Literal["SGPClientError", "APITimeoutError", "InternalServerError", "RateLimitError", "Exception"]]
    ] = None

    tries: Optional[int] = None


class ConfigGenerationNodeConfig(BaseModel):
    llm_model: Optional[str] = None

    llm_model_deployment: Optional[str] = None

    llm_model_instance: Optional[str] = None

    max_tokens: Optional[int] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    retry_config: Optional[ConfigGenerationNodeConfigRetryConfig] = None

    stop_sequences: Optional[List[str]] = None

    strip_whitespace: Optional[bool] = None

    temperature: Optional[float] = None

    tool_name: Optional[str] = None

    type_hints: Optional[object] = None


class ConfigChatGenerationNodeConfigRetryConfig(BaseModel):
    backoff: Optional[int] = None

    delay: Optional[int] = None

    exceptions: Optional[
        List[Literal["SGPClientError", "APITimeoutError", "InternalServerError", "RateLimitError", "Exception"]]
    ] = None

    tries: Optional[int] = None


class ConfigChatGenerationNodeConfig(BaseModel):
    memory_strategy: object

    instructions: Optional[str] = None

    llm_model: Optional[str] = None

    llm_model_deployment: Optional[str] = None

    llm_model_instance: Optional[str] = None

    max_tokens: Optional[int] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    retry_config: Optional[ConfigChatGenerationNodeConfigRetryConfig] = None

    stop_sequences: Optional[List[str]] = None

    strip_whitespace: Optional[bool] = None

    temperature: Optional[float] = None

    tool_name: Optional[str] = None

    type_hints: Optional[object] = None


class ConfigGenerationWithCitationsNodeConfigRetryConfig(BaseModel):
    backoff: Optional[int] = None

    delay: Optional[int] = None

    exceptions: Optional[
        List[Literal["SGPClientError", "APITimeoutError", "InternalServerError", "RateLimitError", "Exception"]]
    ] = None

    tries: Optional[int] = None


class ConfigGenerationWithCitationsNodeConfig(BaseModel):
    regex_pattern: str

    regex_replace: str

    llm_model: Optional[str] = None

    llm_model_deployment: Optional[str] = None

    llm_model_instance: Optional[str] = None

    max_tokens: Optional[int] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    retry_config: Optional[ConfigGenerationWithCitationsNodeConfigRetryConfig] = None

    stop_sequences: Optional[List[str]] = None

    strip_whitespace: Optional[bool] = None

    temperature: Optional[float] = None

    tool_name: Optional[str] = None

    type_hints: Optional[object] = None


class ConfigChatGenerationWithCitationsNodeConfigRetryConfig(BaseModel):
    backoff: Optional[int] = None

    delay: Optional[int] = None

    exceptions: Optional[
        List[Literal["SGPClientError", "APITimeoutError", "InternalServerError", "RateLimitError", "Exception"]]
    ] = None

    tries: Optional[int] = None


class ConfigChatGenerationWithCitationsNodeConfig(BaseModel):
    memory_strategy: object

    regex_pattern: str

    regex_replace: str

    instructions: Optional[str] = None

    llm_model: Optional[str] = None

    llm_model_deployment: Optional[str] = None

    llm_model_instance: Optional[str] = None

    max_tokens: Optional[int] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    retry_config: Optional[ConfigChatGenerationWithCitationsNodeConfigRetryConfig] = None

    stop_sequences: Optional[List[str]] = None

    strip_whitespace: Optional[bool] = None

    temperature: Optional[float] = None

    tool_name: Optional[str] = None

    type_hints: Optional[object] = None


class ConfigResponseParserNodeConfig(BaseModel):
    action: str

    reference_value: object

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigJinjaNodeConfig(BaseModel):
    context_chunks_key: Optional[str] = None

    data_transformations: Optional[Dict[str, JinjaNodeTemplate]] = None

    llm_model: Optional[str] = None

    log_output: Optional[bool] = None

    log_prefix: Optional[str] = None

    max_tokens: Optional[int] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    output_template: Optional[JinjaNodeTemplate] = None
    """
    Base model for a Jinja template. Guaranteed to store a string that can be read
    in to Template().
    """

    type_hints: Optional[object] = None

    verbose: Optional[bool] = None


class ConfigProcessingNodeConfigFunctionSpecs(BaseModel):
    kwargs: object

    path: str


class ConfigProcessingNodeConfig(BaseModel):
    function_specs: Dict[str, ConfigProcessingNodeConfigFunctionSpecs]

    return_key: str

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigRegexMatchNodeConfig(BaseModel):
    pattern: str

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None


class ConfigSqlExecutorNodeConfig(BaseModel):
    connector_kwargs: Dict[str, str]

    connector_type: Optional[Literal["snowflake"]] = None

    log_queries: Optional[bool] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    return_type: Optional[Literal["df", "dicts", "markdown", "json", "str"]] = None

    schema_remapping_file: Optional[str] = None

    secrets: Optional[List[str]] = None

    type_hints: Optional[object] = None


class ConfigStaticNodeConfig(BaseModel):
    from_file: Union[List[object], str, object, None] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    type_hints: Optional[object] = None

    value: Optional[object] = None


class ConfigLlmEngineNodeConfigBatchSysKwargs(BaseModel):
    checkpoint_path: Optional[str] = None

    labels: Optional[Dict[str, str]] = None

    num_shards: Optional[int] = None

    seed: Optional[int] = None


class ConfigLlmEngineNodeConfig(BaseModel):
    llm_model: str

    batch_run_mode: Optional[Literal["sync", "async"]] = None

    batch_sys_kwargs: Optional[ConfigLlmEngineNodeConfigBatchSysKwargs] = None

    frequency_penalty: Optional[float] = None

    guided_choice: Optional[List[str]] = None

    guided_json: Optional[object] = None

    guided_regex: Optional[str] = None

    include_stop_str_in_output: Optional[bool] = None

    max_tokens: Optional[int] = None

    node_metadata: Optional[List[str]] = None

    num_workers: Optional[int] = None

    presence_penalty: Optional[float] = None

    stop_sequences: Optional[List[str]] = None

    temperature: Optional[float] = None

    timeout: Optional[int] = None

    top_k: Optional[int] = None

    top_p: Optional[float] = None

    type_hints: Optional[object] = None


Config: TypeAlias = Union[
    ConfigNodeConfig,
    ConfigBatchedNodeConfig,
    ConfigChunkEvaluationNodeConfig,
    ConfigRerankerNodeConfig,
    ConfigRetrieverNodeConfig,
    ConfigCitationNodeConfig,
    ConfigSearchCitationNodeConfig,
    ConfigCodeExecutionConfig,
    ConfigConditionNodeConfigOutput,
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


class NodeItemOutput(BaseModel):
    config: Config
    """A data model describing parameters for back-citation using ROUGE similarity.

    metric is the ROUGE metric to use (e.g. rouge1, rouge2, rougeLsum) score is one
    of "precision", "recall", "fmeasure"

    NOTE (john): copied directly from generation.py in order to subclass from
    NodeConfig.
    """

    name: str

    type: str

    inputs: Optional[Dict[str, Union[str, Dict[str, Union[str, object]]]]] = None


if PYDANTIC_V2:
    NodeItemOutput.model_rebuild()
    ConfigNodeConfig.model_rebuild()
    ConfigBatchedNodeConfig.model_rebuild()
    ConfigChunkEvaluationNodeConfig.model_rebuild()
    ConfigRerankerNodeConfig.model_rebuild()
    ConfigRetrieverNodeConfig.model_rebuild()
    ConfigCitationNodeConfig.model_rebuild()
    ConfigCitationNodeConfigCitationContext.model_rebuild()
    ConfigSearchCitationNodeConfig.model_rebuild()
    ConfigCodeExecutionConfig.model_rebuild()
    ConfigConditionNodeConfigOutput.model_rebuild()
    ConfigDataTransformNodeConfig.model_rebuild()
    ConfigCreateMessagesNodeConfig.model_rebuild()
    ConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages.model_rebuild()
    ConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages.model_rebuild()
    ConfigInsertMessagesConfig.model_rebuild()
    ConfigRemoveMessageConfig.model_rebuild()
    ConfigGetMessageConfig.model_rebuild()
    ConfigTokenizerChatTemplateConfig.model_rebuild()
    ConfigGenerationNodeConfig.model_rebuild()
    ConfigGenerationNodeConfigRetryConfig.model_rebuild()
    ConfigChatGenerationNodeConfig.model_rebuild()
    ConfigChatGenerationNodeConfigRetryConfig.model_rebuild()
    ConfigGenerationWithCitationsNodeConfig.model_rebuild()
    ConfigGenerationWithCitationsNodeConfigRetryConfig.model_rebuild()
    ConfigChatGenerationWithCitationsNodeConfig.model_rebuild()
    ConfigChatGenerationWithCitationsNodeConfigRetryConfig.model_rebuild()
    ConfigResponseParserNodeConfig.model_rebuild()
    ConfigJinjaNodeConfig.model_rebuild()
    ConfigProcessingNodeConfig.model_rebuild()
    ConfigProcessingNodeConfigFunctionSpecs.model_rebuild()
    ConfigRegexMatchNodeConfig.model_rebuild()
    ConfigSqlExecutorNodeConfig.model_rebuild()
    ConfigStaticNodeConfig.model_rebuild()
    ConfigLlmEngineNodeConfig.model_rebuild()
    ConfigLlmEngineNodeConfigBatchSysKwargs.model_rebuild()
else:
    NodeItemOutput.update_forward_refs()  # type: ignore
    ConfigNodeConfig.update_forward_refs()  # type: ignore
    ConfigBatchedNodeConfig.update_forward_refs()  # type: ignore
    ConfigChunkEvaluationNodeConfig.update_forward_refs()  # type: ignore
    ConfigRerankerNodeConfig.update_forward_refs()  # type: ignore
    ConfigRetrieverNodeConfig.update_forward_refs()  # type: ignore
    ConfigCitationNodeConfig.update_forward_refs()  # type: ignore
    ConfigCitationNodeConfigCitationContext.update_forward_refs()  # type: ignore
    ConfigSearchCitationNodeConfig.update_forward_refs()  # type: ignore
    ConfigCodeExecutionConfig.update_forward_refs()  # type: ignore
    ConfigConditionNodeConfigOutput.update_forward_refs()  # type: ignore
    ConfigDataTransformNodeConfig.update_forward_refs()  # type: ignore
    ConfigCreateMessagesNodeConfig.update_forward_refs()  # type: ignore
    ConfigCreateMessagesNodeConfigMessageConfigAlternatingRoleMessages.update_forward_refs()  # type: ignore
    ConfigCreateMessagesNodeConfigMessageConfigSingleRoleMessages.update_forward_refs()  # type: ignore
    ConfigInsertMessagesConfig.update_forward_refs()  # type: ignore
    ConfigRemoveMessageConfig.update_forward_refs()  # type: ignore
    ConfigGetMessageConfig.update_forward_refs()  # type: ignore
    ConfigTokenizerChatTemplateConfig.update_forward_refs()  # type: ignore
    ConfigGenerationNodeConfig.update_forward_refs()  # type: ignore
    ConfigGenerationNodeConfigRetryConfig.update_forward_refs()  # type: ignore
    ConfigChatGenerationNodeConfig.update_forward_refs()  # type: ignore
    ConfigChatGenerationNodeConfigRetryConfig.update_forward_refs()  # type: ignore
    ConfigGenerationWithCitationsNodeConfig.update_forward_refs()  # type: ignore
    ConfigGenerationWithCitationsNodeConfigRetryConfig.update_forward_refs()  # type: ignore
    ConfigChatGenerationWithCitationsNodeConfig.update_forward_refs()  # type: ignore
    ConfigChatGenerationWithCitationsNodeConfigRetryConfig.update_forward_refs()  # type: ignore
    ConfigResponseParserNodeConfig.update_forward_refs()  # type: ignore
    ConfigJinjaNodeConfig.update_forward_refs()  # type: ignore
    ConfigProcessingNodeConfig.update_forward_refs()  # type: ignore
    ConfigProcessingNodeConfigFunctionSpecs.update_forward_refs()  # type: ignore
    ConfigRegexMatchNodeConfig.update_forward_refs()  # type: ignore
    ConfigSqlExecutorNodeConfig.update_forward_refs()  # type: ignore
    ConfigStaticNodeConfig.update_forward_refs()  # type: ignore
    ConfigLlmEngineNodeConfig.update_forward_refs()  # type: ignore
    ConfigLlmEngineNodeConfigBatchSysKwargs.update_forward_refs()  # type: ignore
