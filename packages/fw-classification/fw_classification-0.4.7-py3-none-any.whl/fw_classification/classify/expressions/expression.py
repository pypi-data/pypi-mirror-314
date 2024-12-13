"""Implementation of individual expression types."""

import logging
import operator
import re
import typing as t

from dotty_dict import Dotty  # type: ignore

from .base import (
    ActionExpression,
    Expression,
    MatchExpression,
    UnaryExpression,
)

log = logging.getLogger(__name__)

################ Unary Expressions ################


class And(UnaryExpression):
    """Require all sub-expressions to be True."""

    op = "and"

    def evaluate(self, i_dict: Dotty) -> bool:
        """Evaluate `and` expression."""
        res = True
        for expr in self.exprs:
            if not expr.evaluate(i_dict):
                res = False
                break
        return res

    def __repr__(self):
        """Implement `repr()`."""
        return "\n\t and ".join([repr(expr) for expr in self.exprs])


class Or(UnaryExpression):
    """Require at least one sub-expression to be True."""

    op = "or"

    def evaluate(self, i_dict: Dotty) -> bool:
        """Evaluate `or` expression."""
        res = False
        for expr in self.exprs:
            if expr.evaluate(i_dict):
                res = True
                break
        return res

    def __repr__(self):
        """Implement `repr()`."""
        return "\n\t or ".join([repr(expr) for expr in self.exprs])


class Not(UnaryExpression):
    """Require sub-expression to be False."""

    op = "not"

    def __init__(self, exprs: t.List[Expression]) -> None:
        """Initialize Not expression.

        Args:
            exprs (t.List[Expression]): List of expressions.
        """
        if len(exprs) > 1:
            raise ValueError(
                f"Not block can only have 1 child element, found {len(exprs)}",
                "Try grouping with And or Or",
            )
        super().__init__(exprs)

    def evaluate(self, i_dict: Dotty) -> bool:
        """Evaluate `not` expression."""
        return not self.exprs[0].evaluate(i_dict)

    def __repr__(self):
        """Implement `repr()`."""
        return "not (\n\t" + "\n\t".join([repr(expr) for expr in self.exprs]) + "\n)"


################ Binary Expressions ################


def is_numeric(val: t.Any) -> bool:
    """Helper to see if value is numeric.

    Args:
        val (Any): Value.

    Returns:
        bool: True if numeric, False otherwise
    """
    try:
        float(val)
    except (ValueError, TypeError):
        return False
    return True


class Contains(MatchExpression):
    """Returns True if `value` is in the `field`.

    Config Options:
    resolve (bool, default false) Resolves "value" as a key from i_dict
    """

    op = "contains"

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        if "resolve" in self.config and self.config["resolve"]:
            self._resolve_value(i_dict)
            if not self._value:
                log.debug("_resolve_value returns empty!")
        val = self.get_value(i_dict)

        return self.value in val

    def __repr__(self):
        """Implement `repr()`."""
        return f"{self.value} is in {self._field}"


class Is(MatchExpression):
    """Returns True if the `field`'s value equals `value`.

    Config Options:
        approximate (int, default 0): Allow approximate values to n decimals if
            n > 0
        resolve (bool, default false) Resolves "value" as a key from i_dict
    """

    op = "is"

    @staticmethod
    def validate(
        field: str,
        val: t.Any,
        variables: t.Optional[t.Dict[str, str]] = None,
        **kwargs,
    ) -> t.List[str]:
        """Validate regex config option(s)."""
        err = super(Is, Is).validate(field, val, variables, **kwargs)
        if "approximate" in kwargs:
            if not isinstance(kwargs["approximate"], int):
                err.append(
                    f"Is: approximate must be int, found '{kwargs['approximate']}'"
                )
            if "resolve" not in kwargs:
                if not is_numeric(val):
                    err.append(
                        f"Value must be numeric if using approximate, found '{val}'"
                    )
        return err

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        if "resolve" in self.config and self.config["resolve"]:
            self._resolve_value(i_dict)
            if not self._value:
                log.debug("_resolve_value returns empty!")
        val = self.get_value(i_dict)

        if "approximate" in self.config and self.config["approximate"]:
            dig = self.config["approximate"]
            return round(val, ndigits=dig) == round(self.value, ndigits=dig)
        return val == self.value

    def __repr__(self):
        """Implement `repr()`."""
        base = f"{self._field} is {self.value}"
        if "approximate" in self.config and self.config["approximate"]:
            base += f" when rounding to {self.config['approximate']} digits"
        return base


