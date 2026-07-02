"""
Incidence in Projective Geometry
=================================

Visualizes a point and a line in the projective plane, showing
the incidence relationship.
"""
import matplotlib.pyplot as plt
import numpy as np

# Line: ax + by + c = 0 -> line = [a, b, c]
line = np.array([1.0, 2.0, -3.0])

# Point on the line (satisfies dot product = 0)
point = np.array([1.0, 1.0, 1.0])

x_vals = np.linspace(-2, 4, 100)
# ax + by + c = 0 => y = (-ax - c) / b
y_vals = (-line[0] * x_vals - line[2]) / line[1]

plt.figure(figsize=(7, 6))
plt.plot(x_vals, y_vals, "b-", linewidth=2, label="Projective Line")
plt.scatter(
    [point[0] / point[2]],
    [point[1] / point[2]],
    color="red",
    s=100,
    zorder=5,
    label="Incident Point",
)
plt.axhline(0, color="gray", linewidth=0.5)
plt.axvline(0, color="gray", linewidth=0.5)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Point-Line Incidence in Projective Plane")
plt.legend()
plt.grid(True, alpha=0.3)
plt.axis("equal")
