import time
import click
from rich import box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import os


from .const import SSH_KEY_PATH
from .client import send_request
from .datamodels.datamodels import WorkstationConfig
import yaml
from .utils import get_template


@click.group(name="ws", chain=True)
def ws():
    """
    Create/Delete a scaletorch workstation
    """
    pass


@ws.command("create")
@click.option("--gpus", type=click.STRING, required=False)
@click.option("--count", type=click.INT, required=False)
@click.option("--name", type=click.STRING, required=False)
@click.option("--num_workstations", type=click.INT, required=False)
@click.option("-c", "--config", type=click.STRING, required=False)
@click.option("-q", "--quiet", is_flag=True)
@click.option("-t", "--template", type=click.STRING, required=False)
def create(gpus, count, name, num_workstations, config, quiet, template):
    """Function to launch a workstation
    args:

    Returns:
    """
    if template:
        # Verify whether the template exists
        config_dict = get_template(template)
        if not config_dict:
            click.echo(
                click.style(
                    f"The template provided: {template} does not exist or is not a Workstation Template",
                    fg="red",
                ),
                err=True,
            )
            return

        config = WorkstationConfig(**config_dict)

    else:
        if not (all([gpus, count, name, num_workstations]) or config):
            click.echo(
                click.style(
                    f"Should provide (gpus, count, name, num_workstations) or a config file",
                    fg="red",
                ),
                err=True,
            )
            exit()

        if config:
            config_path = os.path.join(os.getcwd(), config)

            if not os.path.exists(config_path):
                click.echo(click.style(f"{config} file not found", fg="red"), err=True)
                exit()

            with open(config_path, "r") as fp:
                config_yaml = fp.read()
                dict_ = yaml.safe_load(config_yaml)
                try:
                    config = WorkstationConfig(**dict_)  # Valid config
                except Exception as e:
                    click.echo(
                        click.style(f"Validation Error: {e}", fg="red"), err=True
                    )
                    exit()

            if config.requirements:
                reqs_path = (
                    config.requirements
                    if not config.requirements.startswith("/")
                    else os.path.join(os.getcwd(), config.requirements)
                )
                if os.path.exists(reqs_path):
                    with open(reqs_path, "r") as fp:
                        config.requirements = fp.read()
                        # requirements = fp.read()
                # else:
                #     click.echo(click.style(f"Could not find {reqs_path}", fg="yellow"), err=True)
                #     exit()

        else:
            gpuTypes = gpus.split(",")
            gpuTypes = [gpu_type.strip() for gpu_type in gpuTypes]
            gpuCount = count
            config = WorkstationConfig(name=name, gpuTypes=gpuTypes, gpuCount=gpuCount, numWorkstations=num_workstations)  # type: ignore

    assert isinstance(config, WorkstationConfig)
    # print(config)
    # exit()
    resp = send_request("POST", "/workstation", data=config.model_dump(mode="json"))

    if resp.status_code == 201:
        names = resp.json()["message"]["ws_ids"]
        for name in names:
            click.echo(click.style(f"Creating new workstation: {name}", fg="green"))
    else:
        content = (
            resp.json() if resp.status_code != 500 else resp.content.decode("utf-8")
        )
        click.echo(
            click.style(f"Could not create workstation: {content}", fg="red"), err=True
        )


@ws.command("delete")
@click.argument("ws_id", type=click.STRING, required=True)
def delete(ws_id):

    resp = send_request("DELETE", f"/workstation/{ws_id}")
    if resp.status_code == 200:
        click.echo(click.style(f"Started deletion of workstation: {ws_id}", fg="green"))
    else:
        click.echo(
            click.style(f"Could not start deletion of workstation", fg="red"), err=True
        )


@ws.command("list")
@click.option("-a", "--all", is_flag=True)
def list_(all):

    resp = send_request("GET", f"/workstations")
    if resp.status_code == 200:
        table = Table(
            show_header=True,
            header_style="bold #2070b2",
            title="[bold] Workstations",
            box=box.DOUBLE_EDGE,
        )

        for col in ["ID", "Status", "Cost"]:
            table.add_column(col, justify="center")

        for ws_data in resp.json():
            if all or (not all and (ws_data["status"] in {"RUNNING", "QUEUED"})):
                table.add_row(
                    ws_data["id"],
                    ws_data["status"],
                    f"$ {round(float(ws_data['cost']), 3)}",
                )

            if ws_data["status"] in {"DELETED", "FAILED"} and os.path.exists(
                os.path.join(SSH_KEY_PATH, ws_data["id"])
            ):
                os.remove(os.path.join(SSH_KEY_PATH, ws_data["id"]))

        console = Console()
        console.print(table, justify="left")

    else:
        click.echo(click.style(f"Could not find any workstations", fg="red"), err=True)


