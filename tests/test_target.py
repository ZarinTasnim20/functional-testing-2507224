"""Functional tests for target.py - every corner case of all 16 functions."""

import math

import pytest

import target


# ---------------------------------------------------------------- 1. is_adult
@pytest.mark.parametrize(
    "age, expected",
    [
        (0, False),
        (1, False),
        (17, False),
        (18, True),  # boundary
        (19, True),
        (120, True),
        (17.99, False),
        (18.0, True),
    ],
)
def test_is_adult_valid(age, expected):
    result = target.is_adult(age)
    assert result is expected
    assert isinstance(result, bool)


@pytest.mark.parametrize("age", [-1, -18, -0.5])
def test_is_adult_negative_raises(age):
    with pytest.raises(ValueError, match="age cannot be negative"):
        target.is_adult(age)


@pytest.mark.parametrize("age", ["18", None, [18]])
def test_is_adult_wrong_type(age):
    with pytest.raises(TypeError):
        target.is_adult(age)


# ------------------------------------------------------- 2. celsius_to_fahrenheit
@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32.0),
        (100, 212.0),
        (-40, -40.0),  # the two scales meet
        (37, 98.6),
        (-273.15, -459.67),  # absolute zero
        (36.6, 97.88),
        (1.234, 34.22),  # rounded to 2 decimals
    ],
)
def test_celsius_to_fahrenheit_valid(celsius, expected):
    result = target.celsius_to_fahrenheit(celsius)
    assert result == pytest.approx(expected)
    assert isinstance(result, float)
    assert round(result, 2) == result


@pytest.mark.parametrize("celsius", ["0", None, [0]])
def test_celsius_to_fahrenheit_wrong_type(celsius):
    with pytest.raises(TypeError):
        target.celsius_to_fahrenheit(celsius)


# ------------------------------------------------------------- 3. count_vowels
@pytest.mark.parametrize(
    "text, expected",
    [
        ("", 0),
        ("bcdfg", 0),
        ("aeiou", 5),
        ("AEIOU", 5),  # case insensitive
        ("Hello World", 3),
        ("rhythm", 0),  # y is not a vowel
        ("a", 1),
        ("123 !?", 0),
        ("Programming", 3),
    ],
)
def test_count_vowels_valid(text, expected):
    result = target.count_vowels(text)
    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize("text", [None, 123, ["a", "e"], b"aeiou"])
def test_count_vowels_wrong_type(text):
    with pytest.raises(TypeError, match="text must be a string"):
        target.count_vowels(text)


# ------------------------------------------------------------------ 4. invert
@pytest.mark.parametrize("flag, expected", [(True, False), (False, True)])
def test_invert_valid(flag, expected):
    assert target.invert(flag) is expected


@pytest.mark.parametrize("flag", [0, 1, "True", None, 1.0, []])
def test_invert_wrong_type(flag):
    with pytest.raises(TypeError, match="flag must be True or False"):
        target.invert(flag)


# ------------------------------------------------------------------- 5. greet
@pytest.mark.parametrize(
    "name, expected",
    [
        ("Zarin", "Hello, Zarin!"),
        ("  Alif  ", "Hello, Alif!"),  # surrounding spaces stripped
        ("Mary Jane", "Hello, Mary Jane!"),
        ("A", "Hello, A!"),
        (None, "Hello, Guest!"),
        ("", "Hello, Guest!"),
        ("   ", "Hello, Guest!"),
        ("\t\n", "Hello, Guest!"),
    ],
)
def test_greet(name, expected):
    assert target.greet(name) == expected


def test_greet_default_argument():
    assert target.greet() == "Hello, Guest!"


@pytest.mark.parametrize("name", [123, ["Zarin"]])
def test_greet_wrong_type(name):
    # Suspected bug (see README): a non-string name raises AttributeError.
    with pytest.raises(AttributeError):
        target.greet(name)


# ---------------------------------------------------------------- 6. find_max
@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([5], 5),
        ([1, 2, 3], 3),
        ([3, 2, 1], 3),
        ([-5, -2, -9], -2),
        ([2, 2, 2], 2),
        ([1.5, 2.5, 0.5], 2.5),
        ([0, -0.1], 0),
        ((4, 9, 1), 9),
    ],
)
def test_find_max_valid(numbers, expected):
    assert target.find_max(numbers) == expected


def test_find_max_returns_element_type():
    assert type(target.find_max([1, 7, 3])) is int
    assert type(target.find_max([1.0, 7.5])) is float


@pytest.mark.parametrize("numbers", [[], ()])
def test_find_max_empty_raises(numbers):
    with pytest.raises(ValueError, match="list is empty"):
        target.find_max(numbers)


