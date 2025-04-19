import importlib
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


@lru_cache
def load_provider_class(dot_path: str):
    module_path, class_name = dot_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    provider_class = getattr(module, class_name)
    return provider_class


def select_provider(dotpath: str):
    provider_class = load_provider_class(dotpath)
    return provider_class()
