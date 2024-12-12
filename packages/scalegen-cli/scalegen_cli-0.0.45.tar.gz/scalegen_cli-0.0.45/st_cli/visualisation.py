import click

from .const import PRODUCT_TYPE
from .client import send_request


@click.group(name="vis", chain=True)
def vis():
    """
    Start / Stop visualisation server for a ScaleTorch job
    """
    pass


@vis.command("start")
@click.argument("job_id", type=click.STRING, required=True)
def start(job_id):
    resp = send_request("PUT", f"/job/{job_id}/visualisation?action=start")
    if resp.status_code == 200:
        click.echo(
            click.style(
                f"Visualization server is starting. Please run `{'scaletorch' if PRODUCT_TYPE=='SCALETORCH' else 'scalegen finetune'} view {job_id}` to view the visualisation server's URL.",
                fg="green",
            )
        )
    else:
        err = resp.json() if resp.status_code != 500 else resp.content.decode("utf-8")
        click.echo(
            click.style(
                f"Could not start visualisation server: {resp.json()}", fg="red"
            ),
            err=True,
        )


@vis.command("stop")
@click.argument("job_id", type=click.STRING, required=True)
def stop(job_id):
    resp = send_request("PUT", f"/job/{job_id}/visualisation?action=stop")
    if resp.status_code == 200:
        click.echo(click.style(f"Visualization server stopped", fg="green"))
    else:
        err = resp.json() if resp.status_code != 500 else resp.content.decode("utf-8")
        click.echo(
            click.style(
                f"Could not stop visualisation server: {resp.json()}", fg="red"
            ),
            err=True,
        )
