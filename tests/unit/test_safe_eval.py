import pytest

from common.safe_eval import safe_eval


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("1+2*3", 7),
        ("(2+3)*4", 20),
        ("-5+10", 5),
        ("2**3", 8),
    ],
)
def test_safe_eval(expr, expected):
    assert safe_eval(expr) == expected


def test_safe_eval_rejects_invalid():
    with pytest.raises(ValueError):
        safe_eval("__import__('os').system('whoami')")
