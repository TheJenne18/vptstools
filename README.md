# vptstools

[![.github/workflows/run_tests.yaml](https://github.com/enram/vptstools/actions/workflows/run_tests.yaml/badge.svg)](https://github.com/enram/vptstools/actions/workflows/run_tests.yaml)

Python tools to work with vertical profile time series.

Status: WIP, not functional yet

## Installation

Python 3.7+ is required.

```
$ pip install vptstools
```

Included commands:

## vph5_to_vpts

Command-line tool to aggregate/convert a bunch of `ODIM hdf5 profiles` files (generated by [vol2bird](https://github.com/adokter/vol2bird)) to a single [vpts data package](https://github.com/enram/vpts).

The first argument is the path to the input data (multiple `ODIM hdf5 profiles` files). This argument can be an absolute or relative path, possibly containing shell-style wildcards (full syntax: see [glob.glob()](https://docs.python.org/3/library/glob.html#glob.glob))

You may need to quote the argument so the wildcard arguments are passed as-is:

Examples:

```
$ vph5_to_vpts "/home/nnoe/denmark_vp_20131229/dkbor/*"
$ vph5_to_vpts "../../denmark_vp_20131229/*/dkbor_vp_*"
```
