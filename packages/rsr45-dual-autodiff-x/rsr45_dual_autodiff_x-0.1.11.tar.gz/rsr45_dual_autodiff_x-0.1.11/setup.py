from setuptools import setup, Extension
from Cython.Build import cythonize

# Read the content of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define the extensions (Cython modules)
extensions = [
    Extension("dual_autodiff_x.base", ["dual_autodiff_x/base.pyx"]),
    Extension("dual_autodiff_x.dual", ["dual_autodiff_x/dual.pyx"]),
    Extension("dual_autodiff_x.functions", ["dual_autodiff_x/functions.pyx"]),
]

# Call setup with cythonized extensions
setup(
    name="rsr45-dual-autodiff-x",
    version="0.1.11",  # Updated version
    description="A package for dual number-based automatic differentiation (optimized version)",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify Markdown format
    ext_modules=cythonize(
        extensions, 
        compiler_directives={"language_level": "3"}  # Use Python 3 language level
    ),
    packages=["dual_autodiff_x"],  # Ensure namespace is accurate
    package_data={"dual_autodiff_x": ["*.so"]},  # Include compiled shared objects
    exclude_package_data={"dual_autodiff_x": ["*.pyx", "*.py"]},  # Exclude source files
    zip_safe=False,  # Package is not zip-safe due to compiled extensions
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.6",  # Specify minimum Python version
)

