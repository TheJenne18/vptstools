import glob
import sys

import click
from odimh5.reader import ODIMReader

# Return code (0 = success)
EXIT_INVALID_SOURCE_FILE = 1
EXIT_NO_SOURCE_DATA = 2


class InvalidSourceODIM(Exception):
    pass


def check_source_odim(source_odim: ODIMReader):
    if source_odim.root_object_str != 'VP':
        raise InvalidSourceODIM(f'Incorrect what.object value: expected VP, found {source_odim.root_object_str}')


@click.command()
@click.argument('ODIM_hdf5_profiles')
def cli(odim_hdf5_profiles):
    """This tool aggregate/convert a bunch of ODIM hdf5 profiles files to a single vpts data package"""
    # Open all ODIM files
    odims = [ODIMReader(path) for path in glob.glob(odim_hdf5_profiles, recursive=True)]

    if not odims:
        click.echo(f"No source data file found, is the supplied pattern ({odim_hdf5_profiles}) correct?")
        sys.exit(EXIT_NO_SOURCE_DATA)

    # Individual checks for each of them
    for source_odim in odims:
        try:
            check_source_odim(source_odim)
        except InvalidSourceODIM as e:
            click.echo(f"Invalid ODIM source file: {e}")
            sys.exit(EXIT_INVALID_SOURCE_FILE)

    click.echo("Toto")


if __name__ == '__main__':
    cli(["/Users/nicolas_noe/denmark_vp_20131229/dkbor_vp1_*"])
    #cli(['--help'])