from typing import List

from beamlit.api.models import list_models
from beamlit.authentication import (RunClientWithCredentials,
                                    load_credentials_from_settings,
                                    new_client_with_credentials)
from beamlit.common.settings import init, init_agent
from beamlit.models.model import Model
from beamlit.run import RunClient

settings = init()
credentials = load_credentials_from_settings(settings)

client_config = RunClientWithCredentials(
    credentials=credentials,
    workspace=settings.workspace,
)
client = new_client_with_credentials(client_config)
init_agent(client=client)
models: List[Model] = list_models.sync(client=client)
print(settings.agent_model)

run_client = RunClient(client=client)
response = run_client.run(
    "function",
    "math",
    settings.environment,
    method="POST",
    json={"query": "4+4"}
)

print(response.json())