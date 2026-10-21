# functional-testing-2507224

![CI](https://github.com/ZarinTasnim20/functional-testing-2507224/actions/workflows/ci.yml/badge.svg)

Functional tests, CI/CD and live deployment for `target.py` (16 functions: 11 data-type, 5 maths).

**Live URL:** https://functional-testing-2507224.onrender.com
**Health:** https://functional-testing-2507224.onrender.com/health (returns the deployed commit SHA)

## Setup

```bash
git clone https://github.com/ZarinTasnim20/functional-testing-2507224.git
cd functional-testing-2507224
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the tests

```bash
pytest tests/test_target.py --cov=target --cov-branch --cov-report=term-missing
```

Result: 195 tests, **100% line and branch coverage** of `target.py`.
Frontend tests: `pytest tests/test_app.py`. Lint: `ruff check .`

## Run the frontend locally

```bash
python app.py        # then open http://localhost:5000
```

Each of the 16 functions has a card: type Python values (`18`, `None`, `[1, 2]`, `{1, 2}`, `{"apple": 1}`) and press Run to see the result and its type, or the exception.

## CI/CD pipeline (`.github/workflows/ci.yml`)

1. **test**: runs on every push and on PRs to `main`, Python 3.10 / 3.11 / 3.12 with pip caching. Steps: lint (ruff), tests with `--cov-fail-under=100`, frontend tests, and the coverage report uploaded as an artifact.
2. **deploy** (`needs: test`): only on pushes to `main`. Calls the Render deploy hook stored in the `RENDER_DEPLOY_HOOK` GitHub secret. Auto-deploy is off on Render, so nothing goes live unless the tests pass.
3. **smoke-test** (`needs: deploy`): polls `/health` until the live SHA matches `GITHUB_SHA`, then checks three live requests (home page, a successful call, an error call).

## Suspected bugs in target.py

`target.py` has not been modified. These are behaviours that look wrong or are unspecified:

1. **`greet`**: a non-string name (for example `greet(123)`) raises `AttributeError` (`'int' object has no attribute 'strip'`) instead of a clear `TypeError` like `count_vowels` and `invert` do.
2. **`factorial`**: a float such as `factorial(2.5)` raises an unhelpful `TypeError` from `range()`. `factorial(5.0)` is also rejected even though it is a whole number. There is no explicit type check.
3. **`is_adult`**: `True`/`False` are accepted as ages (`is_adult(True)` returns `False`) because `bool` is a subclass of `int`. Non-numbers raise a generic `TypeError` from the comparison.
4. **`is_leap_year`**: same `bool` problem (`is_leap_year(True)` treats it as year 1). Years before 1582 use Gregorian rules, which did not exist yet.
5. **`find_max` / `average`**: `average([True, False])` returns `0.5` because bools count as numbers. A non-list such as `None` gives a generic `TypeError` from `len()`, not a clear message.
6. **`swap`**: accepts any length-2 sequence (a list or the string `"xy"`), not only tuples.
7. **`common_items`**: no type check, so lists raise a generic `TypeError` from the `&` operator. A set and a frozenset work, but the result type follows the first argument.
8. **`celsius_to_fahrenheit`**: accepts temperatures below absolute zero (−273.15 °C) without error.
9. **`to_int`**: `to_int("3.5")` raises `ValueError` and `to_int(float("inf"))` raises `OverflowError`. Neither is documented.
10. **`divide`**: `divide(float("nan"), 1)` returns `nan` silently.

## Project structure

```
target.py                 # given, unchanged
tests/test_target.py      # functional tests (195)
tests/test_app.py         # frontend/API tests
app.py, templates/        # Flask frontend + /health
.github/workflows/ci.yml  # test → deploy → smoke-test
render.yaml               # Render service (autoDeploy: false)
requirements.txt          # pinned
```
