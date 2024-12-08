"""Read the latest Real Python tutorials.

Usage:
------

    $ realpython [options] [id] [id ...]

List the latest tutorials:

    $ realpython

Read one tutorial:

    $ realpython <id>

    where <id> is the number shown when listing tutorials.

Read the latest tutorial:

    $ realpython 0


Available options are:

    -h, --help         Show this help
    -l, --show-links   Show links in text


Contact:
--------

- https://realpython.com/contact/

More information is available at:

- https://pypi.org/project/realpython-reader/
- https://github.com/realpython/reader


Version:
--------

- realpython-reader v1.1.4
"""
# Standard library imports
import sys

# Reader imports
import objexp
from objexp import ox


def main() -> None:
    """Read the Real Python article feed."""
    ox()

if __name__ == "__main__":
    main()
