import pytest
from dual_autodiff.dual import Dual

def test_dual_addition():
    a = Dual(2, 3)
    b = Dual(4, 5)
    result = a + b
    assert result.real == 6
    assert result.dual == 8

def test_dual_subtraction():
    a = Dual(5, 3)
    b = Dual(2, 1)
    result = a - b
    assert result.real == 3
    assert result.dual == 2

def test_dual_multiplication():
    a = Dual(3, 2)
    b = Dual(4, 1)
    result = a * b
    assert result.real == 12
    assert result.dual == 11

def test_dual_division():
    a = Dual(6, 2)
    b = Dual(3, 1)
    result = a / b
    assert result.real == 2
    assert result.dual == 0

def test_dual_power():
    a = Dual(2, 1)
    result = a ** 3
    assert result.real == 8
    assert result.dual == 12

def test_dual_representation():
    a = Dual(5, -3)
    assert repr(a) == "5 - 3ε"

def test_dual_truediv_by_scalar():
    a = Dual(10, 4)
    result = a / 2
    assert result.real == 5
    assert result.dual == 2

