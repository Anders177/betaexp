"""Core routines for beta-expansions."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext
from typing import Iterable, TypeAlias

Number: TypeAlias = int | float | str | Decimal


def _as_decimal(value: Number, *, name: str) -> Decimal:
    """Convert a supported numeric value to a finite Decimal."""
    try:
        result = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{name} must be a real number") from exc

    if not result.is_finite():
        raise ValueError(f"{name} must be finite")
    return result


def _validate_beta(beta: Number) -> Decimal:
    value = _as_decimal(beta, name="beta")
    if not Decimal(1) < value < Decimal(2):
        raise ValueError("beta must satisfy 1 < beta < 2")
    return value


def _validate_precision(precision: int) -> int:
    if isinstance(precision, bool) or not isinstance(precision, int):
        raise TypeError("precision must be an integer")
    if precision < 16:
        raise ValueError("precision must be at least 16")
    return precision


def _validate_n_digits(n_digits: int) -> int:
    if isinstance(n_digits, bool) or not isinstance(n_digits, int):
        raise TypeError("n_digits must be an integer")
    if n_digits < 0:
        raise ValueError("n_digits must be non-negative")
    return n_digits


def greedy_expansion(
    x: Number,
    beta: Number,
    n_digits: int = 20,
    *,
    precision: int = 50,
) -> tuple[int, ...]:
    """Return the first ``n_digits`` digits of the greedy beta-expansion of ``x``.

    The implementation is restricted to ``1 < beta < 2`` and ``0 <= x <= 1``.
    Digits therefore belong to ``{0, 1}``.

    Parameters
    ----------
    x:
        Number to expand.
    beta:
        Base of the expansion.
    n_digits:
        Number of digits to compute.
    precision:
        Decimal working precision used by the iteration.
    """
    n_digits = _validate_n_digits(n_digits)
    precision = _validate_precision(precision)

    with localcontext() as ctx:
        ctx.prec = precision
        b = _validate_beta(beta)
        remainder = _as_decimal(x, name="x")

        if not Decimal(0) <= remainder <= Decimal(1):
            raise ValueError("x must satisfy 0 <= x <= 1")

        digits: list[int] = []
        for _ in range(n_digits):
            y = b * remainder
            digit = int(y)

            if digit not in (0, 1):
                raise ArithmeticError("computed digit lies outside {0, 1}")

            digits.append(digit)
            remainder = y - digit

            if remainder == 0:
                digits.extend([0] * (n_digits - len(digits)))
                break

        return tuple(digits)


def beta_projection(
    digits: Iterable[int],
    beta: Number,
    *,
    precision: int = 50,
) -> Decimal:
    """Project a finite binary word to the real line.

    For digits ``d_1, ..., d_n``, this returns

    ``sum(d_k / beta**k for k in range(1, n + 1))``.
    """
    precision = _validate_precision(precision)

    with localcontext() as ctx:
        ctx.prec = precision
        b = _validate_beta(beta)
        value = Decimal(0)
        weight = Decimal(1) / b

        for digit in digits:
            if isinstance(digit, bool) or not isinstance(digit, int) or digit not in (0, 1):
                raise ValueError("digits must contain only the integers 0 and 1")
            if digit:
                value += weight
            weight /= b

        return +value
