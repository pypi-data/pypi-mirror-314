from .log import LogFormatter


def get_default_logging_config(verbosity: int = 0, level: str = "INFO"):
    args = {}
    level = level
    if verbosity == 1:
        args = {
            "add_name": False,
            "add_path": True,
            "before_message": "\n",
        }
    elif verbosity == 2:
        args = {
            "print_traceback": True,
        }
    elif verbosity == 3:
        args = {
            "print_traceback": True,
            "add_name": False,
            "add_path": True,
            "before_message": "\n",
        }

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "custom": {
                "()": LogFormatter,
                **args
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "custom",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": level,
        },
    }
