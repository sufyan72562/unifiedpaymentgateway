from logging.config import dictConfig
from typing import Optional


def init_logging(debug: bool = False, env: Optional[str] = None) -> None:
    level = "DEBUG" if debug else "INFO"

    # Basic structured-ish console logging suitable for most apps and containers
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)s %(name)s: %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": level,
                }
            },
            "root": {"handlers": ["console"], "level": level},
        }
    )
