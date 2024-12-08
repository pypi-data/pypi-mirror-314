# dual_autodiff_x

A Cythonized Python package for forward-mode automatic differentiation using dual numbers.

## Overview

`dual_autodiff_x` is an optimized version of the `dual_autodiff` package, leveraging Cython to improve computational performance. It provides tools to compute derivatives of functions using forward-mode automatic differentiation with dual numbers.

---

## Installation

### Prerequisites

- Python 3.9 or later
- Cython

### Installing the Package

1. Clone the repository:
```bash
   git clone https://github.com/your_username/dual_autodiff_x.git
   cd dual_autodiff_x
```

2. Install the package in editable mode:
```bash
pip install -e .
```

3. Verify the installation:
```bash
python -c 'import dual_autodiff; print("dual_autodiff imported successfully!")'
```

---

## Usage

### Importing the Package

To use the package:
```python
import dual_autodiff as df
from dual_autodiff.dual import Dual
from dual_autodiff.functions import sin, cos, log
```

### Creating Dual Numbers
```python
x = Dual(2, 1)  # Represents the dual number 2 + 1ε
```

### Performing Operations
```python
# Example: f(x) = log(sin(x)) + x^2 * cos(x)
f_x = log(sin(x)) + x**2 * cos(x)
print(f_x)  # Output the result and its derivative
```

---

## Performance

The Cythonized version of dual_autodiff_x is significantly faster for computationally intensive operations compared to its pure Python counterpart. This is achieved by compiling key modules (dual.py and functions.py) into efficient shared object (.so) files.



