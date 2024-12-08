import pytest
from dual_autodiff.dual import Dual
from dual_autodiff.functions import (
    sin, cos, tan, log, exp, sqrt, sinh, cosh, tanh, asin, acos, atan
)

def test_sin():
    a = Dual(0, 1)
    result = sin(a)
    assert result.real == 0
    assert result.dual == 1

def test_cos():
    a = Dual(0, 1)
    result = cos(a)
    assert result.real == 1
    assert result.dual == 0

def test_tan():
    a = Dual(0, 1)
    result = tan(a)
    assert result.real == 0
    assert result.dual == 1

def test_log():
    a = Dual(2, 1)
    result = log(a)
    assert result.real == pytest.approx(0.693, rel=1e-3)
    assert result.dual == 0.5

def test_exp():
    a = Dual(1, 1)
    result = exp(a)
    assert result.real == pytest.approx(2.718, rel=1e-3)
    assert result.dual == pytest.approx(2.718, rel=1e-3)

def test_sqrt():
    a = Dual(4, 1)
    result = sqrt(a)
    assert result.real == 2
    assert result.dual == 0.25

def test_asin():
    a = Dual(0.5, 1)
    result = asin(a)
    assert result.real == pytest.approx(0.5236, rel=1e-3)
    assert result.dual == pytest.approx(1.1547, rel=1e-3)

def test_acos():
    a = Dual(0.5, 1)
    result = acos(a)
    assert result.real == pytest.approx(1.047, rel=1e-3)
    assert result.dual == pytest.approx(-1.1547, rel=1e-3)

def test_atan():
    a = Dual(1, 1)
    result = atan(a)
    assert result.real == pytest.approx(0.7854, rel=1e-3)
    assert result.dual == 0.5

