from .pg_object import PgObject


class PgPoint(PgObject["PgLine"]):
    """_summary_

    Args:
        PgObject (_type_): _description_
    """

    def dual(self) -> type:
        """_summary_

        Returns:
            type: _description_
        """
        return PgLine


class PgLine(PgObject[PgPoint]):
    def dual(self) -> type:
        return PgPoint
