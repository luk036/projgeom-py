=========
Changelog
=========

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