@pytest.mark.parametrize("numbers", [None, 5])
def test_find_max_wrong_type(numbers):
    with pytest.raises(TypeError):
        target.find_max(numbers)


def test_find_max_mixed_types():
    with pytest.raises(TypeError):
        target.find_max([1, "2"])


# --------------------------------------------------------------- 7. get_price
PRICES = {"apple": 0.5, "bread": 2, "milk": 1.25, "free": 0}


@pytest.mark.parametrize(
    "item, expected",
    [("apple", 0.5), ("bread", 2), ("milk", 1.25), ("free", 0)],
)
def test_get_price_valid(item, expected):
    result = target.get_price(PRICES, item)
    assert result == expected
    assert type(result) is type(PRICES[item])


@pytest.mark.parametrize("item", ["banana", "Apple", "", "apple "])
def test_get_price_missing_raises(item):
    with pytest.raises(KeyError, match="not found"):
        target.get_price(PRICES, item)


def test_get_price_empty_dict():
    with pytest.raises(KeyError, match="apple not found"):
        target.get_price({}, "apple")


def test_get_price_does_not_modify_dict():
    prices = dict(PRICES)
    target.get_price(prices, "apple")
    assert prices == PRICES


# -------------------------------------------------------------------- 8. swap
@pytest.mark.parametrize(
    "pair, expected",
    [
        ((1, 2), (2, 1)),
        (("a", "b"), ("b", "a")),
        ((1, 1), (1, 1)),
        ((None, 0), (0, None)),
        ([3, 4], (4, 3)),  # a list of two still works
        ("xy", ("y", "x")),
    ],
)
def test_swap_valid(pair, expected):
    result = target.swap(pair)
    assert result == expected
    assert isinstance(result, tuple)


@pytest.mark.parametrize("pair", [(), (1,), (1, 2, 3), [1, 2, 3, 4]])
def test_swap_wrong_length_raises(pair):
    with pytest.raises(ValueError, match="pair must have exactly 2 values"):
        target.swap(pair)


@pytest.mark.parametrize("pair", [None, 12])
def test_swap_wrong_type(pair):
    with pytest.raises(TypeError):
        target.swap(pair)


# ------------------------------------------------------------- 9. common_items
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ({1, 2, 3}, {2, 3, 4}, {2, 3}),
        ({1, 2}, {3, 4}, set()),
        (set(), {1, 2}, set()),
        (set(), set(), set()),
        ({1, 2}, {1, 2}, {1, 2}),
        ({"a", "b"}, {"b", "c"}, {"b"}),
        ({1, 2, 3}, {2}, {2}),
    ],
)
def test_common_items_valid(a, b, expected):
    result = target.common_items(a, b)
    assert result == expected
    assert isinstance(result, set)


def test_common_items_does_not_modify_inputs():
    a, b = {1, 2}, {2, 3}
    target.common_items(a, b)
    assert a == {1, 2} and b == {2, 3}


@pytest.mark.parametrize("a, b", [([1, 2], [2, 3]), ({1}, None), ("ab", {"a"})])
def test_common_items_wrong_type(a, b):
    with pytest.raises(TypeError):
        target.common_items(a, b)


# ----------------------------------------------------------- 10. is_leap_year
@pytest.mark.parametrize(
    "year, expected",
    [
        (2024, True),  # divisible by 4
        (2023, False),
        (1900, False),  # divisible by 100, not 400
        (2000, True),  # divisible by 400
        (2100, False),
        (2400, True),
        (4, True),
        (1, False),  # boundary
        (400, True),
    ],
)
def test_is_leap_year_valid(year, expected):
    assert target.is_leap_year(year) is expected


@pytest.mark.parametrize("year", [0, -1, -400])
def test_is_leap_year_below_one_raises(year):
    with pytest.raises(ValueError, match="year must be 1 or more"):
        target.is_leap_year(year)


@pytest.mark.parametrize("year", ["2024", None])
def test_is_leap_year_wrong_type(year):
    with pytest.raises(TypeError):
        target.is_leap_year(year)


# ----------------------------------------------------------------- 11. to_int
@pytest.mark.parametrize(
    "value, expected",
    [
        (5, 5),
        (-5, -5),
        (0, 0),
        (3.9, 3),  # truncates toward zero
        (-3.9, -3),
        ("42", 42),
        (" 7 ", 7),
        ("-10", -10),
    ],
)
def test_to_int_valid(value, expected):
    result = target.to_int(value)
    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize("value", [True, False])
def test_to_int_bool_raises(value):
    with pytest.raises(TypeError, match="bool is not allowed"):
        target.to_int(value)


