# Third-party modules
import click

# Product modules

from st_cli.stop import stop
from st_cli.view import view
from st_cli.launch import launch


@click.group(name="seq2seq")
def seq2seq():
    """
    Sequence to sequence models
    """
    pass


seq2seq.add_command(stop, name="stop")
seq2seq.add_command(view, name="view")
seq2seq.add_command(launch, name="launch")
