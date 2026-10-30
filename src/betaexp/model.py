"""Convenience interface for a fixed beta."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from .core import Number, _as_decimal, _validate_beta, _validate_precision, beta_projection, greedy_expansion


@dataclass(frozen=True, slots=True)
class BetaExpansion:
    """Computations for a fixed base ``beta`` in the interval ``(1, 2)``."""

    beta: Decimal
    precision: int = 50

    def __init__(self, beta: Number, *, precision: int = 50) -> None:
        precision = _validate_precision(precision)
        b = _validate_beta(beta)
        object.__setattr__(self, "beta", _as_decimal(b, name="beta"))
        object.__setattr__(self, "precision", precision)

    def greedy(self, x: Number, n_digits: int = 20) -> tuple[int, ...]:
        """Return the first digits of the greedy expansion of ``x``."""
        return greedy_expansion(
            x,
            self.beta,
            n_digits=n_digits,
            precision=self.precision,
        )

    def project(self, digits: Iterable[int]) -> Decimal:
        """Project a finite binary word using this base."""
        return beta_projection(digits, self.beta, precision=self.precision)