class In(MatchExpression):
    """Return True if `field`'s value is in the list `value`.

    Config Options:
    resolve (bool, default false) Resolves "value" as a key from i_dict
    """

    op = "in"

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        if "resolve" in self.config and self.config["resolve"]:
            self._resolve_value(i_dict)
            if not self._value:
                log.debug("_resolve_value returns empty!")
        val = self.get_value(i_dict)

        return val in self.value

    def __repr__(self):
        """Implement `repr()`."""
        return f"{self._field} is in {self.value}"


class Exists(MatchExpression):
    """Return True if `field` exists."""

    op = "exists"

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        return self.field in i_dict if self.value else self.field not in i_dict

    def __repr__(self):
        """Implement `repr()`."""
        return self._field + (" exists" if self.value else " doesn't exist")


class IsNumeric(MatchExpression):
    """Return True if `field` is numeric."""

    op = "is_numeric"

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        val = self.get_value(i_dict)
        return is_numeric(val) if self.value else not is_numeric(val)

    def __repr__(self):
        """Implement `repr()`."""
        return self._field + (" is numeric" if self.value else " isn't numeric")


class Regex(MatchExpression):
    """Return True if `field`'s value matches the regex `value`.

    Config Options:
        case_sensitive (bool, default False): Make the regex case-sensitive.
            Defaults to case insensitive.
    """

    op = "regex"

    @staticmethod
    def validate(
        field: str,
        val: t.Any,
        variables: t.Optional[t.Dict[str, str]] = None,
        **kwargs,
    ) -> t.List[str]:
        """Validate regex config option(s)."""
        err = super(Regex, Regex).validate(field, val, variables, **kwargs)
        if "case_sensitive" in kwargs and not isinstance(
            kwargs["case_sensitive"], bool
        ):
            err.append(
                "Regex case-sensitive must be boolean, found "
                f"'{kwargs['case_sensitive']}'"
            )
        return err

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        if "case_sensitive" in self.config and self.config["case_sensitive"]:
            regex = re.compile(self.value)
        else:
            regex = re.compile(self.value, re.IGNORECASE)
        val = self.get_value(i_dict)
        return bool(regex.search(val))

    def __repr__(self):
        """Implement `repr()`."""
        return f"{self._field} matches regex {self.value}"


class Startswith(MatchExpression):
    """Return True if `field` starts with `value`."""

    op = "startswith"

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        regex = re.compile(f"^{self.value}")
        val = self.get_value(i_dict)
        return bool(regex.match(val))

    def __repr__(self):
        """Implement `repr()`."""
        return f"{self._field} starts with {self.value}"


class NumericMatchExpression(MatchExpression):
    """Base class for numeric expressions."""

    func: t.Callable

    def __init__(
        self,
        field: str,
        val: t.Any,
        variables: t.Optional[t.Dict[str, str]] = None,
        **kwargs,
    ) -> None:
        """Init numeric expression."""
        super().__init__(field, val, variables, **kwargs)
        if not isinstance(val, str):
            self._value = float(val)

    @classmethod
    def validate(
        cls: t.Type["NumericMatchExpression"],
        field: str,
        val: t.Any,
        variables: t.Optional[t.Dict[str, str]] = None,
        **kwargs,
    ) -> t.List[str]:
        """Validate numeric expression."""
        err = super(NumericMatchExpression, NumericMatchExpression).validate(
            field, val, variables, **kwargs
        )
        if not is_numeric(val) and "resolve" not in kwargs:
            err.append(f"'{cls.op}' must be numeric value, found '{val}'")
        if "approximate" in kwargs:
            if not isinstance(kwargs["approximate"], int):
                err.append(
                    f"{cls.op}: approximate must be int, "
                    f"found '{kwargs['approximate']}'"
                )
        return err

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        if "resolve" in self.config and self.config["resolve"]:
            self._resolve_value(i_dict)
            if not self._value:
                log.debug("_resolve_value returns empty!")
        val = self.get_value(i_dict)

        if not is_numeric(val):
            log.warning(
                f"{self.op}: Found non-numeric input for field "
                f"'{self.field}': '{val}'"
            )
            return False
        try:
            res = self.func(float(val), float(self.value))
        except ValueError:
            log.warning(
                f"{self.op}: Cannot convert val: {val} or self.value {self.value} to float"
            )
            return False
        if not res and self.config.get("approximate"):
            dig = self.config["approximate"]
            return round(val, ndigits=dig) == round(self.value, ndigits=dig)
        return res


