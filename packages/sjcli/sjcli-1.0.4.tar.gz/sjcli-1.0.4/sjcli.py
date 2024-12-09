import crud
import click

from utils import utils
from clarity import clarity

@click.group()
@click.version_option()
def cli():
    """The CLI utility
    
    Author: Saurabh Jain <jpr.saurabh@gmail.com>
    """

    # output=click.prompt("Enter Output Directory (without quotes)",type=click.Path(exists=True,dir_okay=True,file_okay=False,writable=True,resolve_path=True))
    # click.echo(ctx.command)
    # ctx.obj={"output_dir":output}
    # click.echo(output)
# These are available commands in sjcli
cli.add_command(clarity)
cli.add_command(utils)

# TODO
# cli.add_command(search)