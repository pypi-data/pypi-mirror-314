from collections import deque
import glob
import random
import string
import time
import click
from typing import List, Any
import subprocess
from progress.spinner import PixelSpinner
import os
import yaml
import io
import zipfile
import requests
from rich.progress import track
from rich.live import Live
from rich.table import Table
from rich.text import Text
import threading
from typing import Dict
from gettext import gettext as _


from .datamodels.datamodels import CodeCopy, CodeCopyType
from .const import MAX_FILES, MAX_SIZE_MB, PRODUCT_TYPE, UPLOAD_WORKERS
from .client import send_request


class CustomSpinner(PixelSpinner):
    def finish(self, fail=False):
        emj = "✅" if not fail else "❌"
        line = "".join([self.message, emj])
        self.writeln(line)
        self.hide_cursor = True


def get_random_str():
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(12)
    )


def run_command(command: str):
    process = subprocess.run(command.split(), stdout=subprocess.PIPE)
    return process.stdout.decode("utf-8").strip("\n")


def read_config_from_yaml(config_path) -> dict:
    config_path = os.path.join(os.getcwd(), config_path)

    if not os.path.exists(config_path):
        click.echo(
            click.style(
                f"{config_path} not found. Please specify config file path", fg="red"
            ),
            err=True,
        )
        exit()

    with open(config_path, "r") as fp:
        config_yaml = fp.read()
        dict_ = yaml.safe_load(config_yaml)

    return dict_


def get_template(template_name: str) -> dict:

    resp = send_request(method="GET", end_point="/templates")
    if resp.status_code != 200:
        click.echo(click.style(f"Template could not be fetched", fg="red"), err=True)
        exit()

    templates = list(filter(lambda x: x["name"] == template_name, resp.json()))
    if not templates:
        return {}

    template_config = templates.pop()["config"]
    return template_config


def zip_and_upload(working_directory: str, exclude_dirs: tuple = ()):
    working_directory = working_directory if working_directory else "."

    assert (
        os.path.exists(working_directory) == True
    ), "codeDir specified in config does not exist"

    # Get user email
    user_email = ""
    resp = send_request("POST", "/user/verify")
    if resp.status_code == 200:
        user_email = resp.json()["email"]
    else:
        click.echo(click.style("Could not connect to API", fg="red"), err=True)
        return

    # Check number of files
    all_files = glob.glob(f"{working_directory}/**", recursive=True)

    # TODO: Use os.walk and exclude sub-directories
    for exclude_dir in exclude_dirs:
        all_files = list(filter(lambda x: exclude_dir not in x, all_files))

    all_files = list(
        filter(lambda x: not os.path.isdir(x), all_files)
    )  # Excluding dir names

    if len(all_files) > MAX_FILES:
        click.echo(
            click.style("Folder contains more than 2000 files.", fg="red"),
            err=True,
        )
        return

    # Check folder size
    folder_size = sum([os.path.getsize(file) for file in all_files]) / (
        1024**2
    )  # Size in MB
    if folder_size > MAX_SIZE_MB:
        click.echo(
            click.style(f"Folder size is more than {MAX_SIZE_MB} MB.", fg="red"),
            err=True,
        )
        return

    # Create a zip file
    # Progress bar
    spinner = CustomSpinner(f"Uploading files ")
    stop_spinner = False
    spinner_error = False

    def spinner_update():
        while True:
            time.sleep(0.5)
            spinner.next()
            if stop_spinner:
                spinner.finish(spinner_error)
                break

    spinner_thread = threading.Thread(target=spinner_update, daemon=True)
    spinner_thread.start()

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, mode="w") as archive:
        for file in all_files:
            file = file.lstrip("./")
            with open(file, "rb") as local_file, archive.open(file, "w") as zip_file:
                zip_file.write(local_file.read())

    zip_buffer.seek(0)

    # Get the pre Signed URL
    resp = send_request("POST", "/get_presigned_url")
    if resp.status_code != 200:
        click.echo(click.style(f"Could not upload files", fg="red"), err=True)
        return
    resp_data = resp.json()

    # Upload zip file
    filename = f"B2_{user_email}_{get_random_str()}.zip"

    # TESTING: Write to a file for testing
    # zip_buf_copy = zip_buffer
    # with open(filename, "wb") as fp:
    #     fp.write(zip_buf_copy.read())

    headers = {
        "Authorization": resp_data["data"]["token"],
        "X-Bz-File-Name": filename,
        "X-Bz-Content-Sha1": "do_not_verify",
    }

    try:
        resp = requests.post(
            resp_data["data"]["uploadUrl"],
            headers=headers,
            files={"archive": (filename, zip_buffer)},
        )
        if resp.status_code == 200:
            spinner_error = False
    except:
        click.echo(click.style(f"Could not upload files", fg="red"), err=True)
        spinner_error = True

    # Stop spinner
    stop_spinner = True
    spinner_thread.join()
    print()

    return CodeCopy(
        type=CodeCopyType.B2, repo=filename, codeDir=working_directory
    ).model_dump(mode="json")


