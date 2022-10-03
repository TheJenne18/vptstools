[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![PyPI-Server](https://img.shields.io/pypi/v/vptstools.svg)](https://pypi.org/project/vptstools/)
[![.github/workflows/run_tests.yaml](https://github.com/enram/vptstools/actions/workflows/run_tests.yaml/badge.svg)](https://github.com/enram/vptstools/actions/workflows/run_tests.yaml)
# vptstools

Python tools to work with vertical profile time series.

## Installation

Python 3.9+ is required.

```
pip install vptstools
```

Included commands:

### vph5_to_vpts

Command-line tool to aggregate/convert a bunch of [ODIM hdf5 bird profiles](https://github.com/adokter/vol2bird/wiki/ODIM-bird-profile-format-specification) files (generated by [vol2bird](https://github.com/adokter/vol2bird)) to a single [vpts data package](https://github.com/enram/vpts-dp).

The first argument is the path to the input data (multiple `ODIM hdf5 profiles` files). This argument can be an absolute or relative path, possibly containing shell-style wildcards (full syntax: see [glob.glob()](https://docs.python.org/3/library/glob.html#glob.glob))

You may need to quote the argument so the wildcard arguments are passed as-is:

Examples:

```
$ vph5_to_vpts "/home/nnoe/denmark_vp_20131229/dkbor/*"
$ vph5_to_vpts "../../denmark_vp_20131229/*/dkbor_vp_*"
```

## Development instructions

See [contributing](docs/contributing.md) for a detailed overview and set of guidelines. If familiar with `tox`,
the setup of a development environment boils down to:

```
tox -e dev       # Create development environment with venv and register an ipykernel. Activate this environment to get started
source venv/bin/activate
```

Next, the following set of commands are available to support development:

```
tox              # Run the unit tests
tox -e docs      # Invoke sphinx-build to build the docs
tox -e format    # Run black code formatting

tox -e clean     # Remove old distribution files and temporary build artifacts (./build and ./dist)

tox -e doctests  # Invoke sphinx-build to run doctests
tox -e linkcheck # Check for broken links in the documentation

tox -e publish   # Publish the package you have been developing to a package index server. By default, it uses testpypi. If you really want to publish your package to be publicly accessible in PyPI, use the `-- --repository pypi` option.
tox -av  # to list all the tasks available
```

<!-- pyscaffold-notes -->
## Notes

- This project has been set up using PyScaffold 4.3.1. For details and usage information on PyScaffold see https://pyscaffold.org/.

- The `odimh5` module was originally developed and released to pypi as a separate [`odimh5`](https://pypi.org/project/odimh5/) package by Nicolas Noé ([@niconoe](https://github.com/niconoe)). Version 0.1.0 has been included into this vptstools package.