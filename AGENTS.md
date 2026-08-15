# AGENTS.md - Agent Guidelines for projgeom-py

## Build/Lint/Test Commands

### Testing
```bash
# Run all tests
pytest
# Or via tox
tox

# Run single test file
pytest tests/test_pg_object.py

# Run specific test function
pytest tests/test_pg_object.py::test_pg_point_meet

# Run doctests in source modules + coverage (CI uses this)
pytest tests/ --doctest-modules src/ --cov=src/

# Property-based tests with hypothesis
pytest tests/test_pg_plane_hypothesis.py
```

### Linting & Formatting
```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Individual tools
black src/projgeom tests/    # Format code (line length 256)
isort src/projgeom tests/    # Sort imports (Black profile)
flake8 src/projgeom tests/   # Lint (max_line_length=256)
mypy src/                    # Type check (Python 3.12 target)
```

### Build
```bash
tox -e build                  # Build sdist + wheel
tox -e clean                  # Remove build artifacts
```

### Docs
```bash
tox -e docs                   # Build HTML docs
tox -e doctests               # Run doctests via sphinx
tox -e linkcheck              # Check for broken links
```

## Code Style Guidelines

### Project Structure
- Source: `src/projgeom/` (namespace package) with one module per geometry domain
- Tests: `tests/` with plain pytest tests plus `test_*_hypothesis.py` property tests
- Version managed via setuptools_scm (version_scheme=no-guess-dev)

### Naming Conventions
- **Classes**: PascalCase (e.g., `PgObject`, `PgPoint`, `PgLine`, `Transform`, `Conic`)
- **Functions/Methods**: snake_case (e.g., `dot`, `cross`, `cross0`, `check_axiom`, `harm_conj`)
- **Type variables**: PascalCase (e.g., `Dual`)
- **Type aliases**: `Value` for the field type used in coordinates

### Type Hints
- **Required**: All functions and methods must have type hints
- Use `typing` modern features: `Self`, `TypeVar`, `Type`, `cast`
  ```python
  from typing import List, Self, Type, TypeVar, cast

  Dual = TypeVar("Dual", bound="PgObject")  # type: ignore[type-arg]
  ```
- Exact arithmetic uses `Fraction` (e.g., in `transform.py` matrices)

### Docstrings
- **Style**: reStructuredText with Napoleon-style Google/NumPy sections, `:param:`, `:return:`
- **Math**: Use `.. math::` directives for formulas in reST docstrings
- **Examples**: Include `Examples:` with `>>>` doctest lines
- **Module docs**: Start with `"""` explaining the module's purpose

### Imports
- **Order**: stdlib → third-party → local (isort with Black profile)
- Local imports use relative form: `from .pg_plane import ProjectivePlane, Value`
- Sub-modules re-exported from `__init__.py` with `__all__`

### Error Handling
- **Custom exception hierarchy** in `error.py`, all subclassing `GeometryError`:
  - `OverflowError`, `DivisionByZeroError`, `InvalidCoordinatesError`
  - `PointAtInfinityError`, `CoincidentPointsError`, `CoincidentLinesError`
  - `NotCollinearError`, `InvalidTriangleError`
- Raise `ValueError` for invalid coordinate input

### Testing Patterns
- **Framework**: pytest with doctest support, coverage required
- **Property-based testing**: hypothesis for algebraic identities in `test_*_hypothesis.py`
- Plain `assert` statements in tests, `test_` prefix with `-> None` return type
- Docstring `>>>` examples are verified via `--doctest-modules`

### Python Version
- CI targets Python 3.11 (python-app) and 3.11/3.13 (ci.yml, multi-platforms)
- mypy configured for Python 3.12
- `python_requires` >= 3.11 (importlib-metadata only for <3.11)

### Pre-commit Hooks (Active)
- trailing-whitespace
- check-added-large-files
- check-ast
- check-json / check-yaml / check-xml
- check-merge-conflict
- debug-statements
- end-of-file-fixer
- requirements-txt-fixer
- mixed-line-ending (auto-fix)
- isort
- black
- flake8

### Configuration Files
- `setup.cfg`: Package metadata, pytest options, flake8 (max_line_length=256)
- `.flake8`: Formatting rules disabled (extends setup.cfg)
- `pyproject.toml`: Build system (setuptools_scm)
- `tox.ini`: Test environments (default, build, clean, docs, doctests, linkcheck, publish)
- `.isort.cfg`: Import sorting (Black profile, known_first_party=projgeom)
- `mypy.ini`: Type checking (Python 3.12, ignores for matplotlib/hypothesis)
- `.coveragerc`: Coverage reporting (branch coverage, excludes repr/debug/asserts)

## Key Project Context

projgeom-py implements projective geometry in Python:
- **Core objects**: Points and lines in homogeneous coordinates (`PgObject`, `PgPoint`, `PgLine`) with duality (`aux`), dot/cross products for incidence and meets
- **Geometry models**: Euclidean (`euclid_object`, `euclid_plane_measure`), Cayley-Klein (`ck_plane`, `myck_object`), elliptic (`ell_object`), hyperbolic (`hyp_object`), and perspective (`persp_object`) planes
- **Plane-level operations**: Desargues/Pappus checks, harmonic conjugates, involutions, cross-ratio (`R`, `R0`, `R1`), projective transforms
- **Key dependencies**: `typing_extensions` (runtime dep); `hypothesis` and `matplotlib` only for testing/debugging
