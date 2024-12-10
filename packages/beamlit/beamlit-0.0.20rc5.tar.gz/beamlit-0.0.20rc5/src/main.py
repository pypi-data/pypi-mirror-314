from typing import List

from beamlit.api.models import get_model_deployment
from beamlit.authentication import (get_authentication_headers,
                                    new_client_from_settings)
from beamlit.common.settings import init, init_agent
from beamlit.models.model import Model
from beamlit.models.model_deployment import ModelDeployment
from beamlit.run import RunClient

settings = init()
client = new_client_from_settings(settings)
model_deployment: ModelDeployment = get_model_deployment.sync("all-minilm-l6-v2", "production", client=client)
init_agent(client=client)
run_client = RunClient(client=client)
response = run_client.run(
    "function",
    "math",
    settings.environment,
    method="POST",
    json={"query": "4+4"}
)
print(response.json())
print(get_authentication_headers(settings))