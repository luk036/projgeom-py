Figures Demo
============

Auto-generated figures demonstrating projgeom-py functionality.

.. plot:: examples/plot_projective_transformation.py

.. plot:: examples/plot_incidence.py

The plot inline directive
-------------------------

.. plot::

   import matplotlib.pyplot as plt
   import numpy as np

   x = np.linspace(0, 2 * np.pi, 100)
   plt.plot(x, np.sin(x))
   plt.title("Simple Sine Wave")
   plt.grid(True, alpha=0.3)
