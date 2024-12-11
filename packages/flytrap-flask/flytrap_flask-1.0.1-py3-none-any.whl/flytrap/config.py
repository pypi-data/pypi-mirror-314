from .utils.exceptions import FlytrapError
from .handler.system_handler import setup_system_handler

_config = None


def init(config: dict, force: bool = False) -> None:
    """
    Initializes Flytrap with the provided configuration and sets up global error
    handlers.
    """
    global _config

    if _config and not force:
        raise FlytrapError("Flytrap has already been initialized.")

    _config = {**config, "include_context": config.get("include_context", True)}

    setup_system_handler()


def get_config() -> dict:
    """Retrieves the current Flytrap SDK configuration."""
    if not _config:
        raise FlytrapError("Flytrap is not initialized. Call init() first.")
    return _config
