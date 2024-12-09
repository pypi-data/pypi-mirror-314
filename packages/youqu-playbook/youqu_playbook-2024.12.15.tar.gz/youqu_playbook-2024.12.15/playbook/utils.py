import os
import re
import sys

from typing import Tuple

from playbook.config import config
from nocmd import RemoteCmd
from funnylog2 import logger


def pre_env():
    empty = "> /dev/null 2>&1"
    os.system("rm -rf ./Pipfile")
    os.system("rm -rf ~/Pipfile")
    os.system("rm -rf .venv")
    os.system("rm -rf ~/.ssh/known_hosts")
    sudo = f"echo '{config.PASSWORD}' | sudo -S"
    if "StrictHostKeyChecking no" not in os.popen("cat /etc/ssh/ssh_config").read():
        os.system(
            f"""{sudo} sed -i "s/#   StrictHostKeyChecking ask/ StrictHostKeyChecking no/g" /etc/ssh/ssh_config {empty}"""
        )
    if os.system(f"sshpass -V {empty}") != 0:
        os.system(f"{sudo} apt update {empty}")
        os.system(f"{sudo} apt install sshpass {empty}")


def check_remote_connected(user, _ip, password, debug: bool = False):
    logger.info(f"Checking remote: {user, _ip, password}")
    if debug:
        return True
    return_code = RemoteCmd(user, _ip, password).remote_run("hostname -I", use_sshpass=True, log_cmd=False)
    if return_code == 0:
        logger.info(f"Remote: {user, _ip, password} connected")
        return True
    return False


def convert_client_to_ip(client: str) -> Tuple[str, str, str]:
    match = re.match(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", client)
    if match:
        user, ip, password = match.groups()
        if not password:
            password = config.PASSWORD
        return user, ip, password
    else:
        raise ValueError("Invalid client format")

def set_playbook_run_exitcode(status):
    if status != 0:
        os.environ["PLAYBOOK_RUN_EXIT_CODE"] = str(status)

def exit_with_playbook_run_exitcode():
    playbook_run_exitcode = os.environ.get("PLAYBOOK_RUN_EXIT_CODE")
    if playbook_run_exitcode is not None and int(playbook_run_exitcode) != 0:
        sys.exit(1)
