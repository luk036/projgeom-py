"""
Projective Transformation
=========================

Visualization of a projective transformation mapping a square to a quadrilateral.
"""
import matplotlib.pyplot as plt
import numpy as np

# Original square
square = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])

# Projective transformation matrix (homography)
H = np.array([[1.0, 0.3, 0.1],
              [0.2, 1.0, 0.2],
              [0.1, 0.1, 1.0]])


def apply_homography(points, H):
    pts_h = np.column_stack([points, np.ones(len(points))])
    transformed = pts_h @ H.T
    transformed = transformed / transformed[:, 2:3]
    return transformed[:, :2]


transformed = apply_homography(square, H)

plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.fill(square[:, 0], square[:, 1], alpha=0.3, color='steelblue')
plt.plot(square[:, 0], square[:, 1], 'b-', linewidth=2)
plt.scatter(square[:-1, 0], square[:-1, 1], color='darkblue', s=50)
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.title('Original Square')
plt.grid(True, alpha=0.3)
plt.axis('equal')

plt.subplot(1, 2, 2)
plt.fill(transformed[:, 0], transformed[:, 1], alpha=0.3, color='lightcoral')
plt.plot(transformed[:, 0], transformed[:, 1], 'r-', linewidth=2)
plt.scatter(transformed[:-1, 0], transformed[:-1, 1], color='darkred', s=50)
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.title('Projectively Transformed')
plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.tight_layout()
