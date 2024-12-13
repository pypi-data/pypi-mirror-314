"""Test utility functions."""

from typing import Iterator

from kelvin.message.utils import flatten


def test_flatten() -> None:
    """Test flatten function."""

    data = {"a": {"b": 1, "c": {"d": 100}, "q": [1, 2, 3]}, "z": {}}

    result = flatten(data)
    assert isinstance(result, Iterator)

    assert [*result] == [
        ("a.b", 1),
        ("a.c.d", 100),
        ("a.q", [1, 2, 3]),
    ]
