import click
from .parsers import parse_app_access
from utils import get_timestamp_stats_from_csv


__all__=[
    "parse_app_access"
]

@click.command(name="parse-app")
@click.argument("filename",type=click.Path(exists=True))
@click.argument("output",type=click.Path(exists=True,file_okay=False))
@click.option(
    "-p",
    "--prefix",
    default="app-access",
    help="The file prefix to search if the filename is path to directory"
)
@click.option(
    "-i",
    "--ignore",
    default=".csv",
    help="The file extension to be ignore while searching directory matching criteria defined in 'prefix'"
)
def parse(filename:str,output:str,prefix:str, ignore:str):
    """Parse the app-access file/ files into csv.
    It removes all the lines which are without any HTTP operations
    
    filename: Path to app-access.*.log or directory containing app-access.*.log.
    output: Path to the output directory.
    prefix: File prefix to search in directory. Example app-access
    ignore: The extension to ignore. Example .csv
    """
    parse_app_access(filepath=filename,output_dir=output,file_prefix=prefix,ignore_extension=ignore)

@click.argument("input_dir",type=click.Path(exists=True,file_okay=False))
@click.argument("output_dir",type=click.Path(exists=True,file_okay=False))
@click.argument("dateindex",type=int)
@click.option(
    "-f",
    "--filename",
    default="datetime_stats.csv",
    help="The output file to be created, default=datetime_stats.csv"
)
@click.option(
    "-p",
    "--prefix",
    default="app-access",
    help="File prefix determines which files will be parse to gather DateTime stats, default app-access"
)
@click.option(
    "-i",
    "--ignore",
    default=".log",
    help="The file extension to be ignore while searching directory matching criteria defined in 'prefix', default=.log"
)
@click.command(name="datetime")
def sessions(input_dir:str,output_dir:str,dateindex:int,filename:str,prefix:str,ignore:str):
    """Get date-time details from all csv file parsed by 'parse-app'
    """
    get_timestamp_stats_from_csv(input_dir=input_dir,date_col_index=dateindex,output_dir=output_dir,output_file=filename,file_prefix=prefix,ignore_extension=ignore)

@click.group
def clarity()->None:
    """ Clarity CLI commands
    
    """

clarity.add_command(parse)
clarity.add_command(sessions)