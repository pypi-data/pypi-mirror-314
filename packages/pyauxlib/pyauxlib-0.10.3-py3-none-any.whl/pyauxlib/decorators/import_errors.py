"""Decorators for handling imports."""

import importlib
import logging
from collections.abc import Callable
from typing import Any

import wrapt

logger = logging.getLogger(__name__)


def packages_required(package_names: list[str]) -> Any:
    """Check if specific packages are installed.

    Parameters
    ----------
    package_names : List[str]
        The names of the packages that the decorated function requires.

    Returns
    -------
    Callable[..., Any]
        The decorated function, which will raise an ImportError if the required packages are not
        installed.
    """

    @wrapt.decorator
    def wrapper(
        wrapped: Callable[..., Any],
        instance: Any | None,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        for package_name in package_names:
            if importlib.util.find_spec(package_name) is None:
                error_msg = f"The '{package_name}' package is required to use '{wrapped.__module__}.{wrapped.__name__}'."
                logger.warning(error_msg)
                raise ImportError(error_msg)
        return wrapped(*args, **kwargs)

    return wrapper
