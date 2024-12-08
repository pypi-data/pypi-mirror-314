import pytest
from dual_autodiff.base import is_dual_instance, ensure_dual
from dual_autodiff.dual import Dual

def test_is_dual_instance():
    # Test with a Dual instance
    dual_num = Dual(2, 1)
    assert is_dual_instance(dual_num) == True

    # Test with a non-Dual instance (e.g., integer)
    non_dual_num = 5
    assert is_dual_instance(non_dual_num) == False

    # Test with a non-Dual instance (e.g., float)
    non_dual_num_float = 3.14
    assert is_dual_instance(non_dual_num_float) == False

    # Test with a string
    non_dual_string = "not a dual number"
    assert is_dual_instance(non_dual_string) == False


def test_ensure_dual():
    # Test with a Dual instance (should return the same object)
    dual_num = Dual(2, 1)
    result = ensure_dual(dual_num)
    assert isinstance(result, Dual)
    assert result.real == 2
    assert result.dual == 1

    # Test with an integer (should wrap it into a Dual object)
    int_num = 5
    result = ensure_dual(int_num)
    assert isinstance(result, Dual)
    assert result.real == 5
    assert result.dual == 0  # Default dual part should be 0

    # Test with a float (should wrap it into a Dual object)
    float_num = 3.14
    result = ensure_dual(float_num)
    assert isinstance(result, Dual)
    assert result.real == 3.14
    assert result.dual == 0  # Default dual part should be 0

