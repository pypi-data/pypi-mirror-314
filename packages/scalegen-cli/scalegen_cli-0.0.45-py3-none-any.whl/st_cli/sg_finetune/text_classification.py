# Third-party modules
import click

# Product modules

from st_cli.stop import stop
from st_cli.view import view
from st_cli.launch import launch


@click.group(name="text_classification")
def text_classification():
    """
    Text classification
    """
    pass


text_classification.add_command(stop, name="stop")
text_classification.add_command(view, name="view")
text_classification.add_command(launch, name="launch")
