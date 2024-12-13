# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal

import httpx

from ..types import config_list_params, config_create_params, config_execute_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.config_list_response import ConfigListResponse
from ..types.config_create_response import ConfigCreateResponse
from ..types.config_delete_response import ConfigDeleteResponse
from ..types.config_retrieve_response import ConfigRetrieveResponse

__all__ = ["ConfigsResource", "AsyncConfigsResource"]


class ConfigsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/agents-python#accessing-raw-response-data-eg-headers
        """
        return ConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/agents-python#with_streaming_response
        """
        return ConfigsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        config: config_create_params.Config,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigCreateResponse:
        """Create Config

        Args:
          config: Representation of a plan, i.e.

        a composition of workflows and branch complexes

              Public attributes: workflows: maps a workflow "name" to either a workflow yaml
              file or an inline workflow definition plan: representation of the graph
              connecting workflows / branch complexes

              Private attributes: helper_workflows: a list of workflows created by default, in
              order to support loops and other control flow features

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/configs/create",
            body=maybe_transform({"config": config}, config_create_params.ConfigCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigCreateResponse,
        )

    def retrieve(
        self,
        config_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigRetrieveResponse:
        """
        Get Config By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not config_id:
            raise ValueError(f"Expected a non-empty value for `config_id` but received {config_id!r}")
        return self._get(
            f"/v1/configs/{config_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigRetrieveResponse,
        )

    def list(
        self,
        *,
        config_type: Literal["workflow", "plan", "state_machine"],
        account_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigListResponse:
        """
        List Configs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/configs/list",
            body=maybe_transform(
                {
                    "config_type": config_type,
                    "account_id": account_id,
                },
                config_list_params.ConfigListParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigListResponse,
        )

    def delete(
        self,
        config_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigDeleteResponse:
        """
        Delete Config By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not config_id:
            raise ValueError(f"Expected a non-empty value for `config_id` but received {config_id!r}")
        return self._delete(
            f"/v1/configs/{config_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigDeleteResponse,
        )

    def execute(
        self,
        config_id: str,
        *,
        session_id: str,
        id: str | NotGiven = NOT_GIVEN,
        concurrent: Optional[bool] | NotGiven = NOT_GIVEN,
        messages: Optional[Iterable[config_execute_params.Message]] | NotGiven = NOT_GIVEN,
        metadata: Optional[object] | NotGiven = NOT_GIVEN,
        return_span: Optional[bool] | NotGiven = NOT_GIVEN,
        run_id: Optional[str] | NotGiven = NOT_GIVEN,
        stream: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Execute Config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not config_id:
            raise ValueError(f"Expected a non-empty value for `config_id` but received {config_id!r}")
        return self._post(
            f"/v1/configs/execute/{config_id}",
            body=maybe_transform(
                {
                    "session_id": session_id,
                    "id": id,
                    "concurrent": concurrent,
                    "messages": messages,
                    "metadata": metadata,
                    "return_span": return_span,
                    "run_id": run_id,
                    "stream": stream,
                },
                config_execute_params.ConfigExecuteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncConfigsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/agents-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/agents-python#with_streaming_response
        """
        return AsyncConfigsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        config: config_create_params.Config,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigCreateResponse:
        """Create Config

        Args:
          config: Representation of a plan, i.e.

        a composition of workflows and branch complexes

              Public attributes: workflows: maps a workflow "name" to either a workflow yaml
              file or an inline workflow definition plan: representation of the graph
              connecting workflows / branch complexes

              Private attributes: helper_workflows: a list of workflows created by default, in
              order to support loops and other control flow features

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/configs/create",
            body=await async_maybe_transform({"config": config}, config_create_params.ConfigCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigCreateResponse,
        )

    async def retrieve(
        self,
        config_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigRetrieveResponse:
        """
        Get Config By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not config_id:
            raise ValueError(f"Expected a non-empty value for `config_id` but received {config_id!r}")
        return await self._get(
            f"/v1/configs/{config_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigRetrieveResponse,
        )

    async def list(
        self,
        *,
        config_type: Literal["workflow", "plan", "state_machine"],
        account_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigListResponse:
        """
        List Configs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/configs/list",
            body=await async_maybe_transform(
                {
                    "config_type": config_type,
                    "account_id": account_id,
                },
                config_list_params.ConfigListParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigListResponse,
        )

    async def delete(
        self,
        config_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigDeleteResponse:
        """
        Delete Config By Id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not config_id:
            raise ValueError(f"Expected a non-empty value for `config_id` but received {config_id!r}")
        return await self._delete(
            f"/v1/configs/{config_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigDeleteResponse,
        )

    async def execute(
        self,
        config_id: str,
        *,
        session_id: str,
        id: str | NotGiven = NOT_GIVEN,
        concurrent: Optional[bool] | NotGiven = NOT_GIVEN,
        messages: Optional[Iterable[config_execute_params.Message]] | NotGiven = NOT_GIVEN,
        metadata: Optional[object] | NotGiven = NOT_GIVEN,
        return_span: Optional[bool] | NotGiven = NOT_GIVEN,
        run_id: Optional[str] | NotGiven = NOT_GIVEN,
        stream: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Execute Config

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not config_id:
            raise ValueError(f"Expected a non-empty value for `config_id` but received {config_id!r}")
        return await self._post(
            f"/v1/configs/execute/{config_id}",
            body=await async_maybe_transform(
                {
                    "session_id": session_id,
                    "id": id,
                    "concurrent": concurrent,
                    "messages": messages,
                    "metadata": metadata,
                    "return_span": return_span,
                    "run_id": run_id,
                    "stream": stream,
                },
                config_execute_params.ConfigExecuteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ConfigsResourceWithRawResponse:
    def __init__(self, configs: ConfigsResource) -> None:
        self._configs = configs

        self.create = to_raw_response_wrapper(
            configs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            configs.retrieve,
        )
        self.list = to_raw_response_wrapper(
            configs.list,
        )
        self.delete = to_raw_response_wrapper(
            configs.delete,
        )
        self.execute = to_raw_response_wrapper(
            configs.execute,
        )


class AsyncConfigsResourceWithRawResponse:
    def __init__(self, configs: AsyncConfigsResource) -> None:
        self._configs = configs

        self.create = async_to_raw_response_wrapper(
            configs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            configs.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            configs.list,
        )
        self.delete = async_to_raw_response_wrapper(
            configs.delete,
        )
        self.execute = async_to_raw_response_wrapper(
            configs.execute,
        )


class ConfigsResourceWithStreamingResponse:
    def __init__(self, configs: ConfigsResource) -> None:
        self._configs = configs

        self.create = to_streamed_response_wrapper(
            configs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            configs.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            configs.list,
        )
        self.delete = to_streamed_response_wrapper(
            configs.delete,
        )
        self.execute = to_streamed_response_wrapper(
            configs.execute,
        )


class AsyncConfigsResourceWithStreamingResponse:
    def __init__(self, configs: AsyncConfigsResource) -> None:
        self._configs = configs

        self.create = async_to_streamed_response_wrapper(
            configs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            configs.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            configs.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            configs.delete,
        )
        self.execute = async_to_streamed_response_wrapper(
            configs.execute,
        )
