# PyPackIT-Test1 © 2024 Armin Ariamajd
# SPDX-License-Identifier: MIT

"""PyPackIT Test1: A New Python Project.

Welcome to PyPackIT Test1 powered by <a href="https://pypackit.repodynamics.com/">PyPackIT</a>.
Replace this text with a short abstract of PyPackIT Test1, describing its purpose and main features.
By default, this text is displayed on the repository's main README file, on the homepage of the
project's website, on the project's PyPI and TestPyPI pages, and on the package's main docstring.
Like all other entries in the repository's control center, this text can also contain dynamic
references to other entries, using the <code>${‎{ json-path.to.value }}$</code> syntax. By default,
the first occurrence of the name of the project in this text is styled as strong and linked to the
project's website.
"""

from pypackit_test1 import data

__all__ = ["data", "__version_details__", "__version__"]

__version_details__: dict[str, str] = { "version": "0.0.10", "build_date": "2024.12.08", "committer_date": "2024.12.08", "author_date": "2024.12.08", "branch": "main", "distance": "0", "commit_hash": "66b24fed3e0fff73c622de5e230a7802b614b592" }
"""Details of the currently installed version of the package,
including version number, date, branch, and commit hash."""

__version__: str = __version_details__["version"]
"""Version number of the currently installed package."""
