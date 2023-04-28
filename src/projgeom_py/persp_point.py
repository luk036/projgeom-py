from .pg_object import PgObject
from typing_extensions import Self


class PerspPoint(PgObject["PerspLine"]):
    def dual(self) -> type:
        return PerspLine

    def perp(self) -> "PerspLine":
        """_summary_

        Returns:
            PerspLine: _description_
        """
        return L_INF

    def midpoint(self, other: Self) -> Self:
        """_summary_

        Returns:
            PerspPoint: _description_
        """
        alpha = L_INF.dot(other)
        beta = L_INF.dot(self)
        return self.plucker(alpha, other, beta)


class PerspLine(PgObject[PerspPoint]):
    def dual(self) -> type:
        return PerspPoint

    def perp(self) -> PerspPoint:
        """_summary_

        Returns:
            PerspPoint: _description_
        """
        alpha = I_RE.dot(self)
        beta = I_IM.dot(self)
        return I_RE.plucker(alpha, I_IM, beta)

    def is_parallel(self, other: Self) -> bool:
        return L_INF.dot(self.circ(other)) == 0


I_RE = PerspPoint([0, 1, 1])
I_IM = PerspPoint([1, 0, 0])
L_INF = PerspLine([0, -1, 1])
