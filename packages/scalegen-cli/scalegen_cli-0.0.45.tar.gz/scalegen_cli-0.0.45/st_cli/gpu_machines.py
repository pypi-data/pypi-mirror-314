from typing import Any, Dict, List, Optional
import os
import sys
import click
from rich import box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .client import send_request


@click.group(name="gpu_machines")
def gpu_machines():
    """
    ScaleGen commands for managing fine-tuning deployments
    """
    pass


def get_available_machines(
    gpu_type: Optional[str], num_gpus: Optional[int]
) -> Optional[List[Dict[str, Any]]]:
    response = send_request(
        "GET",
        "/gpu_machines/list_available",
        params={
            "gpu_type": gpu_type,
            "num_gpus": num_gpus or 1 if gpu_type else num_gpus,
        },
    )
    if response.status_code not in {200, 404}:
        click.echo(f"Error: {response.content.decode('utf-8')}")
        return
    return response.json()


@gpu_machines.command(name="list")
def list_gpu_machines():
    """
    List all GPU machines

    """
    console = Console()
    with console.status("[bold green]Fetching list...") as _:
        try:
            response = send_request("GET", "/gpu_machines/list")
        except:
            click.echo(click.style(f"\nUnable to fetch...", fg="red"))
        gpu_machines = response.json()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Machine ID")
        table.add_column("GPU Type x Count")
        table.add_column("Status")
        table.add_column("Region")

        for gpu_machine in gpu_machines:
            table.add_row(
                gpu_machine["id"],
                f'{gpu_machine["instance_details"]["gpu_type"]} x {gpu_machine["instance_details"]["gpu_count"]}',
                gpu_machine["status"],
                gpu_machine["instance_details"]["region"],
            )
        console.print(table)


@gpu_machines.command(name="view")
@click.argument("gpu_machine_id", type=click.STRING)
def view_gpu_machine(gpu_machine_id: str):
    """
    View a GPU machine
    """
    # Fetch data from the API
    console = Console()
    payload = {"gpu_machine_id": gpu_machine_id}
    with console.status("[bold green]Fetching data...") as _:
        response = send_request("GET", "/gpu_machines/get", params=payload)

    if response.status_code == 200:
        response = response.json()
        pass
    else:
        click.echo(click.style(f"\nUnable to fetch...", fg="red"))
        sys.exit()

    # Download SSH Key

    gpu_details = send_request(
        "GET", "/gpu_machines/gpu_nodes", params={"gpu_mach_id": gpu_machine_id}
    )

    gpu_details = gpu_details.json()[0]

    ssh_key_id = gpu_details["ssh_key_id"]
    username = gpu_details["username"]
    ip = gpu_details["ip"]
    metadata = gpu_details["metadata"]

    path = os.path.expanduser("~/.scalegen")
    os.makedirs(path, exist_ok=True)
    file_path = f"{ssh_key_id}_id_rsa"
    file_path = os.path.join(path, file_path)

    endpoint = f"INTERNAL_SSH_PRIVATE_KEY_{ssh_key_id}"
    ssh_response = send_request("GET", f"/secret/{endpoint}")
    if ssh_response.status_code != 200:
        raise Exception(
            f"Couldn't make request call, Exception : {ssh_response.content.decode('utf-8')} "
        )

    private_key = ssh_response.json()["secret"][endpoint]

    with open(file_path, "w") as ssh_file:
        ssh_file.write(private_key)

    # Change permissions
    os.chmod(file_path, 0o600)

    markdown_content = (
        f"[bold][orange_red1]ID[/orange_red1] : [cyan]{response['id']}[/cyan]\n"
    )
    markdown_content += (
        f"[orange_red1]Status[/orange_red1] : [yellow]{response['status']}[/yellow]\n"
    )
    markdown_content += f"[orange_red1]Cloud[/orange_red1] : [yellow]{response['instance_details']['cloud']}[/yellow]\n"
    markdown_content += f"[orange_red1]GPU_Type[/orange_red1] : [yellow]{response['instance_details']['gpu_type']}[/yellow]\n"
    markdown_content += f"[orange_red1]GPU_Count[/orange_red1] : [yellow]{response['instance_details']['gpu_count']}[/yellow]\n"
    markdown_content += f"[orange_red1]Cost[/orange_red1] : [yellow]$ {round(response['instance_details']['on_demand'], 3)}[/yellow]\n"
    markdown_content += f"[orange_red1]SSH Command[/orange_red1] : [yellow]$ ssh -i  {file_path} {username}@{ip} -p {metadata.get('container_ssh_port', 22)}[/yellow]"

    # Display panel along with SSH command
    console.print(Panel(markdown_content))
    pass


@gpu_machines.command(name="list_available")
@click.option("--gpu_type", type=click.STRING, required=False, help="GPU Type to use")
@click.option(
    "--num_gpus", type=click.INT, required=False, help="Number of GPUs to use"
)
@click.option("-p", "--plain", is_flag=True)
def list_available_gpu_machines(
    gpu_type: Optional[str], num_gpus: Optional[int], plain: bool
):

    console = Console()
    table = Table(
        show_header=True,
        title="Available GPU Machines",
        box=None if plain else box.DOUBLE_EDGE,
    )

    col_names = [
        "ID",
        "GPU Type",
        "GPU Count",
        "Price Per Hour (USD)",
        "Region",
        "Memory (GB)",
        "vCPUs",
    ]

    for col in col_names:
        table.add_column(col)

    with console.status("[bold green]Fetching list...") as _:
        data = get_available_machines(gpu_type, num_gpus)

    if not data:
        click.echo(
            click.style(f"\nNo GPUs available with the selected config", fg="red")
        )
        exit(0)

    for machine in data:
        table.add_row(
            machine["id"],
            machine["gpu_type"],
            str(machine["gpu_count"]),
            str(round(machine["on_demand"], 3)),
            machine["region"],
            str(int(machine["memory"])),
            str(int(machine["vcpus"])),
        )

    if table.row_count <= 15 or plain:
        console.print(table, justify="left")
    else:
        with console.pager():
            console.print(table, justify="left")


@gpu_machines.command(name="create")
@click.option(
    "--machine_avail_id",
    type=click.STRING,
    required=True,
    help="Machine ID from list_available command",
)
@click.option(
    "--artifacts_store_name",
    type=click.STRING,
    required=False,
    help="Artifacts Store name to be used",
)
def create_gpu_machine(
    machine_avail_id: str,
    artifacts_store_name: Optional[str] = None,
):
    """
    Create a new GPU machine
    """

    payload: Dict[str, Any] = {
        "machine_avail_id": machine_avail_id,
        "artifacts_store_name": artifacts_store_name,
    }

    response = send_request("POST", "/gpu_machines/create", data=payload)
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.content.decode('utf-8')}")


@gpu_machines.command(name="delete")
@click.argument("gpu_machine_id", type=click.STRING)
def delete_gpu_machine(gpu_machine_id: str):
    """
    Delete an existing GPU machine
    """
    payload: Dict[str, Any] = {"gpu_machine_id": gpu_machine_id}

    console = Console()
    with console.status("[bold green]Deleting machine...") as _:
        response = send_request("DELETE", "/gpu_machines/delete", params=payload)
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.content.decode('utf-8')}")
