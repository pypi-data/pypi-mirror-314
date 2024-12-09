import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.NOTSET,
    format="%(message)s",
    handlers=[RichHandler()],
)

# Qimchi Logger
logger = logging.getLogger(__name__)
