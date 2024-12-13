# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ConfigExecuteParams", "Message", "MessageRetrievedContext", "MessageRetrievedContextContextDocument"]


class ConfigExecuteParams(TypedDict, total=False):
    session_id: Required[str]

    id: str

    concurrent: Optional[bool]

    messages: Optional[Iterable[Message]]

    metadata: Optional[object]

    return_span: Optional[bool]

    run_id: Optional[str]

    stream: bool


class MessageRetrievedContextContextDocument(TypedDict, total=False):
    document_id: Required[str]

    attachment_url: Optional[str]

    description: Optional[str]

    metadata: Optional[object]

    title: Optional[str]


class MessageRetrievedContext(TypedDict, total=False):
    id: Required[str]

    content: Required[str]

    type: Required[Literal["context_chunk", "document", "sql", "external_url", "other"]]

    context_document: Optional[MessageRetrievedContextContextDocument]
    """Represents a document related to the chat context.

    Attributes: document_id (str): The unique identifier of the document. title
    (Optional[str]): The title of the document. description (Optional[str]): The
    description of the document. attachment_url (Optional[str]): The URL of the
    original document (e.g., PDF). metadata (Optional[dict]): Additional metadata
    for the document.
    """

    page_number: Optional[str]

    score: Optional[float]

    source_url: Optional[str]


class Message(TypedDict, total=False):
    content: Required[str]

    role: Required[Literal["assistant", "user", "system"]]

    retrieved_context: Optional[Iterable[MessageRetrievedContext]]

    uuid: Annotated[str, PropertyInfo(alias="UUID")]
