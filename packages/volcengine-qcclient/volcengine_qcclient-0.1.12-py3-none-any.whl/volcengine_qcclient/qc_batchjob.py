import base64
import logging
import sys
import time
from typing import List, Dict, Optional, Union
import os
from datetime import datetime
import random
import string
from retry import retry
import requests
import tarfile
import shutil
from urllib3.exceptions import ReadTimeoutError

from volcengine_qcclient import QcService

validTaskStatuses = [
    "Pending",
    "Running",
    "Succeeded",
    "Failed",
    "Killed",
    "Stopped",
]

MAX_BATCH_SIZE = 100


def _generate_label(prefix='qcbatchjob'):
    now = datetime.now()
    date_str = now.strftime("%Y%m%d%H%M")

    # generate random string with length 5.
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

    # generate final label.
    label = f"{prefix}-{date_str}-{random_str}"
    return label


def encode_base64(raw: string) -> str:
    return base64.b64encode(raw.encode('utf-8')).decode('utf-8')


def decode_base64(raw: str) -> str:
    return base64.b64decode(raw.encode('utf-8')).decode('utf-8')


def hide_str(s: str, hide_length=30):
    if not s:
        return ''
    if len(s) <= hide_length:
        return '*' * len(s)

    start_index = (len(s) - hide_length) // 2
    end_index = start_index + hide_length

    hidden_string = s[:start_index] + '*' * hide_length + s[end_index:]

    return hidden_string


def is_valid_xyz_content(content: str) -> bool:
    lines = content.split('\n')

    # Check if there are enough lines
    if len(lines) < 2:
        return False

    # Check if the first line is a valid integer
    try:
        num_atoms = int(lines[0])
    except ValueError:
        return False

    # Check if the number of atom lines matches the specified number of atoms
    if len(lines) != num_atoms + 2:
        return False

    # Validate each atom line
    for i in range(2, len(lines)):
        parts = lines[i].split()
        if len(parts) != 4:
            return False

        element, x, y, z = parts

        # Check if the element symbol is alphabetic
        if not element.isalpha():
            return False

        # Check if x, y, z are valid floating point numbers
        try:
            float(x)
            float(y)
            float(z)
        except ValueError:
            return False

    return True


def is_finished(summary: dict) -> bool:
    for status in ["Running", "Pending", "Killed"]:
        if status in summary and summary[status] > 0:
            return False
    return True


# download_output download output of qc task to target_dir.
@retry(ReadTimeoutError, tries=3, delay=2)
def download_output(url: str, target_dir: str):
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    os.makedirs(target_dir, exist_ok=True)
    if ".h5" in url:
        output_h5 = os.path.join(target_dir, "output.h5")
        open(output_h5, 'wb').write(requests.get(url).content)
    elif "tar.gz" in url:
        output_targz = os.path.join(target_dir, "output.tar.gz")
        open(output_targz, 'wb').write(requests.get(url).content)
        with tarfile.open(output_targz, 'r:gz') as tar:
            tar.extractall(path=target_dir)
        os.remove(output_targz)
    else:
        print("unsupported file type")


def get_default_logger(log_level):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # 创建一个处理器，将 DEBUG 和 INFO 级别的日志消息输出到 stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)  # 设置处理器的最低日志级别
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)  # 过滤仅输出 DEBUG 和 INFO 级别的日志

    # 创建一个处理器，将 WARNING 及以上级别的日志消息输出到 stderr
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)  # 设置处理器的最低日志级别

    # 创建一个日志格式器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    return logger


