# Health

Types:

```python
from sgp_agents.types import HealthRetrieveResponse
```

Methods:

- <code title="get /health">client.health.<a href="./src/sgp_agents/resources/health.py">retrieve</a>() -> <a href="./src/sgp_agents/types/health_retrieve_response.py">object</a></code>

# Healthz

Types:

```python
from sgp_agents.types import HealthzRetrieveResponse
```

Methods:

- <code title="get /healthz">client.healthz.<a href="./src/sgp_agents/resources/healthz.py">retrieve</a>() -> <a href="./src/sgp_agents/types/healthz_retrieve_response.py">object</a></code>

# Configs

Types:

```python
from sgp_agents.types import (
    CompoundConditionInput,
    CompoundConditionOutput,
    JinjaNodeTemplate,
    NodeItemInput,
    NodeItemOutput,
    PlanConfigInput,
    PlanConfigOutput,
    UnaryCondition,
    WorkflowConfigInput,
    WorkflowConfigOutput,
    WorkflowItem,
    ConfigCreateResponse,
    ConfigRetrieveResponse,
    ConfigListResponse,
    ConfigDeleteResponse,
    ConfigExecuteResponse,
)
```

Methods:

- <code title="post /v1/configs/create">client.configs.<a href="./src/sgp_agents/resources/configs.py">create</a>(\*\*<a href="src/sgp_agents/types/config_create_params.py">params</a>) -> <a href="./src/sgp_agents/types/config_create_response.py">ConfigCreateResponse</a></code>
- <code title="get /v1/configs/{config_id}">client.configs.<a href="./src/sgp_agents/resources/configs.py">retrieve</a>(config_id) -> <a href="./src/sgp_agents/types/config_retrieve_response.py">ConfigRetrieveResponse</a></code>
- <code title="post /v1/configs/list">client.configs.<a href="./src/sgp_agents/resources/configs.py">list</a>(\*\*<a href="src/sgp_agents/types/config_list_params.py">params</a>) -> <a href="./src/sgp_agents/types/config_list_response.py">ConfigListResponse</a></code>
- <code title="delete /v1/configs/{config_id}">client.configs.<a href="./src/sgp_agents/resources/configs.py">delete</a>(config_id) -> <a href="./src/sgp_agents/types/config_delete_response.py">ConfigDeleteResponse</a></code>
- <code title="post /v1/configs/execute/{config_id}">client.configs.<a href="./src/sgp_agents/resources/configs.py">execute</a>(config_id, \*\*<a href="src/sgp_agents/types/config_execute_params.py">params</a>) -> <a href="./src/sgp_agents/types/config_execute_response.py">object</a></code>
