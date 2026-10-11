"""
Geometric transformations.

This module provides transformation matrices for projective geometry,
including translation, rotation, scaling, shear, and composition.
"""

from fractions import Fraction
from typing import List

from ._linalg import inverse3, matmul3, matvec3
from .error import InvalidTriangleError
from .pg_object import PgLine, PgPoint, rationalize


class Transform:
    """A 3x3 projective transformation matrix.

    The matrix is stored in row-major order and operates on homogeneous
    coordinates (x:y:z).

    Examples:
        >>> from projgeom.transform import Transform
        >>> t = Transform.identity()
        >>> p = PgPoint([1, 2, 3])
        >>> t.apply_point(p) == p
        True
    """

    def __init__(self, matrix: List[List[Fraction]]):
        """Initialise the transform with a 3x3 matrix.

        :param matrix: A 3x3 matrix of :class:`Fraction` values.
        """
        self.matrix = matrix

    @staticmethod
    def identity() -> "Transform":
        r"""Create an identity transformation.

        .. math::

            I = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}

        :return: The identity transform.

        Examples:
            >>> from projgeom.transform import Transform
            >>> t = Transform.identity()
            >>> t.matrix[0][0] == Fraction(1, 1)
            True
        """
        return Transform(
            [
                [Fraction(1, 1), Fraction(0, 1), Fraction(0, 1)],
                [Fraction(0, 1), Fraction(1, 1), Fraction(0, 1)],
                [Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)],
            ]
        )

    @staticmethod
    def translation(tx: int, ty: int) -> "Transform":
        r"""Create a translation transformation.

        .. math::

            T(t_x, t_y) = \begin{bmatrix}
                1 & 0 & t_x \\
                0 & 1 & t_y \\
                0 & 0 & 1
            \end{bmatrix}

        :param tx: Translation in x.
        :param ty: Translation in y.
        :return: The translation transform.

        Examples:
            >>> from projgeom.transform import Transform
            >>> t = Transform.translation(5, 3)
            >>> t.apply_point(PgPoint([1, 2, 1]))
            PgPoint(6 : 5 : 1)
        """
        return Transform(
            [
                [Fraction(1, 1), Fraction(0, 1), Fraction(tx, 1)],
                [Fraction(0, 1), Fraction(1, 1), Fraction(ty, 1)],
                [Fraction(0, 1), Fraction(0, 1), Fraction(1, 1)],
            ]
        )

    @staticmethod
    def rotation(angle_cos: Fraction, angle_sin: Fraction) -> "Transform":
        r"""Create a rotation transformation.

        .. math::

            R(\theta) = \begin{bmatrix}
                \cos\theta & -\sin\theta & 0 \\
                \sin\theta &  \cos\theta & 0 \\
                0          &  0          & 1
            \end{bmatrix}

        :param angle_cos: Cosine of the rotation angle.
        :param angle_sin: Sine of the rotation angle.
        :return: The rotation transform.

        Examples:
            >>> from fractions import Fraction
            >>> from projgeom.transform import Transform
            >>> t = Transform.rotation(Fraction(0, 1), Fraction(1, 1))
            >>> t.apply_point(PgPoint([1, 0, 1]))
            PgPoint(0 : 1 : 1)
        """
        zero = Fraction(0, 1)
        return Transform(
            [
                [angle_cos, -angle_sin, zero],
                [angle_sin, angle_cos, zero],
                [zero, zero, Fraction(1, 1)],
            ]
        )

    @staticmethod
    def rotation_from_tangent(t: Fraction) -> "Transform":
        r"""Create a rotation from the tangent of its half-angle.

        For a rational :math:`t = \tan(\theta/2)` this yields an exact rotation
        through :math:`\theta` with rational entries:

        .. math::

            \cos\theta = \frac{1 - t^2}{1 + t^2}, \qquad
            \sin\theta = \frac{2 t}{1 + t^2}.

        :param t: The tangent of half the rotation angle.
        :return: The rotation transform.

        Examples:
            >>> from fractions import Fraction
            >>> from projgeom.transform import Transform
            >>> t = Transform.rotation_from_tangent(Fraction(1, 1))
            >>> t.apply_point(PgPoint([1, 0, 1]))
            PgPoint(0 : 1 : 1)
        """
        one = Fraction(1, 1)
        denom = one + t * t
        return Transform.rotation((one - t * t) / denom, (2 * t) / denom)

    @staticmethod
    def scaling(sx: Fraction, sy: Fraction) -> "Transform":
        r"""Create a scaling transformation.

        .. math::

            S(s_x, s_y) = \begin{bmatrix}
                s_x & 0   & 0 \\
                0   & s_y & 0 \\
                0   & 0   & 1
            \end{bmatrix}

        :param sx: Scale factor in x.
        :param sy: Scale factor in y.
        :return: The scaling transform.

        Examples:
            >>> from fractions import Fraction
            >>> from projgeom.transform import Transform
            >>> t = Transform.scaling(Fraction(2, 1), Fraction(3, 1))
            >>> t.apply_point(PgPoint([1, 2, 1]))
            PgPoint(2 : 6 : 1)
        """
        zero = Fraction(0, 1)
        return Transform(
            [
                [sx, zero, zero],
                [zero, sy, zero],
                [zero, zero, Fraction(1, 1)],
            ]
        )

    @staticmethod
    def shear(shx: Fraction, shy: Fraction) -> "Transform":
        r"""Create a shear transformation.

        .. math::

            H(sh_x, sh_y) = \begin{bmatrix}
                1 & sh_x & 0 \\
                sh_y & 1 & 0 \\
                0 & 0 & 1
            \end{bmatrix}

        :param shx: Shear factor in x.
        :param shy: Shear factor in y.
        :return: The shear transform.

        Examples:
            >>> from fractions import Fraction
            >>> from projgeom.transform import Transform
            >>> t = Transform.shear(Fraction(1, 1), Fraction(0, 1))
            >>> t.apply_point(PgPoint([1, 1, 1]))
            PgPoint(2 : 1 : 1)
        """
        zero = Fraction(0, 1)
        return Transform(
            [
                [Fraction(1, 1), shx, zero],
                [shy, Fraction(1, 1), zero],
                [zero, zero, Fraction(1, 1)],
            ]
        )

    def compose(self, other: "Transform") -> "Transform":
        r"""Compose this transformation with another.

        .. math::

            (M_{\text{result}})_{ij} = \sum_k (M_{\text{self}})_{ik} (M_{\text{other}})_{kj}

        :param other: The transform to apply after this one.
        :return: The composed transform.

        Examples:
            >>> from fractions import Fraction
            >>> from projgeom.transform import Transform
            >>> t1 = Transform.translation(2, 3)
            >>> t2 = Transform.scaling(Fraction(2, 1), Fraction(2, 1))
            >>> tc = t1.compose(t2)
            >>> tc.apply_point(PgPoint([1, 1, 1]))
            PgPoint(4 : 5 : 1)
        """
        result = [[Fraction(0, 1) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                s = Fraction(0, 1)
                for k in range(3):
                    s += self.matrix[i][k] * other.matrix[k][j]
                result[i][j] = s
        return Transform(result)

    def apply_point(self, point: PgPoint) -> PgPoint:
        r"""Apply the transformation to a point.

        .. math::

            p' = M p

        :param point: The point to transform.
        :return: The transformed point.

        Examples:
            >>> from projgeom.transform import Transform
            >>> t = Transform.translation(1, 1)
            >>> t.apply_point(PgPoint([1, 0, 1]))
            PgPoint(2 : 1 : 1)
        """
        x = Fraction(point.coord[0], 1)
        y = Fraction(point.coord[1], 1)
        z = Fraction(point.coord[2], 1)

        x_new = self.matrix[0][0] * x + self.matrix[0][1] * y + self.matrix[0][2] * z
        y_new = self.matrix[1][0] * x + self.matrix[1][1] * y + self.matrix[1][2] * z
        z_new = self.matrix[2][0] * x + self.matrix[2][1] * y + self.matrix[2][2] * z

        return PgPoint(rationalize([x_new, y_new, z_new]))

    def apply_line(self, line: PgLine) -> PgLine:
        r"""Apply the transformation to a line.

        Lines transform by the inverse transpose: :math:`l' = M^{-T} l`.

        :param line: The line to transform.
        :return: The transformed line.

        Examples:
            >>> from projgeom.transform import Transform
            >>> from projgeom.pg_object import PgLine
            >>> t = Transform.translation(1, 1)
            >>> line = PgLine([1, 0, 0])
            >>> tl = t.apply_line(line)
            >>> isinstance(tl, PgLine)
            True
        """
        inv = self.inverse()
        x = Fraction(line.coord[0], 1)
        y = Fraction(line.coord[1], 1)
        z = Fraction(line.coord[2], 1)

        x_new = inv.matrix[0][0] * x + inv.matrix[1][0] * y + inv.matrix[2][0] * z
        y_new = inv.matrix[0][1] * x + inv.matrix[1][1] * y + inv.matrix[2][1] * z
        z_new = inv.matrix[0][2] * x + inv.matrix[1][2] * y + inv.matrix[2][2] * z

        return PgLine(rationalize([x_new, y_new, z_new]))

    def inverse(self) -> "Transform":
        r"""Compute the inverse of this transformation.

        .. math::

            M^{-1} = \frac{\text{adj}(M)}{\det(M)}

        :return: The inverse transform.
        :raises ZeroDivisionError: If the matrix is singular.

        Examples:
            >>> from projgeom.transform import Transform
            >>> t = Transform.translation(5, 3)
            >>> inv = t.inverse()
            >>> p = PgPoint([1, 2, 1])
            >>> t.apply_point(p) == p
            False
            >>> inv.apply_point(t.apply_point(p)) == p
            True
        """
        a = self.matrix[0][0]
        b = self.matrix[0][1]
        c = self.matrix[0][2]
        d = self.matrix[1][0]
        e = self.matrix[1][1]
        f = self.matrix[1][2]
        g = self.matrix[2][0]
        h = self.matrix[2][1]
        i_val = self.matrix[2][2]

        det = a * (e * i_val - f * h) - b * (d * i_val - f * g) + c * (d * h - e * g)

        if det == Fraction(0, 1):
            raise ZeroDivisionError("Cannot invert singular matrix")

        inv_det = Fraction(1, 1) / det

        return Transform(
            [
                [
                    inv_det * (e * i_val - f * h),
                    inv_det * (c * h - b * i_val),
                    inv_det * (b * f - c * e),
                ],
                [
                    inv_det * (f * g - d * i_val),
                    inv_det * (a * i_val - c * g),
                    inv_det * (c * d - a * f),
                ],
                [
                    inv_det * (d * h - e * g),
                    inv_det * (b * g - a * h),
                    inv_det * (a * e - b * d),
                ],
            ]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transform):
            return NotImplemented
        return self.matrix == other.matrix


def rotate_point(point: PgPoint, angle_cos: Fraction, angle_sin: Fraction) -> PgPoint:
    r"""Rotate a point around the origin.

    .. math::

        p' = R(\theta)\, p

    :param point: The point to rotate.
    :param angle_cos: Cosine of the rotation angle.
    :param angle_sin: Sine of the rotation angle.
    :return: The rotated point.

    Examples:
        >>> from fractions import Fraction
        >>> from projgeom.transform import rotate_point
        >>> from projgeom.pg_object import PgPoint
        >>> p = rotate_point(PgPoint([1, 0, 1]), Fraction(0, 1), Fraction(1, 1))
        >>> p
        PgPoint(0 : 1 : 1)
    """
    t = Transform.rotation(angle_cos, angle_sin)
    return t.apply_point(point)


def translate_point(point: PgPoint, tx: int, ty: int) -> PgPoint:
    r"""Translate a point.

    .. math::

        p' = T(t_x, t_y)\, p

    :param point: The point to translate.
    :param tx: Translation in x.
    :param ty: Translation in y.
    :return: The translated point.

    Examples:
        >>> from projgeom.transform import translate_point
        >>> from projgeom.pg_object import PgPoint
        >>> translate_point(PgPoint([1, 2, 1]), 3, 4)
        PgPoint(4 : 6 : 1)
    """
    t = Transform.translation(tx, ty)
    return t.apply_point(point)


def scale_point(point: PgPoint, sx: Fraction, sy: Fraction) -> PgPoint:
    r"""Scale a point.

    .. math::

        p' = S(s_x, s_y)\, p

    :param point: The point to scale.
    :param sx: Scale factor in x.
    :param sy: Scale factor in y.
    :return: The scaled point.

    Examples:
        >>> from fractions import Fraction
        >>> from projgeom.transform import scale_point
        >>> from projgeom.pg_object import PgPoint
        >>> scale_point(PgPoint([2, 3, 1]), Fraction(2, 1), Fraction(3, 1))
        PgPoint(4 : 9 : 1)
    """
    t = Transform.scaling(sx, sy)
    return t.apply_point(point)


def projective_transform(src: List[PgPoint], dst: List[PgPoint]) -> Transform:
    r"""Compute the projective transformation mapping four points to four points.

    The correspondences are normalized against their unit point, so that the
    resulting transform satisfies :math:`M p_i \sim q_i`. The computation is
    exact over the rationals.

    :param src: Four source points, no three of which are collinear.
    :param dst: Four destination points, no three of which are collinear.
    :return: The transformation matrix.
    :raises ValueError: If the number of correspondences is not four.
    :raises InvalidTriangleError: If either set of points is degenerate.

    Examples:
        >>> from projgeom.pg_object import PgPoint
        >>> from projgeom.transform import projective_transform
        >>> src = [PgPoint([0, 0, 1]), PgPoint([1, 0, 1]), PgPoint([0, 1, 1]), PgPoint([1, 1, 1])]
        >>> dst = [PgPoint([0, 0, 1]), PgPoint([2, 0, 1]), PgPoint([0, 2, 1]), PgPoint([2, 2, 1])]
        >>> t = projective_transform(src, dst)
        >>> t.apply_point(PgPoint([1, 1, 1]))
        PgPoint(2 : 2 : 1)
    """
    if len(src) != 4 or len(dst) != 4:
        raise ValueError("projective_transform requires four point correspondences")

    def support_matrix(points: List[PgPoint]) -> List[List[Fraction]]:
        return [[Fraction(points[j].coord[i], 1) for j in range(3)] for i in range(3)]

    src_matrix = support_matrix(src)
    dst_matrix = support_matrix(dst)
    try:
        src_inverse = inverse3(src_matrix)
        dst_inverse = inverse3(dst_matrix)
    except ZeroDivisionError as exc:
        raise InvalidTriangleError("the support points are collinear") from exc

    src_basis = matvec3(src_inverse, [Fraction(value, 1) for value in src[3].coord])
    dst_basis = matvec3(dst_inverse, [Fraction(value, 1) for value in dst[3].coord])
    diagonal = [[Fraction(0, 1) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        if src_basis[i] == 0 or dst_basis[i] == 0:
            raise InvalidTriangleError(
                "the correspondences are not in general position"
            )
        diagonal[i][i] = dst_basis[i] / src_basis[i]

    return Transform(matmul3(matmul3(dst_matrix, diagonal), src_inverse))
