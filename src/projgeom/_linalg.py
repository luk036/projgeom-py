"""
Internal 3x3 linear-algebra helpers over the rationals.

These helpers exist so that the conic and transform modules can perform exact
matrix operations (inverse, adjugate, products) without a floating-point or
symbolic dependency. They are an implementation detail and are not part of the
public API.
"""

from fractions import Fraction
from typing import List

Matrix = List[List[Fraction]]
Vector = List[Fraction]


def determinant3(m: Matrix) -> Fraction:
    """Return the determinant of a 3x3 matrix.

    :param m: A 3x3 matrix of :class:`Fraction` values.
    :return: The determinant.
    """
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def adjugate3(m: Matrix) -> Matrix:
    """Return the adjugate (classical adjoint) of a 3x3 matrix.

    The adjugate satisfies ``m @ adjugate3(m) == determinant3(m) * I``, so it
    is the numerator of the inverse and is well defined even for singular
    matrices.

    :param m: A 3x3 matrix of :class:`Fraction` values.
    :return: The adjugate matrix.
    """
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    return [
        [e * i - f * h, c * h - b * i, b * f - c * e],
        [f * g - d * i, a * i - c * g, c * d - a * f],
        [d * h - e * g, b * g - a * h, a * e - b * d],
    ]


def inverse3(m: Matrix) -> Matrix:
    """Return the inverse of a 3x3 matrix.

    :param m: A 3x3 matrix of :class:`Fraction` values.
    :return: The inverse matrix.
    :raises ZeroDivisionError: If the matrix is singular.
    """
    det = determinant3(m)
    if det == 0:
        raise ZeroDivisionError("Cannot invert singular matrix")
    adj = adjugate3(m)
    return [[adj[i][j] / det for j in range(3)] for i in range(3)]


def matmul3(a: Matrix, b: Matrix) -> Matrix:
    """Return the product of two 3x3 matrices.

    :param a: The left matrix.
    :param b: The right matrix.
    :return: ``a @ b``.
    """
    return [
        [a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j] for j in range(3)]
        for i in range(3)
    ]


def matvec3(m: Matrix, v: Vector) -> Vector:
    """Return the product of a 3x3 matrix and a 3-vector.

    :param m: The matrix.
    :param v: The vector.
    :return: ``m @ v``.
    """
    return [m[i][0] * v[0] + m[i][1] * v[1] + m[i][2] * v[2] for i in range(3)]
