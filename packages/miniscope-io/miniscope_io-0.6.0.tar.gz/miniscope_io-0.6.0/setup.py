import os
import sys
import warnings

from setuptools import setup


error_message = "\n".join(
    [
        "`miniscope-io` is now `mio`!",
        "Replace all imports and installs of `miniscope-io` with `mio` :)",
        "",
        "See: https://pypi.org/project/mio/",
    ]
)


def likely_error():

    raise SystemExit(error_message)


if __name__ == "__main__":
    # We allow python setup.py sdist to always work to be able to create the
    # sdist and upload it to PyPI
    sdist_mode = len(sys.argv) == 2 and sys.argv[1] == "sdist"

    if not sdist_mode:
        likely_error()

    setup(
        description="miniscope-io is now mio!",
        long_description=error_message,
        long_description_content_type="text/markdown",
        name="miniscope-io",
        version="0.6.0",
    )