@pytest.mark.parametrize("value", ["3.5", "abc", ""])
def test_to_int_bad_string_raises(value):
    with pytest.raises(ValueError):
        target.to_int(value)


@pytest.mark.parametrize("value", [None, [1]])
def test_to_int_wrong_type(value):
    with pytest.raises(TypeError):
        target.to_int(value)


def test_to_int_infinity_raises():
    with pytest.raises(OverflowError):
        target.to_int(float("inf"))


# ----------------------------------------------------------------- 12. divide
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 2, 5.0),
        (7, 2, 3.5),
        (-9, 3, -3.0),
        (0, 5, 0.0),
        (1, 3, 1 / 3),
        (5, 0.5, 10.0),
        (-1, -4, 0.25),
    ],
)
def test_divide_valid(a, b, expected):
    result = target.divide(a, b)
    assert result == pytest.approx(expected)
    assert isinstance(result, float)


@pytest.mark.parametrize("a, b", [(1, 0), (0, 0), (5, 0.0), (-3, -0.0)])
def test_divide_by_zero_raises(a, b):
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        target.divide(a, b)


@pytest.mark.parametrize("a, b", [("10", 2), (10, None)])
def test_divide_wrong_type(a, b):
    with pytest.raises(TypeError):
        target.divide(a, b)


# ------------------------------------------------------------------ 13. power
@pytest.mark.parametrize(
    "base, exponent, expected",
    [
        (2, 3, 8),
        (2, 0, 1),
        (0, 0, 1),
        (0, 5, 0),
        (-2, 3, -8),
        (-2, 2, 4),
        (5, 1, 5),
        (10, 10, 10_000_000_000),
    ],
)
def test_power_int(base, exponent, expected):
    result = target.power(base, exponent)
    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize(
    "base, exponent, expected",
    [(2, -1, 0.5), (4, 0.5, 2.0), (2.5, 2, 6.25), (9, -0.5, 1 / 3)],
)
def test_power_float(base, exponent, expected):
    result = target.power(base, exponent)
    assert result == pytest.approx(expected)
    assert isinstance(result, float)


def test_power_zero_negative_exponent_raises():
    with pytest.raises(ZeroDivisionError):
        target.power(0, -1)


@pytest.mark.parametrize("base, exponent", [("2", 3), (2, None)])
def test_power_wrong_type(base, exponent):
    with pytest.raises(TypeError):
        target.power(base, exponent)


# ------------------------------------------------------------ 14. square_root
@pytest.mark.parametrize(
    "x, expected",
    [(0, 0.0), (1, 1.0), (4, 2.0), (2, math.sqrt(2)), (0.25, 0.5), (1e10, 1e5)],
)
def test_square_root_valid(x, expected):
    result = target.square_root(x)
    assert result == pytest.approx(expected)
    assert isinstance(result, float)


@pytest.mark.parametrize("x", [-1, -0.0001, -100])
def test_square_root_negative_raises(x):
    with pytest.raises(
        ValueError, match="cannot take the square root of a negative number"
    ):
        target.square_root(x)


@pytest.mark.parametrize("x", ["4", None])
def test_square_root_wrong_type(x):
    with pytest.raises(TypeError):
        target.square_root(x)


# -------------------------------------------------------------- 15. factorial
@pytest.mark.parametrize(
    "n, expected",
    [(0, 1), (1, 1), (2, 2), (3, 6), (5, 120), (10, 3_628_800), (20, 2432902008176640000)],
)
def test_factorial_valid(n, expected):
    result = target.factorial(n)
    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize("n", [-1, -10])
def test_factorial_negative_raises(n):
    with pytest.raises(
        ValueError, match="factorial is not defined for negative numbers"
    ):
        target.factorial(n)


@pytest.mark.parametrize("n", [2.5, "5", None])
def test_factorial_wrong_type(n):
    with pytest.raises(TypeError):
        target.factorial(n)


# ---------------------------------------------------------------- 16. average
@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([5], 5.0),
        ([1, 2, 3], 2.0),
        ([1, 2], 1.5),
        ([-1, 1], 0.0),
        ([0.1, 0.2, 0.3], 0.2),
        ([10, 20, 30, 40], 25.0),
        ((2, 4), 3.0),
    ],
)
def test_average_valid(numbers, expected):
    result = target.average(numbers)
    assert result == pytest.approx(expected)
    assert isinstance(result, float)


@pytest.mark.parametrize("numbers", [[], ()])
def test_average_empty_raises(numbers):
    with pytest.raises(ValueError, match="list is empty"):
        target.average(numbers)


@pytest.mark.parametrize("numbers", [None, ["1", "2"]])
def test_average_wrong_type(numbers):
    with pytest.raises(TypeError):
        target.average(numbers)
