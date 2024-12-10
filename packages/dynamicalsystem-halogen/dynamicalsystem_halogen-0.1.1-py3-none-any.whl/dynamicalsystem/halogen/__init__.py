from dynamicalsystem.halogen.config import config_instance
from dynamicalsystem.halogen.logging import create_logger
from pprint import pprint

logger = create_logger()


def main() -> int:
    config = config_instance(__name__)
    print(f"Hello from {__name__}")
    logger.info(f"Hello from {__name__}")
    pprint(config.__dict__)
    return 0
