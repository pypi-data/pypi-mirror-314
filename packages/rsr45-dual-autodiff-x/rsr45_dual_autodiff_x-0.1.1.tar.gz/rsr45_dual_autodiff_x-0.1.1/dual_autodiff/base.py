# base.py
"""
Base functionality for the dual_autodiff package.
Contains utilities or helper functions that may be shared across modules.
"""

def is_dual_instance(value):
    """
    Checks if the given value is an instance of the Dual class.
    """
    from dual_autodiff.dual import Dual
    return isinstance(value, Dual)

def ensure_dual(value):
    """
    Ensures the input is a Dual object.
    If the input is not a Dual, wraps it into a Dual object with a zero dual part.
    """
    from dual_autodiff.dual import Dual
    return value if isinstance(value, Dual) else Dual(value)