def display_event_logs(job_id: str, **kwargs: Any):

    stage = "Starting job setup"
    try:
        while True:
            resp = send_request("GET", f"/job/{job_id}")
            if resp.status_code != 200:
                time.sleep(5)
                continue

            job = resp.json()
            spinner = CustomSpinner(f"{stage} ")

            if job["stage"] == "" or job["stage"] == stage:

                for _ in range(15):
                    spinner.next()
                    time.sleep(1)
            else:
                spinner.finish()
                print()
                stage = job["stage"]
                spinner = CustomSpinner(f"{stage} ")

            if job["status"] == "FAILED":
                spinner.finish(fail=True)
                print()
                click.echo(click.style("Couldn't create job", fg="red"), err=True)
                return

            if job["status"] == "RUNNING":
                spinner.finish()
                print()
                click.echo(click.style("The job is runnning", fg="green"))
                return

            if job["status"] in {"STOPPING", "STOPPED"}:
                spinner.finish()
                print()
                click.echo(click.style("The job was stopped", fg="yellow"))
                return

    except KeyboardInterrupt:
        if PRODUCT_TYPE == "SCALETORCH":
            stop_cmd = "scaletorch"
        else:
            stop_cmd = (
                f"scalegen finetune {kwargs.get('ft_type', '<ft_type>')} stop {job_id}"
            )

        click.echo(
            click.style(
                f"\nTo stop the workload please run `{stop_cmd}`",
                fg="yellow",
            )
        )

    except Exception:
        click.echo(
            click.style(
                f"\nFailed to retrieve the latest status. Please run `{'scaletorch' if PRODUCT_TYPE=='SCALETORCH' else 'scalegen finetune ft_type'} view {job_id}` to know the status fo the workload",
                fg="yellow",
            )
        )