@ws.command("view")
@click.argument("ws_id", type=click.STRING, required=True)
def view(ws_id):

    resp = send_request("GET", f"/workstation/{ws_id}")
    if resp.status_code != 200:
        click.echo(
            click.style(f"Could not find workstation: {ws_id}", fg="red"), err=True
        )
        return

    ws_data = resp.json()
    node = None
    if ws_data["nodes"]:
        running_vms = list(
            filter(
                lambda node: node["status"] == "RUNNING"
                and node["role"] == "WORKSTATION",
                ws_data["nodes"],
            )
        )
        if running_vms:
            node = running_vms.pop()
        else:
            node = None

    # Download the SSH Key to the user's machine
    if node and not os.path.exists(os.path.join(SSH_KEY_PATH, ws_id)):
        resp = send_request(
            "GET", f"/secret/INTERNAL_SSH_PRIVATE_KEY_{node['ssh_key_id']}"
        )
        if resp.status_code == 200:
            with open(os.path.join(SSH_KEY_PATH, ws_id), "w") as fp:
                fp.write(
                    resp.json()["secret"][
                        f'INTERNAL_SSH_PRIVATE_KEY_{node["ssh_key_id"]}'
                    ]
                )

    if ws_data["status"] in {"DELETED", "FAILED"} and os.path.exists(
        os.path.join(SSH_KEY_PATH, ws_data["id"])
    ):
        os.remove(os.path.join(SSH_KEY_PATH, ws_data["id"]))

    console = Console()
    markdown_content = (
        f"[bold][orange_red1]Id[/orange_red1] : [cyan]{ws_data['id']}[/cyan]\n"
    )
    viz_link = (
        "N/A"
        if ("viz_page" in ws_data and ws_data["viz_page"] == "")
        else ws_data["viz_page"]
    )
    markdown_content += (
        f"[orange_red1]Visualisation[/orange_red1] : [yellow]N/A[/yellow]\n"
    )
    markdown_content += (
        f"[orange_red1]Status[/orange_red1] : [yellow]{ws_data['status']}[/yellow]\n"
    )
    markdown_content += f"[orange_red1]Cost[/orange_red1] : [yellow]$ {round(ws_data['cost'], 3)}[/yellow]\n"

    if ws_data["status"] == "RUNNING" and node:
        markdown_content += f"[orange_red1]Jupyter Lab[/orange_red1] : [yellow]http://{node['ip']}:8888[/yellow]\n"
        markdown_content += f"[orange_red1]Jupyter Password[/orange_red1] : [yellow]{ws_data['id']}[/yellow]\n"
        ssh_content = f"""Run the following commands to SSH into workstation\n- chmod 400 {os.path.join(SSH_KEY_PATH, ws_id)}\n- sudo ssh -i {os.path.join(SSH_KEY_PATH, ws_id)} root@{node['ip']} -p 2222 """
        markdown_content += f"[yellow]{ssh_content}[/yellow]\n"

    console.print(Panel(markdown_content))


@ws.command("restart")
@click.argument("ws_id", type=click.STRING, required=True)
def restart(ws_id):
    """
    Restart a workstation that has either been stopped, deleted, crashed while running or pre-empted due to spot instance
    """
    resp = send_request("PUT", f"/workstation/{ws_id}?action=RESTART")
    if resp.status_code == 200:
        click.echo(click.style(f"Started restart of workstation: {ws_id}", fg="green"))
    else:
        click.echo(
            click.style(
                f"Could not restart workstation: {resp.content.decode('utf-8')}",
                fg="red",
            ),
            err=True,
        )


@ws.command("stop")
@click.argument("ws_id", type=click.STRING, required=True)
def stop(ws_id):
    """
    Stop a workstation that is running
    """
    resp = send_request("PUT", f"/workstation/{ws_id}?action=STOP")
    if resp.status_code == 200:
        click.echo(click.style(f"Stopping workstation: {ws_id}", fg="green"))
    else:
        click.echo(
            click.style(
                f"Could not stop workstation: {resp.content.decode('utf-8')}", fg="red"
            ),
            err=True,
        )
