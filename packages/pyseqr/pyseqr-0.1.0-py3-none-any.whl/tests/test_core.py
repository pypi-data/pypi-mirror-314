from pyseqr.core import placeholder_function


def test_placeholder_function():
    assert placeholder_function() == "This is a placeholder."
