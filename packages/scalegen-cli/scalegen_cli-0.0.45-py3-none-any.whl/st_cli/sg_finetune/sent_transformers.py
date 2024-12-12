# Third-party modules
import click

# Product modules

from st_cli.stop import stop
from st_cli.view import view
from st_cli.launch import launch


@click.group(name="sent_transformers")
def sent_transformers():
    """
    Sentence transformers
    """
    pass


sent_transformers.add_command(stop, name="stop")
sent_transformers.add_command(view, name="view")
sent_transformers.add_command(launch, name="launch")