def show_job_live_logs(job_id: str):
    """
    Displays the live logs of the only trial for the job by communicating with the user-logs-viewer API
    """
    try:
        # Pre-checks
        resp = send_request("GET", f"/job/{job_id}")
        if resp.status_code != 200:
            click.echo(
                click.style(
                    f"\nFailed to retrieve the latest status. Please run `{'scaletorch' if PRODUCT_TYPE=='SCALETORCH' else 'scalegen finetune'} view {job_id}` to know the status fo the workload",
                    fg="yellow",
                )
            )
            return

        job_data = resp.json()

        if job_data["status"] in {"QUEUED", "STOPPED"}:
            return

        # Helpers
        width, height = os.get_terminal_size()
        height = height - 1
        messages = deque(maxlen=height - 1)

        def get_table():
            table = Table(box=None, pad_edge=False)
            table.add_column("Logs:\n")

            for row in list(messages):
                table.add_row(Text(row))

            return table

        # Wait for trial to be running
        counter = 0
        non_dapp_trials = []

        while counter < 10:
            trial_resp = send_request("GET", f"/job/{job_id}/trials")
            trial_data: List[Dict] = trial_resp.json()
            if trial_resp.status_code == 200:
                non_dapp_trials = list(
                    filter(lambda x: not x["is_dapp_trial"], trial_data)
                )
                if non_dapp_trials and non_dapp_trials[0]["status"] == "WAITING":
                    continue
                break
            else:
                time.sleep(10)
                counter += 1

        if non_dapp_trials and non_dapp_trials[0]["status"] == "RUNNING":

            logs_url = f"https://proxy-prod.scalegen.ai/logs/{job_id}/{non_dapp_trials[0]['trial_id']}/get-last-lines?num=100&mtime={{}}"
            counter = 0

            log_resp = requests.get(logs_url.format(round(time.time() * 1000)))
            prev_line = ""
            if log_resp.status_code == 200:
                logs = log_resp.json()["content"].split("\n")
                for log in logs:
                    print(log)
                prev_line = logs[-2]

            # Create rich table for logs
            with Live(
                get_table(), refresh_per_second=4
            ) as live:  # update 4 times a second to feel fluid
                while True:
                    log_resp = requests.get(logs_url.format(round(time.time() * 1000)))
                    if log_resp.status_code == 200:
                        logs = log_resp.json()["content"].split("\n")
                        # print(logs)
                        # print("****" * 20)
                        i = -2
                        if len(logs) > 2:
                            while logs[i] != prev_line and i > -len(logs):
                                i -= 1
                            for log in logs[i + 1 : -1]:
                                print(log)
                            prev_line = logs[-2]
                        # print(logs)
                        # [messages.append(log) for log in logs]

                        # if len(logs) < height:
                        #     print(height - len(logs))
                        #     [messages.append("\n") for _ in range(height - len(logs) + 1)]

                    # Check job status
                    resp = send_request("GET", f"/job/{job_id}")
                    if resp.status_code != 200:
                        if resp.json()["status"] in {"STOPPED", "FAILED"}:
                            break

                    # time.sleep(1)
                    # live.update(get_table())

    except KeyboardInterrupt:
        click.echo(
            click.style(
                f"\nTo stop the workload please run `{'scaletorch' if PRODUCT_TYPE=='SCALETORCH' else 'scalegen finetune'} stop {job_id}` ",
                fg="yellow",
            )
        )
        exit()

    except:
        # import traceback
        # print(traceback.format_exc())
        click.echo(click.style(f"\nCould not fetch job logs", fg="red"))


def is_repo_private():
    # https://stackoverflow.com/questions/4089430/how-to-determine-the-url-that-a-local-git-repository-was-originally-cloned-from/63907839#63907839
    repo_url = run_command(
        """git config --get remote.origin.url | sed -e 's/:/\//g'| sed -e 's/ssh\/\/\///g'| sed -e 's/git@/https:\/\//g' """
    )
    try:
        print(repo_url)
        res = requests.get(repo_url, allow_redirects=True)
        return res.status_code > 300
    except:
        return True


def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents


class CategorizedMutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        self.category = kwargs.pop("category", "Common options")
        help = kwargs.get("help", "")
        if self.mutually_exclusive:
            ex_str = ", ".join(self.mutually_exclusive)
            kwargs["help"] = help + click.style(
                " NOTE: This argument is mutually exclusive with"
                " arguments: (" + ex_str + ").",
                italic=True,
            )
        super(CategorizedMutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(self.name, ", ".join(self.mutually_exclusive))
            )
        return super(CategorizedMutuallyExclusiveOption, self).handle_parse_result(
            ctx, opts, args
        )


class PatchedCommand(click.Command):
    def format_options(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Writes all the options into the formatter if they exist."""
        categories = {}
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if hasattr(param, "category") and rv is not None:
                categories.setdefault(param.category, []).append(rv)
            elif not hasattr(param, "category") and rv is not None:
                categories.setdefault("Common options", []).append(rv)

        if categories:

            with formatter.section(_("Options")):
                for group_name, opts in categories.items():
                    with formatter.section(group_name):
                        formatter.write_dl(opts, col_max=40, col_spacing=4)
