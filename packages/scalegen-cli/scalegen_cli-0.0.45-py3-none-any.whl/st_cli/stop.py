import click
from rich.console import Console

from .client import send_request


@click.command()
@click.argument("job_id", type=click.STRING, required=True)
@click.option("-f", "--force", is_flag=True, help="Force stop the job")
# @click.argument("trial_id", type=click.STRING, required=False)
def stop(job_id: str, force: bool = False):
    """
    Stop a job
    """
    console = Console()
    # if not trial_id:
    with console.status("[bold green]Stopping job...") as _:
        resp = send_request("DELETE", f"/job/{job_id}", params={"force": force})

    if resp.status_code == 201:
        color = "green"
    else:
        color = "red"

    click.echo(click.style(f"{resp.json()['message']}", fg=color))
    return

    click.echo(
        click.style(f"\nSuccessfully requested to stop job: {job_id}", fg="green")
    )

    # else:
    #     resp = send_request('DELETE', f'/job/{job_id}/trial/{trial_id}')

    #     if resp.status_code != 202:
    #         click.echo(click.style("Couldn't find the requested trial", fg='red'))
    #         return

    #     click.echo(click.style(f"Stopping trial: {trial_id}", fg='blue'))
