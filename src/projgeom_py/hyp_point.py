from .pg_object import PgObject


class HypPoint(PgObject):
    def dual(self) -> type:
        return HypLine

    def perp(self):
        """_summary_

        Returns:
            HypLine: _description_
        """
        return HypLine([self.coord[0], self.coord[1], -self.coord[2]])


class HypLine(PgObject):
    def dual(self) -> type:
        return HypPoint

    def perp(self) -> HypPoint:
        """_summary_

        Returns:
            HypPoint: _description_
        """
        return HypPoint([self.coord[0], self.coord[1], -self.coord[2]])
