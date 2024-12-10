from dataclasses import dataclass
from typing import Dict, Generator

from beamlit.common.settings import Settings
from httpx import Auth, Request, Response

from ..client import AuthenticatedClient
from .apikey import ApiKeyProvider
from .clientcredentials import ClientCredentials
from .credentials import Credentials, load_credentials_from_settings
from .device_mode import BearerToken


class PublicProvider(Auth):
    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        yield request



@dataclass
class RunClientWithCredentials:
    credentials: Credentials
    workspace: str
    api_url: str = "https://api.beamlit.dev/v0"
    run_url: str = "https://run.beamlit.dev/v0"


def new_client_from_settings(settings: Settings):
    credentials = load_credentials_from_settings(settings)

    client_config = RunClientWithCredentials(
        credentials=credentials,
        workspace=settings.workspace,
    )
    return new_client_with_credentials(client_config)

def new_client_with_credentials(config: RunClientWithCredentials):
    provider: Auth = None
    if config.credentials.api_key:
        provider = ApiKeyProvider(config.credentials, config.workspace)
    elif config.credentials.access_token:
        provider = BearerToken(config.credentials, config.workspace, config.api_url)
    elif config.credentials.client_credentials:
        provider = ClientCredentials(config.credentials, config.workspace, config.api_url)
    else:
        provider = PublicProvider()

    return AuthenticatedClient(base_url=config.api_url, provider=provider)

def get_authentication_headers(settings: Settings) -> Dict[str, str]:
    credentials = load_credentials_from_settings(settings)
    config = RunClientWithCredentials(
        credentials=credentials,
        workspace=settings.workspace,
    )
    provider = None
    if config.credentials.api_key:
        provider = ApiKeyProvider(config.credentials, config.workspace)
    elif config.credentials.access_token:
        provider = BearerToken(config.credentials, config.workspace, config.api_url)
    elif config.credentials.client_credentials:
        provider = ClientCredentials(config.credentials, config.workspace, config.api_url)

    if provider is None:
        return None

    return provider.get_headers()
