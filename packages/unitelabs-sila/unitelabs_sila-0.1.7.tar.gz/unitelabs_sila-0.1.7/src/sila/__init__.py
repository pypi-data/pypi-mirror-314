import logging
from importlib.metadata import version

logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = version("unitelabs_sila")
__all__ = ["__version__"]
