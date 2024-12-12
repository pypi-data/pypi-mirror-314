import click
from rich import box
from rich.console import Console
from rich.table import Table

from .client import send_request


@click.command()
@click.option("-a", "--all", is_flag=True)
def list(all):
    """
    List all jobs
    """
    """
    - Status of the Workload
    - Status of the trials:
        - Trial Name
        - Trial latest metrics
        - Trial Status
    """
    console = Console()

    with console.status("[bold green]Fetching jobs...") as status:
        resp = send_request("GET", f"/job")

        if resp.status_code == 204:
            click.echo(click.style(f"\nNo jobs found", fg="red"))
            return
        elif resp.status_code != 200:
            err = (
                resp.json() if resp.status_code != 500 else resp.content.decode("utf-8")
            )
            click.echo(click.style(f"\nCouldn't list the jobs: {err}", fg="red"))
            return

        resp_data = resp.json()

        table = Table(
            show_header=True,
            header_style="bold #2070b2",
            title="[bold] Jobs",
            box=box.DOUBLE_EDGE,
        )

        for col in ["ID", "Name", "Status"]:
            table.add_column(col)

        for job in resp_data:
            if all or (
                not all and (job["status"] == "RUNNING" or job["status"] == "QUEUED")
            ):
                table.add_row(job["id"], job["name"], job["status"])

    if table.row_count <= 15:
        console.print(table, justify="left")
    else:
        with console.pager():
            console.print(table, justify="left")
