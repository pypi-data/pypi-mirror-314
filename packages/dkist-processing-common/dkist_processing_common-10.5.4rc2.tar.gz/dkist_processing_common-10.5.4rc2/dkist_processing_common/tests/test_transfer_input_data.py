import json
import os
from itertools import chain
from pathlib import Path
from uuid import uuid4

import pytest

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.transfer_input_data import TransferL0Data
from dkist_processing_common.tests.conftest import create_parameter_files


@pytest.fixture
def transfer_l0_data(recipe_run_id, tmp_path) -> dict:
    task = TransferL0Data(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    )
    task.scratch = WorkflowFileSystem(
        recipe_run_id=recipe_run_id,
        scratch_base_path=tmp_path,
    )
    task.scratch.scratch_base_path = tmp_path
    input_dataset_parameters_part = [
        {
            "parameterName": "param_name_1",
            "parameterValues": [
                {
                    "parameterValueId": 1,
                    "parameterValue": json.dumps([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                    "parameterValueStartDate": "2000-01-01",
                }
            ],
        },
        {
            "parameterName": "param_name_2",
            "parameterValues": [
                {
                    "parameterValueId": 2,
                    "parameterValue": json.dumps(
                        {
                            "__file__": {
                                "bucket": "data",
                                "objectKey": f"parameters/param_name/{uuid4().hex}.dat",
                            }
                        }
                    ),
                    "parameterValueStartDate": "2000-01-01",
                },
                {
                    "parameterValueId": 3,
                    "parameterValue": json.dumps(
                        {
                            "__file__": {
                                "bucket": "data",
                                "objectKey": f"parameters/param_name/{uuid4().hex}.dat",
                            }
                        }
                    ),
                    "parameterValueStartDate": "2000-01-02",
                },
            ],
        },
        {
            "parameterName": "param_name_4",
            "parameterValues": [
                {
                    "parameterValueId": 4,
                    "parameterValue": json.dumps(
                        {"a": 1, "b": 3.14159, "c": "foo", "d": [1, 2, 3]}
                    ),
                    "parameterValueStartDate": "2000-01-01",
                }
            ],
        },
    ]
    input_dataset_observe_frames_part = [
        {
            "bucket": uuid4().hex[:6],
            "object_keys": [Path(uuid4().hex[:6]).as_posix() for _ in range(3)],
        }
    ]
    input_dataset_calibration_frames_part = [
        {
            "bucket": uuid4().hex[:6],
            "object_keys": [Path(uuid4().hex[:6]).as_posix() for _ in range(3)],
        },
        {
            "bucket": uuid4().hex[:6],
            "object_keys": [Path(uuid4().hex[:6]).as_posix() for _ in range(3)],
        },
    ]
    # load parameters file
    file_path = task.scratch.workflow_base_path / Path(f"{uuid4().hex[:6]}.ext")
    file_path.write_text(data=json.dumps(input_dataset_parameters_part))
    task.tag(path=file_path, tags=Tag.input_dataset_parameters())
    # create parameter files
    expected_parameters = dict()
    for item in input_dataset_parameters_part:
        expected_parameters[item["parameterName"]] = item["parameterValues"]
    create_parameter_files(task, expected_parameters)
    # load observe frames file
    file_path = task.scratch.workflow_base_path / Path(f"{uuid4().hex[:6]}.ext")
    file_path.write_text(data=json.dumps(input_dataset_observe_frames_part))
    task.tag(path=file_path, tags=Tag.input_dataset_observe_frames())
    # load calibration frames file
    file_path = task.scratch.workflow_base_path / Path(f"{uuid4().hex[:6]}.ext")
    file_path.write_text(data=json.dumps(input_dataset_calibration_frames_part))
    task.tag(path=file_path, tags=Tag.input_dataset_calibration_frames())

    yield {
        "task": task,
        "parameters": input_dataset_parameters_part,
        "observe": input_dataset_observe_frames_part,
        "calibration": input_dataset_calibration_frames_part,
    }
    task._purge()


def test_format_frame_transfer_items(transfer_l0_data):
    """
    :Given: a TransferL0Data task with a valid input dataset
    :When: formatting items in the input dataset for transfer
    :Then: the items are correctly loaded into GlobusTransferItem objects
    """
    task = transfer_l0_data["task"]
    source_filenames = []
    destination_filenames = []
    for frame_set in chain(transfer_l0_data["observe"], transfer_l0_data["calibration"]):
        for key in frame_set["object_keys"]:
            source_filenames.append(os.path.join("/", frame_set["bucket"], key))
            destination_filenames.append(Path(key).name)
    assert len(task.format_frame_transfer_items()) == len(source_filenames)
    for item in task.format_frame_transfer_items():
        assert item.source_path.as_posix() in source_filenames
        assert item.destination_path.name in destination_filenames
        assert not item.recursive


def test_format_parameter_file_transfer_items(transfer_l0_data):
    """
    :Given: a TransferL0Data task with a valid input dataset
    :When: formatting items in the input dataset for transfer
    :Then: the items are correctly loaded into GlobusTransferItem objects
    """
    task = transfer_l0_data["task"]
    source_filenames = []
    destination_filenames = []
    for param in transfer_l0_data["parameters"]:
        for value in param["parameterValues"]:
            param_value = value["parameterValue"]
            if "__file__" in param_value:
                value_dict = json.loads(param_value)
                bucket = value_dict["__file__"]["bucket"]
                object_key = value_dict["__file__"]["objectKey"]
                source_filenames.append(os.path.join("/", bucket, object_key))
                destination_filenames.append(Path(object_key).name)
    transfer_items = task.format_parameter_transfer_items()
    assert len(transfer_items) == len(source_filenames)
    for transfer_item in transfer_items:
        assert transfer_item.source_path.as_posix() in source_filenames
        assert transfer_item.destination_path.name in destination_filenames
        assert str(transfer_item.destination_path).startswith(str(task.scratch.workflow_base_path))
        assert not transfer_item.recursive
