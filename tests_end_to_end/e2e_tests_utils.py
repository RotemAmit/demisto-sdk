import subprocess
import sys

import demisto_client

from demisto_sdk.commands.common.constants import DEMISTO_GIT_PRIMARY_BRANCH
from demisto_sdk.commands.common.logger import logger
from demisto_sdk.commands.common.tools import get_demisto_version


def git_clone_demisto_sdk(
    destination_folder: str, sdk_git_branch: str = DEMISTO_GIT_PRIMARY_BRANCH
):
    """Clone demisto-sdk from GitHub and add it to sys.path"""
    from demisto_sdk.commands.common.git_util import GitUtil

    logger.info(f"Cloning demisto-sdk to {destination_folder}")

    GitUtil.REPO_CLS.clone_from(
        url="https://github.com/demisto/demisto-sdk.git",
        to_path=destination_folder,
        multi_options=[f"-b {sdk_git_branch}", "--single-branch", "--depth 1"],
    )

    sys.path.insert(1, f"{destination_folder}")


def cli(command: str) -> subprocess.CompletedProcess:
    if command:
        run_req = str(command).split(" ")
        ret_value: subprocess.CompletedProcess = subprocess.run(run_req)
        ret_value.check_returncode()
        return ret_value
    raise Exception("cli cannot be empty.")


def connect_to_server(insecure: bool = False):
    verify = (
        (not insecure) if insecure else None
    )  # set to None so demisto_client will use env var DEMISTO_VERIFY_SSL
    client = demisto_client.configure(verify_ssl=verify)
    demisto_version = get_demisto_version(client)
    if demisto_version == "0":
        raise Exception(
            "Could not connect to XSOAR server. Please check your connection configurations."
        )
    return client
