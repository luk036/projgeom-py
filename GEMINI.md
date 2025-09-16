# GEMINI.md

## Project Overview

This is a Python library for working with projective geometry. The project is set up using PyScaffold and provides a framework for defining and manipulating geometric objects like points and lines in a projective plane.

The core of the library is the `ProjectivePlane` abstract base class, located in `src/projgeom/pg_plane.py`. This class defines the fundamental operations and properties of objects in a projective plane. The library also includes implementations of various geometric theorems and concepts, such as Pappus's hexagon theorem and Desargues's theorem.

The project is well-tested and uses `pytest` for running tests and `tox` for managing test environments.

## Building and Running

The project uses `tox` to automate building, testing, and other development tasks.

### Key Commands:

*   **Run tests:**
    ```bash
    tox
    ```

*   **Build the package:**
    ```bash
    tox -e build
    ```

*   **Clean build artifacts:**
    ```bash
    tox -e clean
    ```

*   **Build documentation:**
    ```bash
    tox -e docs
    ```

## Development Conventions

*   **Coding Style:** The project uses `flake8` for code linting. The configuration can be found in the `.flake8` file.
*   **Testing:** Tests are located in the `tests/` directory and are written using `pytest`. The project also uses `hypothesis` for property-based testing.
*   **Continuous Integration:** The project uses GitHub Actions for CI. The workflows are defined in the `.github/workflows/` directory.
*   **Dependencies:** Project dependencies are managed in `setup.cfg`. Test-specific dependencies are listed under the `[options.extras_require]` section.
