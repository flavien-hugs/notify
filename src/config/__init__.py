from .handlers import shutdown_handler, startup_handler  # noqa: F401
from .settings import get_settings

settings = get_settings()

__all__ = [settings]
