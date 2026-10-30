from decimal import Decimal, localcontext

from betaexp import BetaExpansion


def test_fixed_beta_interface() -> None:
    system = BetaExpansion("1.5", precision=60)
    digits = system.greedy("0.75", n_digits=5)

    with localcontext() as ctx:
        ctx.prec = 60
        expected = Decimal(1) / Decimal("1.5")

    assert digits == (1, 0, 0, 0, 0)
    assert system.project(digits) == expected


def test_beta_is_stored_as_decimal() -> None:
    system = BetaExpansion(1.7)
    assert system.beta == Decimal("1.7")
