"""
Perspective geometry objects (PerspPoint, PerspLine).

This module defines points and lines in a perspective (affine) plane,
including the line at infinity and midpoint calculation.
"""

from .pg_object import PgObject


class PerspPoint(PgObject["PerspLine"]):
    """A point in a perspective plane.

    The PerspPoint class represents a point in a perspective plane and provides methods for calculating
    the polar line and midpoint.

    .. svgbob::
       :align: center

          / \\
         /   \\
        /-----\\
        \\-----/
         \\   /
          \\ /
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (PerspLine for PerspPoint).

        :return: The type of the dual geometric object.

        Examples:
            >>> from projgeom.persp_object import PerspPoint
            >>> pt = PerspPoint([1, 2, 3])
            >>> pt.dual_type()
            <class 'projgeom.persp_object.PerspLine'>
        """
        return PerspLine

    def perp(self) -> "PerspLine":
        """Polar line.

        Returns the line at infinity as the polar for any point in a perspective plane.
        Note: This represents the polar operation in projective geometry, not perpendicular.

        :return: The PerspLine representing the line at infinity.

        Examples:
            >>> from projgeom.persp_object import PerspPoint
            >>> p = PerspPoint([1, 2, 3])
            >>> p.perp()
            PerspLine(0 : -1 : 1)
        """
        return self.polar()

    def polar(self) -> "PerspLine":
        r"""Polar line of a point in a perspective (affine) plane.

        All points share the same polar — the line at infinity
        :math:`\mathbf{L}_\infty = (0:-1:1)`:

        .. math::

           \text{polar}(P) = \mathbf{L}_\infty \quad \forall P

        This reflects the degenerate absolute conic of affine geometry.

        :return: The :class:`PerspLine` representing the line at infinity.

        Examples:
            >>> from projgeom.persp_object import PerspPoint
            >>> p = PerspPoint([1, 2, 3])
            >>> p.polar()
            PerspLine(0 : -1 : 1)
        """
        return L_INF

    def midpoint(self, other: "PerspPoint") -> "PerspPoint":
        r"""Midpoint of two points in a perspective (affine) plane.

        The midpoint :math:`M` of :math:`P` and :math:`Q` is the harmonic
        conjugate of the point at infinity on the line :math:`PQ`:

        .. math::

           \alpha &= \mathbf{L}_\infty \cdot Q \\[4pt]
           \beta &= \mathbf{L}_\infty \cdot P \\[4pt]
           M &= P \cdot \alpha + Q \cdot \beta

        :param other: Other point :math:`Q`
        :return: The midpoint :math:`M`

        Examples:
            >>> from projgeom.persp_object import PerspPoint
            >>> p1 = PerspPoint([1, 2, 3])
            >>> p2 = PerspPoint([4, 5, 6])
            >>> p1.midpoint(p2)
            PerspPoint(5 : 7 : 9)
        """
        alpha = L_INF.dot(other)
        beta = L_INF.dot(self)
        return self.parametrize(alpha, other, beta)


class PerspLine(PgObject[PerspPoint]):
    """A line in a perspective plane.

    The PerspLine class represents a line in a perspective plane and provides methods for calculating
    the pole, as well as checking if two lines are parallel.

    .. svgbob::
       :align: center

          / \\
         /   \\
        /-----\\
        \\-----/
         \\   /
          \\ /
    """

    def dual_type(self) -> type:
        """Returns the type of the dual object (PerspPoint for PerspLine).

        :return: The type of the dual geometric object.

        Examples:
            >>> from projgeom.persp_object import PerspLine
            >>> ln = PerspLine([1, 2, 3])
            >>> ln.dual_type()
            <class 'projgeom.persp_object.PerspPoint'>
        """
        return PerspPoint

    def perp(self) -> PerspPoint:
        """Pole of the line.

        Returns the pole (dual point) for any line in a perspective plane.
        Note: This represents the pole operation in projective geometry, not perpendicular.

        :return: The PerspPoint representing the pole.

        Examples:
            >>> from projgeom.persp_object import PerspLine
            >>> l = PerspLine([1, 2, 3])
            >>> l.perp()
            PerspPoint(1 : 5 : 5)
        """
        return self.pole()

    def pole(self) -> PerspPoint:
        r"""Pole of a line in a perspective (affine) plane.

        The pole is obtained by parametrising the isotropic points
        :math:`\mathbf{I}_{\text{Re}} = (0:1:1)` and
        :math:`\mathbf{I}_{\text{Im}} = (1:0:0)`:

        .. math::

           \alpha &= \mathbf{I}_{\text{Re}} \cdot \mathbf{l} \\[4pt]
           \beta &= \mathbf{I}_{\text{Im}} \cdot \mathbf{l} \\[4pt]
           \text{pole}(\mathbf{l}) &=
           \alpha\,\mathbf{I}_{\text{Re}} + \beta\,\mathbf{I}_{\text{Im}}

        :return: A :class:`PerspPoint` object.
        """
        alpha = I_RE.dot(self)
        beta = I_IM.dot(self)
        return I_RE.parametrize(alpha, I_IM, beta)

    def is_parallel(self, other: "PerspLine") -> bool:
        """
        The function checks if two lines are parallel by calculating the dot product of their direction
        vectors.

        :param other: The "other" parameter is an object of the same class as the current object. It represents another instance of the class that we want to check for parallelism with the current object
        :type other: "PerspLine"
        :return: a boolean value, indicating whether the two objects are parallel or not.

        Examples:
            >>> from projgeom.persp_object import PerspLine
            >>> l1 = PerspLine([1, 2, 3])
            >>> l2 = PerspLine([1, 2, 4])
            >>> l1.is_parallel(l2)
            False
        """
        return L_INF.dot(self.meet(other)) == 0


I_RE = PerspPoint([0, 1, 1])
I_IM = PerspPoint([1, 0, 0])
L_INF = PerspLine([0, -1, 1])
