from .pg_object import PgObject


class EllPoint(PgObject):
    def dual(self) -> type:
        return EllLine

    def perp(self) -> "EllLine":
        """_summary_

        Returns:
            EllLine: _description_
        """
        return EllLine(self.coord)


class EllLine(PgObject):
    def dual(self) -> type:
        return EllPoint

    def perp(self) -> EllPoint:
        """_summary_

        Returns:
            EllPoint: _description_
        """
        return EllPoint(self.coord)
