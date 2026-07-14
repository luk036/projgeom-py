"""
Error types for geometric operations.

This module defines exceptions that can occur during geometric computations.
"""


class GeometryError(Exception):
    """Base exception for geometry-related errors."""


class OverflowError(GeometryError):
    """Raised when an arithmetic overflow occurs."""


class DivisionByZeroError(GeometryError):
    """Raised when a division by zero is attempted."""


class InvalidCoordinatesError(GeometryError):
    """Raised when homogeneous coordinates are all zero."""


class PointAtInfinityError(GeometryError):
    """Raised when a point at infinity is used where affine is required."""


class CoincidentPointsError(GeometryError):
    """Raised when points are coincident but must be distinct."""


class CoincidentLinesError(GeometryError):
    """Raised when lines are coincident but must be distinct."""


class NotCollinearError(GeometryError):
    """Raised when points must be collinear but are not."""


class InvalidTriangleError(GeometryError):
    """Raised when three points are collinear (degenerate triangle)."""