class LessThan(NumericMatchExpression):
    """Return True if `field`'s value is less than `value`.

    Config Options:
        approximate (int): Allows configuration for a less-than-or-equal
            operation.  If less-than fails, round to `approximate` digits
            and evaluate equality.

            e.g.
            - key: file.info.header.dicom.EchoTime
              less_than: 15.5
              approximate: 1

            this would match if the echo time was 15, but also would match
            if echo time was 15.54, since:
            round(15.54, ndigits=1) == round(15.5, ndigits=1)

        resolve (bool, default false) Resolves "value" as a key from i_dict
    """

    op = "less_than"
    func = operator.lt

    def __repr__(self):
        """Implement `repr()`."""
        base = f"{self._field} is less than {self.value}"
        if self.config.get("approximate"):
            base += " or equal when rounded to {self.config['approximate']} digits"
        return base


class GreaterThan(NumericMatchExpression):
    """Return True if `field`'s value is less than `value`.

    Config Options:
        approximate (int): Allows configuration for a greater-than-or-equal
            operation.  If greater-than fails, round to `approximate` digits
            and evaluate equality.

            e.g.
            - key: file.info.header.dicom.EchoTime
              greater_than: 15.5
              approximate: 1

            this would match if the echo time was 15.6, but also would match
            if echo time was 15.49, since:
            round(15.49, ndigits=1) == round(15.5, ndigits=1)

        resolve (bool, default false) Resolves "value" as a key from i_dict

    """

    op = "greater_than"
    func = operator.gt

    def __repr__(self):
        """Implement `repr()`."""
        base = f"{self._field} is greater than {self.value}"
        if self.config.get("approximate"):
            base += " or equal when rounded to {self.config['approximate']} digits"
        return base


################ Action Expressions ################


class Set(ActionExpression):
    """Set `field` to `value`."""

    op = "set"

    def apply(self, i_dict: Dotty) -> bool:
        """Evaluate action."""
        i_dict[self.field] = self.value
        return True

    def __repr__(self):
        """Implement `repr()`."""
        return f"set {self._field} to {self.value}"


class Add(ActionExpression):
    """Add `value` to `field`.

    Available config options:
        allow_duplicate (bool, default False): Allow add to duplicate an
            existing value. Defaults to False.
    """

    op = "add"

    @staticmethod
    def validate(
        field: str,
        val: t.Any,
        variables: t.Optional[t.Dict[str, str]] = None,
        **kwargs,
    ) -> t.List[str]:
        """Validate `allow_duplicate` for regex."""
        # err = super().validate(field, val, variables, **kwargs) returns a
        # mypy error: error: Argument 2 for "super" not an instance of
        # argument 1
        # My understanding is that super() is calling an instance method
        # In order to call a static method, you need super(cls, cls)
        err = super(Add, Add).validate(field, val, variables, **kwargs)
        if "allow_duplicate" in kwargs and not isinstance(
            kwargs["allow_duplicate"], bool
        ):
            err.append(
                "Add allow-duplicate must be boolean, found "
                f"'{kwargs['allow_duplicate']}'"
            )
        return err

    def apply(self, i_dict: Dotty) -> bool:
        """Evaluate action."""
        duplicate = "allow_duplicate" in self.config and self.config["allow_duplicate"]

        # Adder only if to_add is not already in existing, or config marks
        #   specifically to allow duplicating values.
        def _add(existing, to_add):
            return (to_add not in existing or duplicate) and existing.append(to_add)

        val = i_dict.get(self.field, [])
        if isinstance(self.value, list):
            for v in self.value:
                _add(val, v)
        else:
            _add(val, self.value)
        i_dict[self.field] = val
        return True

    def __repr__(self):
        """Implement `repr()`."""
        return f"add {self.value} to {self._field}"
