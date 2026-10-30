from decimal import Decimal, localcontext

import pytest

from betaexp import beta_projection, greedy_expansion


def test_zero_has_zero_expansion() -> None:
    assert greedy_expansion(0, 1.5, 8) == (0,) * 8


def test_terminating_expansion_is_padded_with_zeros() -> None:
    digits = greedy_expansion(Decimal("0.75"), Decimal("1.5"), 6)
    assert digits == (1, 0, 0, 0, 0, 0)


def test_projection_of_single_one() -> None:
    value = beta_projection([1], Decimal("1.5"))
    with localcontext() as ctx:
        ctx.prec = 50
        expected = Decimal(1) / Decimal("1.5")
    assert value == expected


def test_projection_accepts_generators() -> None:
    digits = (digit for digit in [1, 0, 1])
    value = beta_projection(digits, Decimal("1.5"))
    with localcontext() as ctx:
        ctx.prec = 50
        expected = Decimal(1) / Decimal("1.5") + Decimal(1) / Decimal("1.5") ** 3
    assert value == expected


def test_greedy_prefix_reconstructs_x_from_below() -> None:
    beta = Decimal("1.7")
    x = Decimal("0.4")
    digits = greedy_expansion(x, beta, 40, precision=80)
    approximation = beta_projection(digits, beta, precision=80)

    with localcontext() as ctx:
        ctx.prec = 80
        error_bound = beta ** Decimal(-40)

    assert approximation <= x
    assert x - approximation < error_bound


@pytest.mark.parametrize("beta", [1, 2, 0.9, 2.1])
def test_beta_must_lie_between_one_and_two(beta: float) -> None:
    with pytest.raises(ValueError):
        greedy_expansion(0.5, beta)


def test_x_must_lie_in_unit_interval() -> None:
    with pytest.raises(ValueError):
        greedy_expansion(-0.1, 1.5)
    with pytest.raises(ValueError):
        greedy_expansion(1.1, 1.5)


def test_digits_must_be_binary() -> None:
    with pytest.raises(ValueError):
        beta_projection([1, 2, 0], 1.5)


def test_zero_digits_returns_empty_tuple() -> None:
    assert greedy_expansion(0.5, 1.5, 0) == ()


def test_non_integer_n_digits_is_rejected() -> None:
    with pytest.raises(TypeError):
        greedy_expansion(0.5, 1.5, 5.0)  # type: ignore[arg-type]
