import numpy as np
import sympy as sp
from typing import Union, List, Optional

class PysuMath:
    """Advanced Mathematical Operations Library"""
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate factorial of a number"""
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        return np.prod(range(1, n + 1)) if n > 0 else 1
    
    @staticmethod
    def nth_root(num: float, index: int = 2) -> float:
        """Calculate nth root of a number"""
        return num ** (1/index)
    
    @staticmethod
    def quadratic_equation(a: float, b: float, c: float) -> List[float]:
        """Solve quadratic equation ax² + bx + c = 0"""
        delta = (b**2) - (4*a*c)
        if delta < 0:
            return []
        elif delta == 0:
            return [-b/(2*a)]
        else:
            x1 = (-b + PysuMath.nth_root(delta)) / (2*a)
            x2 = (-b - PysuMath.nth_root(delta)) / (2*a)
            return [x1, x2]
    
    @staticmethod
    def lcm(*args: int) -> int:
        """Calculate Least Common Multiple"""
        return abs(np.lcm.reduce(args))
    
    @staticmethod
    def gcd(*args: int) -> int:
        """Calculate Greatest Common Divisor"""
        return abs(np.gcd.reduce(args))
    
    @staticmethod
    def derivative(expression: str, variable: str = 'x') -> str:
        """Calculate derivative of an expression"""
        x = sp.Symbol(variable)
        expr = sp.sympify(expression)
        return str(sp.diff(expr, x))
    
    @staticmethod
    def integral(expression: str, variable: str = 'x') -> str:
        """Calculate indefinite integral of an expression"""
        x = sp.Symbol(variable)
        expr = sp.sympify(expression)
        return str(sp.integrate(expr, x))
    
    @staticmethod
    def matrix_inverse(matrix: List[List[float]]) -> List[List[float]]:
        """Calculate inverse of a matrix"""
        return np.linalg.inv(matrix).tolist()
    
    @staticmethod
    def trigonometric(angle: float, function: str = 'sin') -> float:
        """Calculate trigonometric functions (sin, cos, tan)"""
        if function.lower() == 'sin':
            return np.sin(np.radians(angle))
        elif function.lower() == 'cos':
            return np.cos(np.radians(angle))
        elif function.lower() == 'tan':
            return np.tan(np.radians(angle))
        else:
            raise ValueError("Invalid function. Use 'sin', 'cos' or 'tan'")