# betaexp

`betaexp` is a small Python library for computations with beta-expansions in the range

\[
1 < \beta < 2.
\]

The first release contains two basic operations: greedy expansions and the natural projection of finite binary words.

## Installation

Clone the repository and install it in editable mode:

```bash
git clone <your-repository-url>
cd betaexp
python -m pip install -e .
```

To run the tests:

```bash
python -m pip install -e ".[test]"
pytest
```

## Basic use

```python
from betaexp import greedy_expansion, beta_projection

beta = "1.7"
x = "0.4"

digits = greedy_expansion(x, beta, n_digits=20)
approximation = beta_projection(digits, beta)

print(digits)
print(approximation)
```

For repeated computations with the same base:

```python
from betaexp import BetaExpansion

system = BetaExpansion("1.7", precision=60)

digits = system.greedy("0.4", n_digits=20)
value = system.project(digits)
```

## Definitions used in v0.1.0

For `0 <= x <= 1`, the greedy digits are obtained from

\[
d_n(x)=\left\lfloor \beta T_\beta^{n-1}(x)\right\rfloor,
\qquad
T_\beta(x)=\beta x-\lfloor \beta x\rfloor.
\]

For a finite word `d_1 ... d_n`, the projection is

\[
\pi_\beta(d_1\ldots d_n)
=\sum_{k=1}^{n}\frac{d_k}{\beta^k}.
\]

Since `1 < beta < 2`, the digits are restricted to `{0, 1}`.

## Numerical note

The implementation uses `decimal.Decimal` internally. Strings and `Decimal` objects are recommended when the input value needs to be controlled explicitly. Python floats are accepted, but values produced by previous floating-point calculations may already carry rounding error.

For example:

```python
BetaExpansion("1.7")
```

is preferable to

```python
BetaExpansion(1.7)
```

when the decimal value `1.7` is intended exactly. Near discontinuity points of the greedy transformation, increasing `precision` may be necessary.

## Scope

Version 0.1.0 is intentionally small. It does not yet implement admissibility, the language of the beta-shift, lazy expansions, cylinders, or symbolic dynamics utilities.

## License

MIT License.
