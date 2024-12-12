# Third-party modules
import click

# Product modules

from st_cli.stop import stop
from st_cli.view import view
from st_cli.launch import launch


@click.group(name="token_classification")
def token_classification():
    """
    Token classification
    """
    pass


token_classification.add_command(stop, name="stop")
token_classification.add_command(view, name="view")
token_classification.add_command(launch, name="launch")
