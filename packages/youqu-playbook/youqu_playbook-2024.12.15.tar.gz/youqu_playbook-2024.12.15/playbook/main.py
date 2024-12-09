import time
from typing import List, Dict
import itertools
import json
import os
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from funnylog2 import logger

from playbook.__version__ import __version__
from playbook.utils import pre_env, exit_with_playbook_run_exitcode, set_playbook_run_exitcode
from playbook.utils import convert_client_to_ip
from playbook.utils import check_remote_connected
from playbook.command import Command


class PlayBook:

    def __init__(self, **kwargs):
        self.clients = kwargs.get("clients")
        self.tags = kwargs.get("tags")
        self.only_one_client = True if len(self.clients) == 1 else False
        self.IS_DEBUG = kwargs.get("debug") is True
        self.kwargs = kwargs

    def make_playbook(self) -> List[List[Dict]]:
        playbook: List = []
        group: List = []
        apps = sorted(self.kwargs.get("apps"), key=lambda x: x.get("order"))
        if self.only_one_client:
            for app_obj in apps:
                app_dict = self._create_app_dict(app_obj, split_run=False)
                group.append(app_dict)
                playbook.append(group)
                group = []
        else:
            for app_obj in apps:
                split_run = app_obj.get("split_run")
                app_dict = self._create_app_dict(app_obj, split_run=split_run)
                if split_run:
                    if group:
                        playbook.append(group)
                        group = []
                    group.append(app_dict)
                    playbook.append(group)
                    group = []
                else:
                    group.append(app_dict)
            if group:
                playbook.append(group)
        transfer_file = f"transfer_{self.kwargs.get('task_id')}.json"
        with open(transfer_file, "w", encoding="utf-8") as f:
            json.dump(playbook, f, indent=4)
            logger.info(f"PlayBook 生成: {transfer_file}")
            logger.info(json.dumps(playbook, indent=4))
        return playbook

    def _create_app_dict(self, app_obj: Dict, split_run: bool) -> Dict:
        clients = self.clients if split_run else "rolling"
        if self.only_one_client:
            clients = self.clients
            split_run = False
        app_dict = {
            "app_name": app_obj.get("app_name"),
            "git": {
                "url": app_obj.get("git_url"),
                "branch": app_obj.get("git_branch")
            },
            "framework": app_obj.get("framework"),
            "split_run": split_run,
            "clients": clients,
            "order": app_obj.get("order")
        }
        return app_dict

    def get_client_test_status(self, user, ip, password):
        if self.IS_DEBUG:
            return False
        status_test = os.popen(
            f'''sshpass -p {password} ssh {user}@{ip} "ps aux | grep -E 'env\.sh|pytest' | grep -v grep"'''
        ).read()
        return bool(status_test.strip())

    def run_by_cmd(self, cmd):
        logger.info(cmd)
        if self.IS_DEBUG:
            return
        return_code = os.system(cmd)
        set_playbook_run_exitcode(return_code)

    def _generate_command(self, app: Dict, client=None) -> str:
        framework = app.get("framework")
        clients = app.get("clients") if client is None else [client]

        if hasattr(Command, f"{framework}_command"):
            cmd = getattr(
                Command(
                    app.get("app_name"),
                    clients,
                    self.tags,
                    self.kwargs.get("task_id"),
                    app.get("git").get("url"),
                    app.get("git").get("branch"),
                    self.kwargs.get("json_backfill_base_url"),
                    self.kwargs.get("json_backfill_user"),
                    self.kwargs.get("json_backfill_password"),
                    self.kwargs.get("pms_user"),
                    self.kwargs.get("pms_password"),
                    self.kwargs.get("pms_task_id"),
                    self.IS_DEBUG,
                    self.kwargs.get("manages")
                ),
                f"{framework}_command"
            )()
        else:
            raise EnvironmentError(f"Framework: {framework} not supported")
        return cmd

    def play(self):
        playbooks = self.make_playbook()
        for index, group in enumerate(playbooks):
            logger.debug(f"======= 开始执行 group {index + 1} =======")
            split_run = len(group) == 1 and group[0].get("split_run")
            if split_run or self.only_one_client:
                cmd = self._generate_command(group[0])
                self.run_by_cmd(cmd)
            else:
                executor = ThreadPoolExecutor()
                tasks = []
                for app in group:

                    for client in itertools.cycle(self.clients):
                        user, ip, password = convert_client_to_ip(client)
                        logger.debug(f"检查 {client} 状态是否空闲")
                        if not self.get_client_test_status(user, ip, password):
                            logger.debug(f"{client} 状态空闲，开始执行")
                            cmd = self._generate_command(app, client)
                            t = executor.submit(self.run_by_cmd, cmd)
                            tasks.append(t)

                            for _ in range(25):
                                if self.IS_DEBUG:
                                    break
                                logger.debug(f"等待 {ip} 启动测试")
                                if self.get_client_test_status(user, ip, password):
                                    logger.debug(f"{ip} 测试已启动")
                                    break
                                time.sleep(2)
                            break
                        else:
                            logger.debug(f"{client} 状态非空闲，等待下一个")
                            time.sleep(3)

                wait(tasks, return_when=ALL_COMPLETED)
                executor.shutdown()
            logger.debug(f"======= 结束执行 group {index + 1} =======\n")


def playbook(input_json_path, debug):
    logger.info(f"PlayBook, version: {__version__}")
    with open(input_json_path, "r", encoding="utf-8") as f:
        kwargs = json.load(f)

    kwargs["debug"] = debug
    input_clients = kwargs.get("clients")
    if not input_clients:
        raise ValueError
    clients = []
    for client in input_clients:
        if check_remote_connected(*convert_client_to_ip(client), debug):
            clients.append(client)
        else:
            logger.error(f"======= {client} SSH 连接不通，已剔除资源池！=======")
    kwargs["clients"] = clients

    pre_env()
    PlayBook(**kwargs).play()
    exit_with_playbook_run_exitcode()


if __name__ == '__main__':
    playbook("../info.json", debug=True)
