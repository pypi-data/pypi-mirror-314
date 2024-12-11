"""Init expressions."""

# Import all subclasses of expression
# pylint: disable=unused-import,wildcard-import
import typing as t

from .base import (
    ActionExpression,  # noqa: F401
    BinaryExpression,  # noqa: F401
    Expression,  # noqa: F401
    MatchExpression,  # noqa: F401
    UnaryExpression,  # noqa: F401
)
from .expression import *  # noqa: F403


def subclasses_with_key(cls: t.Type, key: str) -> t.Dict[str, t.Tuple[str, t.Type]]:
    """Recursively return all subclasses of a given class.

    Args:
        cls (Type): Base Class.
        key (str): Key to use for the dictionary.

    Returns:
        (t.Set[t.Type]): List of subclasses.
    """
    subcls: t.Dict[str, t.Tuple[str, t.Type]] = {}
    for sub in cls.__subclasses__():
        if getattr(sub, key, ""):
            if issubclass(sub, BinaryExpression):
                subcls[getattr(sub, key)] = ("binary", sub)
            elif issubclass(sub, UnaryExpression):
                subcls[getattr(sub, key)] = ("unary", sub)
            else:  # pragma: no cover
                raise RuntimeError("Unknown op_type for expression class {sub}")
        subcls.update(subclasses_with_key(sub, key))
    return subcls


expression_map = subclasses_with_key(Expression, "op")
