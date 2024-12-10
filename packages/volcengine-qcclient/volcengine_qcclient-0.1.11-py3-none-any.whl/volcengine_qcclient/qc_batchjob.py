import base64
import time
from typing import List, Dict, Optional, Union
import os
from datetime import datetime
import random
import string
from retry import retry
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


# QcBatchJob: A batch job of qc tasks
class QcBatchJob:
    def __init__(self, ak: str, sk: str,
                 qc_service_id: str = None,
                 label: str = None
                 ):
        # init volcengine qc_service.
        self.qc_service = QcService()
        self.qc_service.set_ak(ak)
        self.qc_service.set_sk(sk)

        if label is None:
            self.label = _generate_label()
        else:
            self.label = label
        print(f"task label is {self.label}")

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
                print(f"Available qc service found: {qc_service['Id']}")
                return qc_service['Id']

        raise ValueError("No available qc service found.")

    # todo:
    def check_qc_service(self, qc_service_id) -> bool:
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
            print("there is no molecule loaded, skip submit.")
            return []

        self.task_type = task_type
        print(f"task type is {self.task_type}")
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

    def wait(self):
        while True:
            summary = self.get_task_summary()
            print(summary)
            if len(summary) == 0:
                raise ValueError("No tasks found.")

            is_finished = True
            for status in ["Running", "Pending", "Killed"]:
                if status in summary and summary[status] > 0:
                    is_finished = False
                    break

            if is_finished:
                print("batch job finished.")
                break
            time.sleep(3)

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
