# dual_autodiff

`dual_autodiff` is a Python package that provides automatic differentiation using dual numbers. It is designed to handle derivatives and mathematical operations efficiently. The package also includes `dual_autodiff_x`, a Cython-optimized version for enhanced performance.

---

## Features

- Automatic differentiation using dual numbers.
- Support for a wide range of mathematical funtions:
- Cython-optimized version (`dual_autodiff_x`) for improved speed.

---

## Installation

### Prerequisites
- Python 3.9 or higher.
- `pip` for package installation.
- `conda` (optional) for managing virtual environments.

### Installing `dual_autodiff`
#### Using pip
Clone the repository and install the package:

```bash
git clone 'https://gitlab.developers.cam.ac.uk/phy/data-intensive-science-mphil/assessments/c1_coursework1/rsr45.git'
cd dual_autodiff
pip install e .
```

#### Using conda
1. Create a virtual environment using the provided `environment.yaml` file:
```bash
conda env create -n dual_env -f environment.yaml
```
2. Activate the environment:
```bash
conda activate dual_env
```
3. Install the package within this environment:
```bash
pip install -e .
```


## Usage
### Using `dual_autodiff`

```python
from dual_autodiff import Dual, sin, cos

# Create a Dual object
x = Dual(1.0, 1.0)  

# Perform operations
y = sin(x)
print(f"Value: {y.real}, Derivative: {y.dual}")
```

## Available Functions

### **Dual Class Methods**
The following methods are available in the `Dual` class:

#### **Arithmetic Operations**
- `__add__`, `__radd__` - Addition
- `__sub__`, `__rsub__` - Subtraction
- `__mul__`, `__rmul__` - Multiplication
- `__truediv__`, `__rtruediv__` - Division
- `__pow__` - Power

#### **Trigonometric Functions**
- `sin()` - Sine
- `cos()` - Cosine
- `tan()` - Tangent
- `asin()` - Arcsine
- `acos()` - Arccosine
- `atan()` - Arctangent

#### **Exponential and Logarithmic Functions**
- `exp()` - Exponential
- `log()` - Natural Logarithm
- `sqrt()` - Square Root

#### **Hyperbolic Functions**
- `sinh()` - Hyperbolic Sine
- `cosh()` - Hyperbolic Cosine
- `tanh()` - Hyperbolic Tangent

---

### **Global Functions in `functions.py`**
These functions are global aliases for the corresponding `Dual` class methods, allowing them to be called directly with either `float` or `Dual` inputs:

#### **Trigonometric Functions**
- `sin`
- `cos`
- `tan`
- `asin`
- `acos`
- `atan`

#### **Exponential and Logarithmic Functions**
- `exp`
- `log`
- `sqrt`

#### **Hyperbolic Functions**
- `sinh`
- `cosh`
- `tanh`

---

## How It Works

### Dual Numbers
Dual numbers are numbers of the form:

\[
a + b $\epsilon$
\]

Where:
- a is the **real part**, representing the function value.
- b is the **dual part**, representing the derivative.
- $\epsilon$^2 = 0\, making \(\epsilon\) infinitesimally small.

This structure allows for efficient computation of derivatives during operations.

---
### Cython Optimization

The `dual_autodiff_x` package uses Cython to compile critical operations into C, providing a significant speed boost for computationally intensive tasks.

### Installing `dual_autodiff_x`
For the Cython-optimized version:

```bash
cd dual_autodiff_x
pip install e .
```



See the README.md file in `dual_autodiff_x`.