# QcBatchJob: A batch job of qc tasks
class QcBatchJob:
    def __init__(self, ak: str = None, sk: str = None,
                 qc_service_id: str = None,
                 label: str = None,
                 log_level: Optional[str] = None,
                 logger: Optional[logging.Logger] = None,
                 ):

        if logger:
            self.logger = logger
        elif log_level:
            self.logger = get_default_logger(log_level)
        else:
            self.logger = get_default_logger(logging.INFO)

        # init volcengine qc_service.
        self.qc_service = QcService()
        if ak and sk:
            self.qc_service.set_ak(ak)
            self.qc_service.set_sk(sk)
        else:
            logger.debug("ak/sk not set, try to load from env(`VOLC_ACCESSKEY` or `VOLC_SECRETKEY`) or "
                         "~/.volc/credentials.")
        if not self.qc_service.service_info.credentials.ak or not self.qc_service.service_info.credentials.sk:
            raise ValueError("ak/sk can not load from env(`VOLC_ACCESSKEY` or `VOLC_SECRETKEY`) or "
                             "`~/.volc/credentials`.")

        self.logger.debug(f"ak: {hide_str(self.qc_service.service_info.credentials.ak)}")
        if label is None:
            self.label = _generate_label()
        else:
            self.label = label
        self.logger.info(f"task label is {self.label}")

        self.task_type = None
        self.molecules = []
        self.qc_tasks = []

        if qc_service_id is None:
            self.qc_service_id = self.find_available_qc_service()
        else:
            if self.check_qc_service(qc_service_id):
                self.qc_service_id = qc_service_id
            else:
                raise ValueError("qc_service_id is invalid.")

    def get_label(self) -> str:
        return self.label

    def find_available_qc_service(self) -> str:
        data = self.qc_service.list_qc_services(params={})
        for qc_service in data['Items']:
            if qc_service['Status'] == 'Enabled':
                self.logger.info(f"Available qc service found: {qc_service['Id']}")
                return qc_service['Id']

        raise ValueError("No available qc service found.")

    def check_qc_service(self, qc_service_id) -> bool:
        data = self.qc_service.list_qc_services(params={
            "Ids": [qc_service_id],
        })
        if not isinstance(data["Items"], list) or len(data["Items"]) != 1:
            self.logger.error(f"qc_service_id {qc_service_id} is not found.")
            return False
        qc_service = data["Items"][0]
        if qc_service['Status'] != 'Enabled':
            self.logger.error(f"qc_service_id {qc_service_id} is not enabled.")
            return False
        return True

    # load molecules from local dir or file path or python list variable.
    def load_molecules(self, from_dir: str = None, from_file: str = None, from_list: List[str] = None,
                       with_molecule_names: List[str] = None):
        if from_dir is not None:
            if not os.path.isdir(from_dir):
                raise ValueError("Directory does not exist.")
            for file_name in sorted(os.listdir(from_dir)):
                if file_name.endswith(".xyz"):
                    # parse molecule name from file_name.
                    molecule_name = file_name.rstrip(".xyz")
                    file_path = os.path.join(from_dir, file_name)
                    with open(file_path, "r") as file:
                        xyz_content = file.read()
                        xyz_content = xyz_content.strip("\n").strip()
                        self.molecules.append({
                            "molecule_name": molecule_name,
                            "content": xyz_content,
                        })

        if from_file is not None:
            if os.path.isfile(from_file) and from_file.endswith(".xyz"):
                molecule_name = os.path.basename(from_file).rstrip(".xyz")
                with open(from_file, "r") as file:
                    xyz_content = file.read()
                    xyz_content = xyz_content.strip("\n").strip()
                    self.molecules.append({
                        "molecule_name": molecule_name,
                        "content": xyz_content,
                    })

        if from_list is not None:
            if with_molecule_names is not None and len(with_molecule_names) != len(from_list):
                raise ValueError("`with_molecule_names` must be the same length as `from_list`.")

            for i in range(len(from_list)):
                xyz_content = from_list[i]
                xyz_content = xyz_content.strip("\n").strip()
                if not is_valid_xyz_content(xyz_content):
                    raise ValueError("Invalid xyz content.")

                self.molecules.append({
                    "molecule_name": "" if with_molecule_names is None else with_molecule_names[i],
                    "content": xyz_content,
                })

    def get_molecules(self) -> List[str]:
        return self.molecules

    def clear_molecules(self):
        self.molecules = []

    # submit qc tasks to server.
    def submit(self, task_type: str, task_config: Union[Dict, List[Dict]]) -> List[str]:
        if len(self.molecules) == 0:
            self.logger.info("there are no molecules loaded, skip submit.")
            return []

        self.task_type = task_type
        self.logger.info(f"task type is {self.task_type}")
        qc_tasks = []
        if isinstance(task_config, list):
            if len(task_config) != len(self.molecules):
                raise ValueError(f"task config is array(len {len(task_config)}),"
                                 f" but the length not equals preloaded molecules(len {len(self.molecules)}).")
            for i in range(len(self.molecules)):
                qc_tasks.append({
                    "MoleculeXyzData": encode_base64(self.molecules[i]["content"]),
                    "MoleculeName": self.molecules[i]["molecule_name"],
                    "QcTaskConfig": task_config[i],
                })
        elif isinstance(task_config, dict):
            for molecule in self.molecules:
                qc_tasks.append({
                    "MoleculeXyzData": encode_base64(molecule["content"]),
                    "MoleculeName": molecule["molecule_name"],
                    "QcTaskConfig": task_config,
                })
        else:
            raise ValueError("task_config must be either dict or list[dict]")

        offset = 0
        task_ids = []
        while offset < len(qc_tasks):
            batch_tasks = qc_tasks[offset: offset + MAX_BATCH_SIZE]
            params = {
                "QcServiceId": self.qc_service_id,
                "TaskType": task_type,
                "Label": self.label,
                "QcTasks": batch_tasks,
            }
            data = self.qc_service.submit_qc_tasks(params=params)
            task_ids.extend(data["Ids"])
            offset += MAX_BATCH_SIZE
        return task_ids

    @retry(ReadTimeoutError, tries=3, delay=2)
    def get_task_summary(self) -> Dict[str, int]:
        params = {
            "QcServiceId": self.qc_service_id,
            "Label": self.label,
        }
        return self.qc_service.get_qc_tasks_summary(params=params)

    def wait(self, download_outputs: bool = False, duration: int = 5):
        self.logger.info(f"download_outputs is set {download_outputs}")
        while True:
            summary = self.get_task_summary()
            self.logger.info(f"tasks summary: {summary}")

            if download_outputs:
                self.download_outputs()

            if len(summary) == 0:
                raise ValueError("no tasks found.")

            if is_finished(summary):
                self.logger.info("batch job finished.")
                break

            time.sleep(duration)

    def is_finished(self) -> bool:
        summary = self.get_task_summary()
        return is_finished(summary)

    def download_outputs(self,
                         task_ids: Optional[List[str]] = None,
                         target_dir: Optional[str] = None,
                         overwrite_exists: bool = False
                         ):
        if target_dir is None:
            target_dir = "./"

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        params = {
            "QcServiceId": self.qc_service_id,
            "Label": self.label,
            "PageSize": MAX_BATCH_SIZE,
            "SortBy": "CreateTime",
            "SortOrder": "Asc",
        }
        if isinstance(task_ids, list) and len(task_ids) > 0:
            params["Ids"] = task_ids

        page_number = 1
        while True:
            params["PageNumber"] = page_number
            data = self.qc_service.list_qc_tasks(params=params)
            if not data["Items"] or not isinstance(data["Items"], list):
                break

            for task in data["Items"]:
                task_id = task["Id"]
                output_url = task["OutputUrl"]
                if not output_url:
                    self.logger.debug(f"output url of task_id: {task_id} is empty, skip download, task_status: {task['Status']}")
                    continue

                task_dir = os.path.join(target_dir, task_id)
                if os.path.exists(task_dir) and not overwrite_exists:
                    self.logger.debug(
                        f"task {task_id} output already exists and `overwrite_exists` is set {overwrite_exists}, "
                        f"skip download, task_dir: {task_dir}")
                    continue
                download_output(output_url, task_dir)
            page_number += 1

    def get_tasks(self, task_ids: Optional[List[str]] = None) -> List[Dict]:
        params = {
            "QcServiceId": self.qc_service_id,
            "Label": self.label,
            "PageSize": MAX_BATCH_SIZE,
            "SortBy": "CreateTime",
            "SortOrder": "Asc",
        }
        if task_ids is not None and len(task_ids) > 0:
            params["Ids"] = task_ids

        tasks = []

        page_number = 1
        while True:
            params["PageNumber"] = page_number
            data = self.qc_service.list_qc_tasks(params=params)
            if data["Items"] is not None and len(data["Items"]) > 0:
                tasks.extend(data["Items"])
            else:
                break
            page_number += 1

        return tasks

    def stop(self):
        params = {
            "QcServiceId": self.qc_service_id,
            "Label": self.label,
        }
        self.qc_service.stop_qc_tasks(params=params)

    def retry(self, status: str = None):
        params = {
            "QcServiceId": self.qc_service_id,
            "Label": self.label,
        }
        if status is not None:
            if status not in validTaskStatuses:
                raise ValueError(f"status must be in {validTaskStatuses}")
            params["Status"] = status

        self.qc_service.retry_qc_tasks(params=params)
