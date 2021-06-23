from logging import getLogger, basicConfig, INFO

logger = getLogger("microservice logger")
basicConfig(
    filename="microservice.log",
    filemode="a",
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=INFO,
)