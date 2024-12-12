import click

from .const import PRODUCT_TYPE
from .login import login
from .launch import launch
from .view import view
from .stop import stop
from .list import list
from .job import job
from .sg_inference import infer
from .sg_finetune import finetune
from .gpu_machines import gpu_machines

# from .workstation import ws
# from .visualisation import vis


@click.group()
def cli():
    pass


# Common commands
cli.add_command(login)

if PRODUCT_TYPE == "SCALEGEN":
    cli.add_command(infer, name="infer")
    cli.add_command(finetune, name="finetune")
    cli.add_command(gpu_machines, name="gpu_machines")
else:
    cli.add_command(launch)
    cli.add_command(view)
    cli.add_command(stop)
    cli.add_command(list)
    cli.add_command(job, name="job")

if __name__ == "__main__":
    cli()
