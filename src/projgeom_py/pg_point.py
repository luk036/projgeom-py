from .pg_object import PgObject


class PgPoint(PgObject):
    def dual(self) -> type:
        return PgLine


class PgLine(PgObject):
    def dual(self) -> type:
        return PgPoint
