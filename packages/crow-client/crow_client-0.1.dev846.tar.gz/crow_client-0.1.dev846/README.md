# crow-client

A client for interacting with endpoints of the FutureHouse crow service.

## Installation

```bash
uv pip install crow-client
```

## Usage

The CrowClient provides simple functions to deploy and monitor your crow.

```python
from pathlib import Path
from crow_client import CrowJob

client = CrowClient()

client.create_crow(
    path=Path("../envs/dummy_env"),
    environment="dummy_env.env.DummyEnv",
    requires_aviary_internal=False,
    environment_variables={"SAMPLE_ENV_VAR": "sample_val"},
    agent="ldp.agent.SimpleAgent",
)

# checks the status
client.get_build_status()
```

This client also provides functions that let you send tasks to an existing crow:

```python
from crow_client import CrowJob

client = CrowClient()

job_data = {"name": "your-job-name", "query": "your task"}
client.create_job(job_data)

# checks the status
client.get_job()
```

The CrowJobClient provides an interface for managing environment states and agent interactions in the FutureHouse crow service.

```python
from crow_client import CrowJobClient
from crow_client.models.app import Stage

client = CrowJobClient(
    environment="your_environment_name",
    agent="your_agent_id",
    auth_token="your_auth_token",
    base_uri=Stage.DEV,
    trajectory_id=None
)
```
