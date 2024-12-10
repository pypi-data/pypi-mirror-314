# Copyright ZettaBlock Labs 2024
import typer

from zetta._utils.async_utils import synchronizer
from zetta.cli.utils import list_databases_v2_from_neo, get_database_v2_from_neo

databasesv2_cli = typer.Typer(
    name="databasesv2",
    help="Manage your databases in Zetta AI Network v2.",
    no_args_is_help=True,
)


@databasesv2_cli.command(name="ls", help="list v2 databases")
@synchronizer.create_blocking
async def ls(database: str = typer.Option("",
                                          help="Name of database")):
    if database:
        get_database_v2_from_neo(database)
    else:
        list_databases_v2_from_neo()
