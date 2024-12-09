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
    version="0.1.7",  # Incremented version
    description="A package for dual number-based automatic differentiation",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify Markdown format
    ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}),
    packages=["dual_autodiff_x"],  # Updated namespace
    package_data={"dual_autodiff_x": ["*.so"]},
    exclude_package_data={"dual_autodiff_x": ["*.pyx", "*.py"]},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

