"""Basic computations with beta-expansions."""

from .core import beta_projection, greedy_expansion
from .model import BetaExpansion

__all__ = ["BetaExpansion", "beta_projection", "greedy_expansion"]
__version__ = "0.1.0"
