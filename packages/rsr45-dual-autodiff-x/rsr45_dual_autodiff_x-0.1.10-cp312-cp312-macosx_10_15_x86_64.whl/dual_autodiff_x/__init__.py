"""
rsr45-dual-autodiff-x: A package for dual number-based automatic differentiation.
"""

try:
    from .dual import Dual
    from .functions import (
        sin, cos, tan, log, exp, sqrt,
        sinh, cosh, tanh, asin, acos, atan
    )
except ImportError as e:
    raise ImportError(
        "Required modules are missing or failed to build. Ensure the package is correctly installed."
    ) from e

# Define the version directly here
__version__ = "0.1.10"

# Define the public API
__all__ = [
    "__version__",  # Expose version information
    "Dual",         # Expose the Dual class
    "sin", "cos", "tan", "log", "exp", "sqrt",  # Expose functions
    "sinh", "cosh", "tanh", "asin", "acos", "atan"
]

