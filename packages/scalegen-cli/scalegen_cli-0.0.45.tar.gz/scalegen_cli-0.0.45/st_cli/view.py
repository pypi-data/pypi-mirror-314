import time
import click
from rich import box
from rich.live import Live
from rich.console import Console
from rich.panel import Panel
from rich.style import NULL_STYLE
from rich.table import Table
import json
import requests

from .client import send_request
from .utils import show_job_live_logs


@click.command()
@click.argument("job-id", type=click.STRING, required=True)
def view(job_id):
    """
    Check the status of the job
    """

    console = Console()
    with console.status("[bold green]Fetching job info...") as status:

        resp = send_request("GET", f"/job/{job_id}")
        if resp.status_code != 200:
            click.echo(click.style("Couldn't find the requested job", fg="red"))
            return
        job_data = resp.json()

        markdown_content = (
            f"[bold][orange_red1]ID[/orange_red1] : [cyan]{job_data['id']}[/cyan]\n"
        )
        markdown_content += (
            f"[orange_red1]Name[/orange_red1] : [yellow]{job_data['name']}[/yellow]\n"
        )
        markdown_content += f"[orange_red1]Status[/orange_red1] : [yellow]{job_data['status']}[/yellow]\n"
        markdown_content += f"[orange_red1]Cost[/orange_red1] : [yellow]$ {round(job_data['cost'], 3)}[/yellow]\n"

        # viz_link = 'N/A' if job_data['viz_page'] == '' else job_data['viz_page']
        # markdown_content += f"[orange_red1]Visualisation[/orange_red1] : [yellow]{viz_link}[/yellow]\n"

        console.print(Panel(markdown_content))

    # Trials
    resp = send_request("GET", f"/job/{job_id}/trials")
    if resp.status_code != 200:
        # click.echo(click.style("No trials running for this job", fg='blue'))
        return
    resp_data = resp.json()

    # Show live logs for simple jobs
    if job_data["spec"]["type"] in {"SIMPLE_JOB", "FINETUNING"}:
        if job_data["status"] not in {"QUEUED", "STOPPED"}:
            show_job_live_logs(job_id)
            return
        else:
            return

    # For experiments (Deprecated)
    table = Table(
        show_header=True,
        header_style="bold #2070b2",
        title=f"[bold] Trials",
        box=box.DOUBLE_EDGE,
    )

    for col in ["ID", "Status", "Hyperparameters", "Logs"]:
        table.add_column(col, justify="right")

    for trial in resp_data:
        if trial.get("is_dapp_trial", False):
            continue

        hpt = "N/A"
        if "hyperparameters" in trial:
            hpt = trial["hyperparameters"]["hyperParameters"]["value"]
            hpt = json.dumps(json.loads(hpt)["parameters"], indent=2)

        logs = "N/A"
        if job_data["status"] == "STOPPED":
            logs = "Please use the web app to download the logs"
        else:
            if "host" in trial and trial["host"]:
                logs = f"http://{trial['host']}:9000/logs/{job_id}/{trial['trial_id']}"

        table.add_row(trial["trial_id"], trial["status"], hpt, logs)

    console.print(table, justify="center")
