import json
import traceback
import click
import os
from rich.console import Console

from .const import CACHE_PATH
from .client import send_request, store_creds


@click.command()
@click.option("-ki", "--access_key_id", type=click.STRING, required=True)
@click.option("-ks", "--access_key_secret", type=click.STRING, required=True)
def login(access_key_id, access_key_secret):

    # Verify ID and secret
    console = Console()
    with console.status("[bold green]Logging in...") as status:
        try:
            store_creds(access_key_id, access_key_secret)
        except:
            # print(traceback.format_exc())
            click.echo(click.style("\nInvalid credentials", fg="red"), err=True)
            return

        resp = send_request("POST", "/user/verify")
        # print(resp.json())

        if resp.status_code == 200:
            # User is verfied
            resp_data = resp.json()
            click.echo(click.style(f'\nLogged in as {resp_data["email"]}', fg="green"))

        else:
            # Bad credentials
            click.echo(click.style("\nInvalid credentials", fg="red"), err=True)
