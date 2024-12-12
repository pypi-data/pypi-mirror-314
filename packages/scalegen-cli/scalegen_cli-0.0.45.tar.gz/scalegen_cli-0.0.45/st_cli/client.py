from typing import Any, Dict, Optional
import requests
import json
import time
import click
import os

from .const import PLATFORM_API, CACHE_PATH, AUTH0_TENANT, AUTH0_API_AUDIENCE


def get_new_access_token(client_id: str, client_secret: str) -> str:

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": AUTH0_API_AUDIENCE,
    }
    resp = requests.post(
        f"{AUTH0_TENANT}/oauth/token",
        json=data,
        headers={"content-type": "application/json"},
    )
    # print(resp.json())
    assert resp.status_code == 200

    return resp.json()


def get_access_token() -> str:
    creds = read_creds()
    if time.time() < creds["expires_at"]:
        return creds["access_token"]

    store_creds(creds["client_id"], creds["client_secret"])
    return get_access_token()


def store_creds(client_id: str, client_secret: str):
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)

    creds = {"client_id": client_id, "client_secret": client_secret}

    resp = get_new_access_token(client_id, client_secret)
    # print(resp)
    creds["access_token"] = resp["access_token"]  # type: ignore
    creds["expires_at"] = time.time() + float(resp["expires_in"]) - 10  # type: ignore

    with open(CACHE_PATH, "w") as fp:
        json.dump(creds, fp)


def read_creds():
    if not os.path.exists(CACHE_PATH):
        click.echo(
            "Could not perform operation. Please try logging in again.", err=True
        )
        exit(1)

    with open(CACHE_PATH, "r") as fp:
        creds = json.load(fp)

    return creds


def send_request(
    method: str,
    end_point: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
):

    token = get_access_token()
    url = f"{PLATFORM_API}{end_point}"
    header = {"Authorization": f"Bearer {token}"}
    resp = requests.request(method, url, headers=header, json=data, params=params)

    if os.environ.get("ST_DEBUG") == "1":
        print(f"Request: {method} {end_point}")
        print(f"Response: {resp.content.decode('utf-8')}")

    return resp


# def get_creds():
#     # TODO: Needs to return B2 bucket name for the user, B2 creds, Encryption Key
#     resp = send_request('POST', '/keys')

#     creds = read_credentials()
#     raw_data = resp.raw.read()
#     # Decrypt the response


def get_garb(key: str) -> str:
    # Fetch it from API
    resp = send_request("GET", f"/secret/{key}")
    if resp.status_code == 200:
        content = resp.json()["secret"][key]
        # if "GS_CREDS" in key or "GDRIVE_CREDS" in key:
        #     content = base64.b64decode(content.encode()).decode("utf8")

        # if not content:
        #     logger.warning(f"garb: {key} is empty!")
        return content

    return ""
