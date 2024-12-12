try:
    from typing import Self, Callable
except Exception:
    from typing_extensions import Self, Callable


def _get_import_error(name: str, submodule: str) -> str:
    return (f"{name} is not included in the base install of eo4eu-comm-utils. " +
            f"Please import using eo4eu-comm-utils[{submodule}] or eo4eu-comm-utils[full]")
