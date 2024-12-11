import os

from .base import PythonResolver


def get_resolver(config):
    if os.environ.get("NRP_USE_PDM"):
        from .pdm import PDMResolver
        return PDMResolver(config)
    else:
        from .uv import UVResolver
        return UVResolver(config)


__all__ = (
    "PythonResolver",
    "get_resolver",
)
