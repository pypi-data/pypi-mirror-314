"""Decorators for creating function tools with Beamlit and LangChain integration."""

from collections.abc import Callable
from logging import getLogger

from langchain_core.tools import create_schema_from_function, tool

from beamlit.authentication import new_client
from beamlit.common.settings import get_settings
from beamlit.models import FunctionDeployment, FunctionKit
from beamlit.run import RunClient

logger = getLogger(__name__)


def get_remote_function(func: Callable, bl_function: FunctionDeployment):
    settings = get_settings()

    def _partial(*args, **kwargs):
        # Get function signature parameters
        try:
            client = new_client()
            run_client = RunClient(client)
            name = (bl_function and bl_function.function) or func.__name__
            logger.debug(
                f"Calling remote function: NAME={name}"
                f" PARAMS={kwargs} ENVIRONMENT={settings.environment}"
            )
            response = run_client.run(
                resource_type="function",
                resource_name=name,
                environment=settings.environment,
                method="POST",
                headers={},
                json=kwargs,
            )
            if response.status_code >= 400:
                content = f"{response.status_code}:{response.text}"
                return f"Error calling remote function: {content}"
            logger.debug(
                f"Response from remote function: NAME={name}"
                f" RESPONSE={response.json()} ENVIRONMENT={settings.environment}"
            )
            return response.json()
        except Exception as e:
            logger.error(f"Error calling function {bl_function.id}: {e}")
            raise e

    remote_func = _partial
    remote_func.__name__ = func.__name__
    remote_func.__doc__ = func.__doc__
    return remote_func


def kit(bl_kit: FunctionKit = None, **kwargs: dict) -> Callable:
    """Create function tools with Beamlit and LangChain integration."""

    def wrapper(func: Callable) -> Callable:
        if bl_kit and not func.__doc__ and bl_kit.description:
            func.__doc__ = bl_kit.description
        return tool(func, **kwargs)

    return wrapper


def function(
    *args, bl_function: FunctionDeployment = None, kit=False, **kwargs: dict
) -> Callable:
    """Create function tools with Beamlit and LangChain integration."""
    settings = get_settings()

    def wrapper(func: Callable) -> Callable:
        if bl_function and not func.__doc__ and bl_function.description:
            func.__doc__ = bl_function.description
        if (
            settings.environment == "development"
            or settings.environment == "production"
        ):
            remote_func = get_remote_function(func, bl_function)
            if not kwargs.get("args_schema"):
                kwargs["args_schema"] = create_schema_from_function(
                    func.__name__,
                    func,
                    parse_docstring=func.__doc__,
                )
            return tool(remote_func, **kwargs)
        return tool(func, **kwargs)

    return wrapper
    return wrapper
