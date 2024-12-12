import os
from logging import getLogger
from typing import List, Tuple, Type, Union

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.graph import CompiledGraph
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from beamlit.api.functions import get_function_deployment
from beamlit.api.models import get_model_deployment
from beamlit.client import AuthenticatedClient
from beamlit.common.logger import init as init_logger
from beamlit.models.agent_deployment import AgentDeployment
from beamlit.models.function_deployment import FunctionDeployment
from beamlit.models.model_deployment import ModelDeployment
from beamlit.types import UNSET, Unset

global SETTINGS
SETTINGS = None


def get_settings():
    return SETTINGS


class SettingsAgent(BaseSettings):
    agent: Union[None, CompiledGraph, BaseChatModel] = None
    chain: Union[Unset, List[AgentDeployment]] = UNSET
    model: Union[Unset, ModelDeployment] = UNSET
    functions: Union[Unset, List[FunctionDeployment]] = UNSET
    functions_directory: str = Field(default="src/functions")
    chat_model: Union[None, BaseChatModel] = None
    module: str = Field(default="main.main")


class SettingsAuthentication(BaseSettings):
    api_key: Union[None, str] = None
    jwt: Union[None, str] = None
    client_credentials: Union[None, str] = None


class SettingsServer(BaseSettings):
    module: str = Field(default="main.main")
    port: int = Field(default=80)
    host: str = Field(default="0.0.0.0")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file="beamlit.yaml",
        env_prefix="bl_",
        env_nested_delimiter="_",
    )

    workspace: str
    environment: str
    type: str = Field(default="agent")
    name: str = Field(default="beamlit-agent")
    base_url: str = Field(default="https://api.beamlit.dev/v0")
    run_url: str = Field(default="https://run.beamlit.dev")
    log_level: str = Field(default="INFO")
    agent: SettingsAgent = SettingsAgent()
    server: SettingsServer = SettingsServer()
    authentication: SettingsAuthentication = SettingsAuthentication()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
            init_settings,
        )


def init_agent(
    client: AuthenticatedClient,
    destination: str = f"{os.getcwd()}/src/beamlit_generated.py",
):
    from beamlit.api.agents import get_agent_deployment
    from beamlit.common.generate import generate

    logger = getLogger(__name__)
    settings = get_settings()
    # Init configuration from environment variables
    if settings.agent.functions or settings.agent.chain:
        return

    # Init configuration from beamlit control plane
    name = settings.name
    env = settings.environment

    agent_deployment = get_agent_deployment.sync(name, env, client=client)
    function_deployments = []
    agent_chain_deployments = []
    if agent_deployment.functions:
        for function in agent_deployment.functions:
            function_deployment = get_function_deployment.sync(function, env, client=client)
            function_deployments.append(function_deployment)
        settings.agent.functions = function_deployments

    if agent_deployment.agent_chain:
        for chain in agent_deployment.agent_chain:
            if chain.enabled:
                agent_deployment = get_agent_deployment.sync(chain.name, env, client=client)
                if chain.description:
                    agent_deployment.description = chain.description
                agent_chain_deployments.append(agent_deployment)
        settings.agent.chain = agent_chain_deployments
    if agent_deployment.model:
        model_deployment = get_model_deployment.sync(agent_deployment.model, env, client=client)
        settings.agent.model = model_deployment

    content_generate = generate(destination, dry_run=True)
    compared_content = None
    if os.path.exists(destination):
        compared_content = open(destination).read()

    if not os.path.exists(destination) or (
        compared_content and content_generate != compared_content
    ):
        logger.info("Generating agent code")
        generate(destination)


def init() -> Settings:
    """Parse the beamlit.yaml file to get configurations."""
    from beamlit.authentication.credentials import current_context

    global SETTINGS

    context = current_context()
    kwargs = {}
    if context.workspace:
        kwargs["workspace"] = context.workspace
    if context.environment:
        kwargs["environment"] = context.environment

    SETTINGS = Settings(**kwargs)
    init_logger(SETTINGS.log_level)

    return SETTINGS
