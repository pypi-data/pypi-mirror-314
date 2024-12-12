import os


class Secret:
    @staticmethod
    def get(name: str):
        return os.getenv(name, os.getenv(f"bl_{name}"))

    @staticmethod
    def set(name: str, value: str):
        os.environ[name] = value
