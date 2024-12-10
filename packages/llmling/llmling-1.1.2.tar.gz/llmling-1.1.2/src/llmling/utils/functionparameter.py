"""Generic parameter handling for function signatures."""

from __future__ import annotations

from collections.abc import Callable
import inspect
from typing import Any

from docstring_parser import parse as parse_docstring
from pydantic import BaseModel, ConfigDict, Field, ImportString

from llmling.core.log import get_logger


logger = get_logger(__name__)


class FunctionParameter(BaseModel):
    """Generic descriptor for function/method parameters."""

    name: str
    """Name of the parameter."""

    description: str | None = None
    """Human-readable description of what the parameter does."""

    required: bool = False
    """Whether this parameter must be provided."""

    type_hint: Any = str
    """Type annotation for the parameter."""

    default: Any | None = None
    """Default value if parameter is optional."""

    completion_function: ImportString | None = None
    """Optional function to provide parameter completions."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_attribute_docstrings=True,
    )

    @classmethod
    def from_parameter(
        cls,
        param: inspect.Parameter,
        description: str | None = None,
    ) -> FunctionParameter:
        """Create from inspect.Parameter.

        Args:
            param: Parameter to convert
            description: Optional description from docstring

        Returns:
            New FunctionParameter instance
        """
        return cls(
            name=param.name,
            description=description,
            required=param.default is inspect.Parameter.empty,
            type_hint=param.annotation
            if param.annotation != inspect.Parameter.empty
            else Any,
            default=None if param.default is inspect.Parameter.empty else param.default,
        )

    @classmethod
    def from_callable(
        cls,
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
            >>> params = FunctionParameter.from_callable(my_func)
        """
        skip_params = skip_params or set()
        sig = inspect.signature(func)
        doc = parse_docstring(func.__doc__ or "")
        param_docs = {
            p.arg_name: p.description
            for p in doc.params
            if p.arg_name and p.description
        }

        return [
            cls.from_parameter(
                param,
                description=param_docs.get(name),
            )
            for name, param in sig.parameters.items()
            if name not in skip_params
            and param.kind
            not in {param.VAR_POSITIONAL, param.VAR_KEYWORD}
        ]

    def to_field_info(self) -> tuple[type, Field]:
        """Convert to Pydantic field information.

        Returns:
            Tuple of (type, Field) for use with Pydantic models

        Example:
            >>> param = FunctionParameter(name="limit", type_hint=int, default=10)
            >>> type_, field = param.to_field_info()
            >>> Model = create_model('DynamicModel', limit=(type_, field))
        """
        return (
            self.type_hint,
            Field(
                default=self.default if not self.required else ...,
                description=self.description,
            )
        )


class PromptParameter(FunctionParameter):
    """Alias for FunctionParameter for backward compatibility.

    @deprecated: Use FunctionParameter instead
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize with deprecation warning."""
        import warnings
        warnings.warn(
            "PromptParameter is deprecated, use FunctionParameter instead",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


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

    params = FunctionParameter.from_callable(example_func)
    for param in params:
        print(f"{param.name}: {param.description} (required={param.required})")
