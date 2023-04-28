from .pg_object import PgObject


class PgPoint(PgObject["PgLine"]):
    def dual(self) -> type:
        return PgLine


class PgLine(PgObject[PgPoint]):
    def dual(self) -> type:
        return PgPoint
