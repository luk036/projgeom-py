=========
Changelog
=========

Version 0.3 (2026-11-20)
========================

Features
--------

- **Exact rational linear algebra**: Added ``rationalize()`` and
  ``from_fractions()``, plus internal 3x3 determinant/adjugate/inverse/product
  helpers over ``Fraction``, so conic and transform results are never truncated
  to ``int``. (#80a1ac7, #94b129c)
- **Exact conic and projective transforms**: ``Conic.polar``/``pole``/``intersect``
  and ``Transform.apply_point``/``apply_line``/``projective_transform`` now stay
  exact over the rationals; added ``rotation_from_tangent()``. (#8218800,
  #7da448f)
- **Fold trick-art generators**: Added anamorphic fold-a-ladder, fold-a-chair,
  fold-a-table and fold-a-house printables, plus fold-reveal/flat-screen/
  foldable-phone movies and the supporting single-module pipeline. (#2997cd1,
  #55da756, #c42447e, #723eba5, #6b7135c, #9b622af)

Bug Fixes
---------

- **Non-secant line/conic intersection**: ``intersect`` now returns an empty
  list instead of raising, matching the C++ and Rust ports. (#fb411a5)

Documentation
-------------

- **Papers, talks and reference bundle**: Added the projective-geometry paper
  and Beamer talk, the fold trick-art paper and reviewer response, reference
  PDFs, and a downloads checklist. (#729ff18, #d896f2c, #a068626, #d230d73,
  #13cd931, #9241345)
- **Anamorphosis session report** and printable/viewpoint SVGs. (#83df275,
  #3893b29, #05ccb44)

Version 0.2 (2026-10-09)
========================

Features
--------

- **7 new geometry modules**: Added ``euclid_object.py`` (``EuclidPoint``,
  ``EuclidLine``, ``midpoint``, ``orthocenter``, ...), ``proj_plane_measure.py``
  (cross-ratio ``R0``/``R1``/``R``/``ratio_ratio``/``x_ratio``),
  ``euclid_plane_measure.py`` (``quadrance``, ``spread``, ``cross_s``),
  ``conic.py`` (``Conic`` + ``ConicType``), ``transform.py`` (``Transform`` +
  free functions), ``error.py`` (9 exception classes), and ``geometry.py``
  (``Geometry`` ABC).
- **Variable-name alignment**: Aligned variable names with the Rust sibling
  project (``v_a``/``v_b``, ``lambda_val``/``mu_val``) and ck_plane line params
  (``ln_l``/``ln_m``). (#5d2b64b)

Bug Fixes
---------

- **mypy type errors**: Resolved covariance, annotation, and import type errors.
  (#a9e0b58)
- **Unused imports**: Removed unused imports across multiple modules. (#6e5cea6)
- **ruff warnings**: Added ``__all__`` to ``__init__.py`` and fixed ambiguous
  variable names (F401, F811, E741). (#f76daed)
- **flake8 E402**: Fixed E402 warnings and refactored ``projgeom`` code.
  (#8bd5fb3)
- **RTD docs build**: Added ``matplotlib`` and ``numpy`` to
  ``docs/requirements.txt``. (#d318cb1)

Testing & Code Quality
----------------------

- **Coverage raised 96% -> 99%**: Added ``pg_object`` edge-case coverage tests.
  (#5228eb9)
- **Edge-case tests + CI coverage**: Added edge-case unit tests and fixed the CI
  coverage run. (#8281f3b)
- **Cross-project verification**: ``tests/verify_consistency.py`` runs 30/30
  consistency checks; ``tests/bench_projgeom.py`` adds 21 pytest-benchmark
  functions with assertions. (#5d2b64b)

Code Cleanup
------------

- **Removed PyScaffold boilerplate**: Deleted ``skeleton.py``/``test_skeleton.py``,
  removed Python < 3.9 compat, dead entry points, stale ``IFLOW.md``, duplicate
  ``LICENSE``, and scrubbed config files. (#af50234)
- **Removed AI slop**: Stripped boilerplate from docstrings and comments.
  (#98f8181)
- **Style**: Formatted multi-line imports in ``verify_consistency.py`` and
  normalized example-plot line endings. (#128f271, #88c1d26)

Documentation
-------------

- **AGENTS.md**: Added agent guidelines for the repository. (#ff7d667)
- **Sphinx docs**: Enabled ``plot_directive`` and added projective-transformation
  and incidence example plots. (#e4f6760)

Build & CI
----------

- **GitHub Actions**: ``checkout``->v4, ``setup-python``->v5,
  ``codecov-action``->v4. (#1453fb8)
- **CI repair**: Fixed the broken ``entry_points`` configuration and remaining
  ``skeleton`` imports. (#8661634)

Version 0.1
===========

- Initial release.
