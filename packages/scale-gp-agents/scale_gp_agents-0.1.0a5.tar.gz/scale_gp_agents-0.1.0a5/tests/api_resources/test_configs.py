# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sgp_agents import Agents, AsyncAgents
from tests.utils import assert_matches_type
from sgp_agents.types import (
    ConfigListResponse,
    ConfigCreateResponse,
    ConfigDeleteResponse,
    ConfigRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestConfigs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Agents) -> None:
        config = client.configs.create(
            config={"plan": [{"workflow_name": "workflow_name"}]},
        )
        assert_matches_type(ConfigCreateResponse, config, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Agents) -> None:
        config = client.configs.create(
            config={
                "plan": [
                    {
                        "workflow_name": "workflow_name",
                        "workflow_alias": "workflow_alias",
                        "workflow_inputs": {"foo": "string"},
                    }
                ],
                "id": "id",
                "account_id": "account_id",
                "application_variant_id": "application_variant_id",
                "base_url": "base_url",
                "concurrency_default": True,
                "datasets": [{}],
                "egp_api_key_override": "egp_api_key_override",
                "egp_ui_evaluation": {},
                "evaluations": [
                    {
                        "config": {
                            "node_metadata": ["string"],
                            "num_workers": 0,
                            "type_hints": {},
                        },
                        "name": "name",
                        "type": "type",
                        "inputs": {"foo": "string"},
                    }
                ],
                "final_output_nodes": ["string"],
                "nodes_to_log": "string",
                "num_workers": 0,
                "streaming_nodes": ["string"],
                "subtype": "chat",
                "type": "workflow",
                "user_input": {},
                "workflows": {
                    "foo": {
                        "name": "name",
                        "nodes": [
                            {
                                "config": {
                                    "node_metadata": ["string"],
                                    "num_workers": 0,
                                    "type_hints": {},
                                },
                                "name": "name",
                                "type": "type",
                                "inputs": {"foo": "string"},
                            }
                        ],
                    }
                },
            },
        )
        assert_matches_type(ConfigCreateResponse, config, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Agents) -> None:
        response = client.configs.with_raw_response.create(
            config={"plan": [{"workflow_name": "workflow_name"}]},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        config = response.parse()
        assert_matches_type(ConfigCreateResponse, config, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Agents) -> None:
        with client.configs.with_streaming_response.create(
            config={"plan": [{"workflow_name": "workflow_name"}]},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            config = response.parse()
            assert_matches_type(ConfigCreateResponse, config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Agents) -> None:
        config = client.configs.retrieve(
            "config_id",
        )
        assert_matches_type(ConfigRetrieveResponse, config, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Agents) -> None:
        response = client.configs.with_raw_response.retrieve(
            "config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        config = response.parse()
        assert_matches_type(ConfigRetrieveResponse, config, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Agents) -> None:
        with client.configs.with_streaming_response.retrieve(
            "config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            config = response.parse()
            assert_matches_type(ConfigRetrieveResponse, config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Agents) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `config_id` but received ''"):
            client.configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Agents) -> None:
        config = client.configs.list(
            config_type="workflow",
        )
        assert_matches_type(ConfigListResponse, config, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Agents) -> None:
        config = client.configs.list(
            config_type="workflow",
            account_id="account_id",
        )
        assert_matches_type(ConfigListResponse, config, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Agents) -> None:
        response = client.configs.with_raw_response.list(
            config_type="workflow",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        config = response.parse()
        assert_matches_type(ConfigListResponse, config, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Agents) -> None:
        with client.configs.with_streaming_response.list(
            config_type="workflow",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            config = response.parse()
            assert_matches_type(ConfigListResponse, config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Agents) -> None:
        config = client.configs.delete(
            "config_id",
        )
        assert_matches_type(ConfigDeleteResponse, config, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Agents) -> None:
        response = client.configs.with_raw_response.delete(
            "config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        config = response.parse()
        assert_matches_type(ConfigDeleteResponse, config, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Agents) -> None:
        with client.configs.with_streaming_response.delete(
            "config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            config = response.parse()
            assert_matches_type(ConfigDeleteResponse, config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Agents) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `config_id` but received ''"):
            client.configs.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_execute(self, client: Agents) -> None:
        config = client.configs.execute(
            config_id="config_id",
            session_id="session_id",
        )
        assert_matches_type(object, config, path=["response"])

    @parametrize
    def test_method_execute_with_all_params(self, client: Agents) -> None:
        config = client.configs.execute(
            config_id="config_id",
            session_id="session_id",
            id="id",
            concurrent=True,
            messages=[
                {
                    "content": "content",
                    "role": "assistant",
                    "retrieved_context": [
                        {
                            "id": "id",
                            "content": "content",
                            "type": "context_chunk",
                            "context_document": {
                                "document_id": "document_id",
                                "attachment_url": "attachment_url",
                                "description": "description",
                                "metadata": {},
                                "title": "title",
                            },
                            "page_number": "page_number",
                            "score": 0,
                            "source_url": "source_url",
                        }
                    ],
                    "uuid": "UUID",
                }
            ],
            metadata={},
            return_span=True,
            run_id="run_id",
            stream=True,
        )
        assert_matches_type(object, config, path=["response"])

    @parametrize
    def test_raw_response_execute(self, client: Agents) -> None:
        response = client.configs.with_raw_response.execute(
            config_id="config_id",
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        config = response.parse()
        assert_matches_type(object, config, path=["response"])

    @parametrize
    def test_streaming_response_execute(self, client: Agents) -> None:
        with client.configs.with_streaming_response.execute(
            config_id="config_id",
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            config = response.parse()
            assert_matches_type(object, config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute(self, client: Agents) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `config_id` but received ''"):
            client.configs.with_raw_response.execute(
                config_id="",
                session_id="session_id",
            )


class TestAsyncConfigs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncAgents) -> None:
        config = await async_client.configs.create(
            config={"plan": [{"workflow_name": "workflow_name"}]},
        )
        assert_matches_type(ConfigCreateResponse, config, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAgents) -> None:
        config = await async_client.configs.create(
            config={
                "plan": [
                    {
                        "workflow_name": "workflow_name",
                        "workflow_alias": "workflow_alias",
                        "workflow_inputs": {"foo": "string"},
                    }
                ],
                "id": "id",
                "account_id": "account_id",
                "application_variant_id": "application_variant_id",
                "base_url": "base_url",
                "concurrency_default": True,
                "datasets": [{}],
                "egp_api_key_override": "egp_api_key_override",
                "egp_ui_evaluation": {},
                "evaluations": [
                    {
                        "config": {
                            "node_metadata": ["string"],
                            "num_workers": 0,
                            "type_hints": {},
                        },
                        "name": "name",
                        "type": "type",
                        "inputs": {"foo": "string"},
                    }
                ],
                "final_output_nodes": ["string"],
                "nodes_to_log": "string",
                "num_workers": 0,
                "streaming_nodes": ["string"],
                "subtype": "chat",
                "type": "workflow",
                "user_input": {},
                "workflows": {
                    "foo": {
                        "name": "name",
                        "nodes": [
                            {
                                "config": {
                                    "node_metadata": ["string"],
                                    "num_workers": 0,
                                    "type_hints": {},
                                },
                                "name": "name",
                                "type": "type",
                                "inputs": {"foo": "string"},
                            }
                        ],
                    }
                },
            },
        )
        assert_matches_type(ConfigCreateResponse, config, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAgents) -> None:
        response = await async_client.configs.with_raw_response.create(
            config={"plan": [{"workflow_name": "workflow_name"}]},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        config = await response.parse()
        assert_matches_type(ConfigCreateResponse, config, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAgents) -> None:
        async with async_client.configs.with_streaming_response.create(
            config={"plan": [{"workflow_name": "workflow_name"}]},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            config = await response.parse()
            assert_matches_type(ConfigCreateResponse, config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAgents) -> None:
        config = await async_client.configs.retrieve(
            "config_id",
        )
        assert_matches_type(ConfigRetrieveResponse, config, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAgents) -> None:
        response = await async_client.configs.with_raw_response.retrieve(
            "config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        config = await response.parse()
        assert_matches_type(ConfigRetrieveResponse, config, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAgents) -> None:
        async with async_client.configs.with_streaming_response.retrieve(
            "config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            config = await response.parse()
            assert_matches_type(ConfigRetrieveResponse, config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAgents) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `config_id` but received ''"):
            await async_client.configs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAgents) -> None:
        config = await async_client.configs.list(
            config_type="workflow",
        )
        assert_matches_type(ConfigListResponse, config, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAgents) -> None:
        config = await async_client.configs.list(
            config_type="workflow",
            account_id="account_id",
        )
        assert_matches_type(ConfigListResponse, config, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAgents) -> None:
        response = await async_client.configs.with_raw_response.list(
            config_type="workflow",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        config = await response.parse()
        assert_matches_type(ConfigListResponse, config, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAgents) -> None:
        async with async_client.configs.with_streaming_response.list(
            config_type="workflow",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            config = await response.parse()
            assert_matches_type(ConfigListResponse, config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAgents) -> None:
        config = await async_client.configs.delete(
            "config_id",
        )
        assert_matches_type(ConfigDeleteResponse, config, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAgents) -> None:
        response = await async_client.configs.with_raw_response.delete(
            "config_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        config = await response.parse()
        assert_matches_type(ConfigDeleteResponse, config, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAgents) -> None:
        async with async_client.configs.with_streaming_response.delete(
            "config_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            config = await response.parse()
            assert_matches_type(ConfigDeleteResponse, config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAgents) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `config_id` but received ''"):
            await async_client.configs.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_execute(self, async_client: AsyncAgents) -> None:
        config = await async_client.configs.execute(
            config_id="config_id",
            session_id="session_id",
        )
        assert_matches_type(object, config, path=["response"])

    @parametrize
    async def test_method_execute_with_all_params(self, async_client: AsyncAgents) -> None:
        config = await async_client.configs.execute(
            config_id="config_id",
            session_id="session_id",
            id="id",
            concurrent=True,
            messages=[
                {
                    "content": "content",
                    "role": "assistant",
                    "retrieved_context": [
                        {
                            "id": "id",
                            "content": "content",
                            "type": "context_chunk",
                            "context_document": {
                                "document_id": "document_id",
                                "attachment_url": "attachment_url",
                                "description": "description",
                                "metadata": {},
                                "title": "title",
                            },
                            "page_number": "page_number",
                            "score": 0,
                            "source_url": "source_url",
                        }
                    ],
                    "uuid": "UUID",
                }
            ],
            metadata={},
            return_span=True,
            run_id="run_id",
            stream=True,
        )
        assert_matches_type(object, config, path=["response"])

    @parametrize
    async def test_raw_response_execute(self, async_client: AsyncAgents) -> None:
        response = await async_client.configs.with_raw_response.execute(
            config_id="config_id",
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        config = await response.parse()
        assert_matches_type(object, config, path=["response"])

    @parametrize
    async def test_streaming_response_execute(self, async_client: AsyncAgents) -> None:
        async with async_client.configs.with_streaming_response.execute(
            config_id="config_id",
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            config = await response.parse()
            assert_matches_type(object, config, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute(self, async_client: AsyncAgents) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `config_id` but received ''"):
            await async_client.configs.with_raw_response.execute(
                config_id="",
                session_id="session_id",
            )
