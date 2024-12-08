from setuptools import setup, Extension
from Cython.Build import cythonize

# Define the extensions (Cython modules)
extensions = [
    Extension("dual_autodiff.base", ["dual_autodiff/base.pyx"]),
    Extension("dual_autodiff.dual", ["dual_autodiff/dual.pyx"]),
    Extension("dual_autodiff.functions", ["dual_autodiff/functions.pyx"]),
]

# Call setup with cythonized extensions
setup(
    name="rsr45_dual_autodiff_x",
    version="0.0.1b2",
    description="A package for dual number-based automatic differentiation",
    ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}),
    packages=["dual_autodiff"],
    package_data={"dual_autodiff": ["*.so"]},
    exclude_package_data={"dual_autodiff": ["*.pyx", "*.py"]},
    zip_safe=False,
)

