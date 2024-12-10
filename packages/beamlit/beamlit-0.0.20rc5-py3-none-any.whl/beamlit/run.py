import urllib.parse
from contextlib import contextmanager
from typing import Any, Callable, Dict, List, Optional

import requests
from beamlit.client import AuthenticatedClient
from beamlit.common.settings import get_settings


class RunClient:
    def __init__(self, client: AuthenticatedClient):
        self.client = client

    def run(
        self,
        resource_type: str,
        resource_name: str,
        environment: str,
        method: str,
        path: str = "",
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        settings = get_settings()
        headers = headers or {}
        params = params or {}

        # Build the path
        if path:
            path = f"{settings.workspace}/{resource_type}s/{resource_name}/{path}"
        else:
            path = f"{settings.workspace}/{resource_type}s/{resource_name}"

        client = self.client.get_httpx_client()
        url = urllib.parse.urljoin(settings.run_url, path)

        kwargs = {
            "headers": headers,
            "params": {"environment": environment, **params},
        }
        if data:
            kwargs["data"] = data
        if json:
            kwargs["json"] = json

        response = client.request(method, url, **kwargs)
        return response
