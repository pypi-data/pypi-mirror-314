from importlib.metadata import version

from .compose_app import AppFactory, compose_app
from .config import Config
from .connector import Connector
from .logging import create_logger

__version__ = version("unitelabs_cdk")
__all__ = ["__version__", "Connector", "Config", "create_logger", "compose_app", "AppFactory"]
