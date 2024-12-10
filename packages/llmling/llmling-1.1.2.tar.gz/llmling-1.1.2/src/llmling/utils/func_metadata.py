"""Function signature analysis and parameter extraction utilities."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

from docstring_parser import parse as parse_docstring
from pydantic import Field

from llmling.core.log import get_logger
from llmling.core.parameters import FunctionParameter


if TYPE_CHECKING:
    from collections.abc import Callable

    from pydantic.fields import FieldInfo


logger = get_logger(__name__)


def parameter_from_signature(
    param: inspect.Parameter,
    description: str | None = None,
) -> FunctionParameter:
    """Create FunctionParameter from inspect.Parameter.

    Args:
        param: Parameter to convert
        description: Optional description from docstring

    Returns:
        New FunctionParameter instance
    """
    return FunctionParameter(
        name=param.name,
        description=description,
        required=param.default is inspect.Parameter.empty,
        type_hint=param.annotation
        if param.annotation != inspect.Parameter.empty
        else Any,
        default=None if param.default is inspect.Parameter.empty else param.default,
    )


def extract_parameters(
    func: Callable[..., Any],
    skip_params: set[str] | None = None,
) -> list[FunctionParameter]:
    """Extract parameters from a callable.

    Analyzes function signature and docstring to create parameter descriptors.
    Handles type hints, default values, and parameter descriptions.

    Args:
        func: Function to analyze
        skip_params: Parameter names to skip

    Returns:
        List of FunctionParameter instances

    Example:
        >>> def my_func(x: int, data: list[str] = None) -> str:
        ...     '''Do something.
        ...     Args:
        ...         x: Some number
        ...         data: List of strings
        ...     '''
        ...     ...
        >>> params = extract_parameters(my_func)
    """
    skip_params = skip_params or set()
    sig = inspect.signature(func)
    doc = parse_docstring(func.__doc__ or "")
    param_docs = {
        p.arg_name: p.description for p in doc.params if p.arg_name and p.description
    }

    return [
        parameter_from_signature(
            param,
            description=param_docs.get(name),
        )
        for name, param in sig.parameters.items()
        if name not in skip_params
        and param.kind not in {param.VAR_POSITIONAL, param.VAR_KEYWORD}
    ]


def to_field_info(param: FunctionParameter) -> tuple[type, FieldInfo]:
    """Convert FunctionParameter to Pydantic field information.

    Args:
        param: Parameter to convert

    Returns:
        Tuple of (type, Field) for use with Pydantic models

    Example:
        >>> param = FunctionParameter(name="limit", type_hint=int, default=10)
        >>> type_, field = to_field_info(param)
        >>> Model = create_model('DynamicModel', limit=(type_, field))
    """
    return (
        param.type_hint,
        Field(
            default=param.default if not param.required else ...,
            description=param.description,
        ),
    )


if __name__ == "__main__":
    # Example usage
    def example_func(
        x: int,
        data: list[str],
        limit: int = 10,
    ) -> str:
        """Do something with the input.

        Args:
            x: Some number to process
            data: List of strings to analyze
            limit: Maximum items to process
        """

    params = extract_parameters(example_func)
    for param in params:
        print(f"{param.name}: {param.description} (required={param.required})")
