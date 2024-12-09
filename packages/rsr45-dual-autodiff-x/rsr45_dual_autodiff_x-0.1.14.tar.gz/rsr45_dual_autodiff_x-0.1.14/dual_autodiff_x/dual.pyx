import numpy as np

class Dual:
    def __init__(self, real, dual=0.0):
        self.real = real
        self.dual = dual

    def __repr__(self):
        return f"{self.real} + {self.dual}ε" if self.dual >= 0 else f"{self.real} - {-self.dual}ε"

    def __add__(self, other):
        if isinstance(other, Dual):
            return Dual(self.real + other.real, self.dual + other.dual)
        return Dual(self.real + other, self.dual)

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Dual):
            return Dual(self.real - other.real, self.dual - other.dual)
        return Dual(self.real - other, self.dual)

    def __rsub__(self, other):
        return Dual(other - self.real, -self.dual)

    def __mul__(self, other):
        if isinstance(other, Dual):
            return Dual(
                self.real * other.real,
                self.real * other.dual + self.dual * other.real
            )
        return Dual(self.real * other, self.dual * other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Dual):
            denom = other.real ** 2
            return Dual(
                self.real / other.real,
                (self.dual * other.real - self.real * other.dual) / denom
            )
        return Dual(self.real / other, self.dual / other)

    def __rtruediv__(self, other):
        return Dual(other / self.real, -other * self.dual / (self.real ** 2))

    def __pow__(self, power):
        if isinstance(power, (int, float)):
            real_part = self.real ** power
            dual_part = power * (self.real ** (power - 1)) * self.dual
            return Dual(real_part, dual_part)
        raise TypeError("Power must be an int or float")

    def sin(self):
        return Dual(np.sin(self.real), self.dual * np.cos(self.real))

    def cos(self):
        return Dual(np.cos(self.real), -self.dual * np.sin(self.real))

    def tan(self):
        tan_real = np.tan(self.real)
        return Dual(tan_real, self.dual * (1 + tan_real ** 2))

    def log(self):
        if self.real <= 0:
            raise ValueError("Logarithm only defined for positive real numbers.")
        return Dual(np.log(self.real), self.dual / self.real)

    def exp(self):
        exp_real = np.exp(self.real)
        return Dual(exp_real, self.dual * exp_real)

    def sqrt(self):
        if self.real < 0:
            raise ValueError("Square root only defined for non-negative real numbers.")
        sqrt_real = np.sqrt(self.real)
        return Dual(sqrt_real, self.dual / (2 * sqrt_real))

    def sinh(self):
        return Dual(np.sinh(self.real), self.dual * np.cosh(self.real))

    def cosh(self):
        return Dual(np.cosh(self.real), self.dual * np.sinh(self.real))

    def tanh(self):
        tanh_real = np.tanh(self.real)
        return Dual(tanh_real, self.dual * (1 - tanh_real ** 2))

    def asin(self):
        if abs(self.real) > 1:
            raise ValueError("asin is only defined for -1 <= x <= 1")
        return Dual(np.arcsin(self.real), self.dual / np.sqrt(1 - self.real ** 2))

    def acos(self):
        if abs(self.real) > 1:
            raise ValueError("acos is only defined for -1 <= x <= 1")
        return Dual(np.arccos(self.real), -self.dual / np.sqrt(1 - self.real ** 2))

    def atan(self):
        return Dual(np.arctan(self.real), self.dual / (1 + self.real ** 2))


