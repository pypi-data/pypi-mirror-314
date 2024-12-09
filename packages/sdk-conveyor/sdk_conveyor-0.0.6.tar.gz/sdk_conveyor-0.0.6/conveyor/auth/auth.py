import json
import logging
import os
import subprocess
import webbrowser
from typing import TYPE_CHECKING, Optional

import grpc
from packaging.version import Version
from packaging.version import parse as parse_version

if TYPE_CHECKING:
    from subprocess import CompletedProcess

logger = logging.getLogger(__name__)


class _ElectronNotAsNode:
    """Workaround for https://github.com/microsoft/vscode/issues/224498"""

    __slots__ = "value"

    def __enter__(self):
        self.value = os.environ.pop("ELECTRON_RUN_AS_NODE", None)

    def __exit__(self, type_, value, traceback):
        if self.value is not None:
            os.environ["ELECTRON_RUN_AS_NODE"] = value


def _get_token(timeout: int = 60) -> Optional[str]:
    try:
        proc = subprocess.Popen(
            ("conveyor", "auth", "get", "--no-browser"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        logger.error(
            "The Conveyor CLI is not installed, please follow the instructions at https://docs.conveyordata.com/get-started/installation#install-the-cli"
        )
        return None

    if (io := proc.stderr) and (message := io.readline()):
        # Parse error message to obtain login URL (if needed)
        url = str(message).split(": ")[-1]
        # Use main process to open URL, using a subprocess for this does not always work (f.e. in Jupyter)
        with _ElectronNotAsNode():
            webbrowser.open_new_tab(url)

    try:
        outs, _ = proc.communicate(timeout=timeout)
        return json.loads(outs).get("access_token")
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        logger.error(
            f"Unable to authenticate after waiting {timeout} seconds.\nMessage: {outs}\nError: {errs}"
        )
    return None


def get_api_url() -> str:
    completed: CompletedProcess = subprocess.run(
        ("conveyor", "auth", "config"),
        capture_output=True,
        timeout=10,
        text=True,
        env=os.environ,
    )
    return json.loads(completed.stdout).get("api")


def get_grpc_target() -> str:
    api_url = get_api_url()
    return api_url.replace("https://", "")


def get_grpc_credentials() -> grpc.ChannelCredentials:
    try:
        access_token = _get_token()
    except Exception as e:
        logger.error(f"Failed to get Conveyor token due to {str(e)}")
        access_token = None

    if not access_token:
        exit(1)

    ssl = grpc.ssl_channel_credentials()
    token = grpc.access_token_call_credentials(access_token)
    return grpc.composite_channel_credentials(ssl, token)


def _validate_version(version: str) -> None:
    stripped_version = version
    # Our dev builds adds an extra git hash which is not recognized by the version parser so we remove it
    if "-" in stripped_version:
        stripped_version = stripped_version.split("-")[0]
    if parse_version(stripped_version) < Version("1.18.10"):
        raise SystemExit(
            Exception(
                f"Your Conveyor CLI is too old to work with the Python SDK. The minimal version is 1.18.10, you are using {version}"
            )
        )


def validate_cli_version() -> None:
    completed: CompletedProcess = subprocess.run(
        ("conveyor", "--version"),
        capture_output=True,
        timeout=10,
        text=True,
        env=os.environ,
    )
    version = completed.stdout.replace("conveyor version", "").strip()
    _validate_version(version)
