from beamlit.common.secrets import Secret

from . import kit


def github(name: str, *args):
    """This function kit is used to perform actions on Github."""
    github_token = Secret.get("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("github_token missing from configuration.")

    modes = {}

    for func_name in dir(kit):
        if not func_name.startswith("_"):
            modes[func_name] = getattr(kit, func_name)
    if name not in modes:
        msg = f"Invalid mode: {name}"
        raise ValueError(msg)
    return modes[name](*args)
    return modes[name](*args)
