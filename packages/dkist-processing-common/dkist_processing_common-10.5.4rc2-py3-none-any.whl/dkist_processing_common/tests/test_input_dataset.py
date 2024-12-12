import json
from copy import copy
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetObject
from dkist_processing_common.tests.conftest import create_parameter_files
from dkist_processing_common.tests.conftest import InputDatasetTask


def input_dataset_frames_part_factory(bucket_count: int = 1) -> list[dict]:
    return [
        {"bucket": uuid4().hex[:6], "object_keys": [uuid4().hex[:6] for _ in range(3)]}
        for _ in range(bucket_count)
    ]


def flatten_frame_parts(frame_parts: list[dict]) -> list[tuple[str, str]]:
    result = []
    for frame_set in frame_parts:
        for key in frame_set["object_keys"]:
            result.append((frame_set["bucket"], key))
    return result


def input_dataset_parameters_part_factory(
    parameter_count: int = 1,
    parameter_value_count: int = 1,
    has_date: bool = False,
    has_file: bool = False,
) -> list[dict]:
    result = [
        {
            "parameterName": uuid4().hex[:6],
            "parameterValues": [
                {"parameterValueId": i, "parameterValue": json.dumps(uuid4().hex)}
                for i in range(parameter_value_count)
            ],
        }
        for _ in range(parameter_count)
    ]
    if has_date:
        for data in result:
            data["parameterValueStartDate"] = datetime(2022, 9, 14).isoformat()[:10]
    if has_file:
        for data in result:
            param_list = data["parameterValues"]
            for item in param_list:
                item["parameterValue"] = json.dumps(
                    {
                        "__file__": {
                            "bucket": "data",
                            "objectKey": f"parameters/{data['parameterName']}/{uuid4().hex}.dat",
                        }
                    }
                )
    return result


@pytest.mark.parametrize(
    "input_dataset_parts",
    [
        pytest.param((None, Tag.input_dataset_observe_frames()), id="empty"),
        pytest.param(
            (input_dataset_frames_part_factory(), Tag.input_dataset_observe_frames()),
            id="single_bucket",
        ),
        pytest.param(
            (input_dataset_frames_part_factory(bucket_count=2), Tag.input_dataset_observe_frames()),
            id="multi_bucket",
        ),
    ],
)
def test_input_dataset_observe_frames_part_document(
    task_with_input_dataset, input_dataset_parts: tuple[Any, str]
):
    """
    Given: A task with an input dataset observe frames part document tagged as such
    When: Accessing the document via the InputDatasetMixIn
    Then: The contents of the file are returned
    """
    doc_part, _ = input_dataset_parts
    task = task_with_input_dataset
    assert task.input_dataset_observe_frames_part_document == doc_part


@pytest.mark.parametrize(
    "input_dataset_parts",
    [
        pytest.param((None, Tag.input_dataset_calibration_frames()), id="empty"),
        pytest.param(
            (input_dataset_frames_part_factory(), Tag.input_dataset_calibration_frames()),
            id="single_bucket",
        ),
        pytest.param(
            (
                input_dataset_frames_part_factory(bucket_count=2),
                Tag.input_dataset_calibration_frames(),
            ),
            id="multi_bucket",
        ),
    ],
)
def test_input_dataset_calibration_frames_part_document(
    task_with_input_dataset, input_dataset_parts: tuple[Any, str]
):
    """
    Given: A task with an input dataset calibration frames part document tagged as such
    When: Accessing the document via the InputDatasetMixIn
    Then: The contents of the file are returned
    """
    doc_part, _ = input_dataset_parts
    task = task_with_input_dataset
    assert task.input_dataset_calibration_frames_part_document == doc_part


@pytest.mark.parametrize(
    "input_dataset_parts",
    [
        pytest.param((None, Tag.input_dataset_parameters()), id="empty"),
        pytest.param(
            (input_dataset_parameters_part_factory(), Tag.input_dataset_parameters()),
            id="single_param_no_date",
        ),
        pytest.param(
            (
                input_dataset_parameters_part_factory(parameter_count=2),
                Tag.input_dataset_parameters(),
            ),
            id="multi_param_no_date",
        ),
        pytest.param(
            (input_dataset_parameters_part_factory(has_date=True), Tag.input_dataset_parameters()),
            id="single_param_with_date",
        ),
        pytest.param(
            (
                input_dataset_parameters_part_factory(parameter_count=2, has_date=True),
                Tag.input_dataset_parameters(),
            ),
            id="multi_param_with_date",
        ),
    ],
)
def test_input_dataset_parameters_part_document(
    task_with_input_dataset, input_dataset_parts: tuple[Any, str]
):
    """
    Given: A task with an input dataset parameters part document tagged as such
    When: Accessing the document via the InputDatasetMixIn
    Then: The contents of the file are returned
    """
    doc_part, _ = input_dataset_parts
    task = task_with_input_dataset
    assert task.input_dataset_parameters_part_document == doc_part


@pytest.mark.parametrize(
    "input_dataset_parts",
    [
        pytest.param(
            [
                (input_dataset_frames_part_factory(), Tag.input_dataset_observe_frames()),
                (input_dataset_frames_part_factory(), Tag.input_dataset_calibration_frames()),
            ],
            id="observe1_cal1_single_bucket",
        ),
        pytest.param(
            [
                (input_dataset_frames_part_factory(), Tag.input_dataset_observe_frames()),
                (None, Tag.input_dataset_calibration_frames()),
            ],
            id="observe1_cal0_single_bucket",
        ),
        pytest.param(
            [
                (None, Tag.input_dataset_observe_frames()),
                (input_dataset_frames_part_factory(), Tag.input_dataset_calibration_frames()),
            ],
            id="observe0_cal1_single_bucket",
        ),
        pytest.param(
            [
                (None, Tag.input_dataset_observe_frames()),
                (None, Tag.input_dataset_calibration_frames()),
            ],
            id="observe0_cal0_single_bucket",
        ),
        pytest.param(
            [
                (
                    input_dataset_frames_part_factory(bucket_count=2),
                    Tag.input_dataset_observe_frames(),
                ),
                (
                    input_dataset_frames_part_factory(bucket_count=2),
                    Tag.input_dataset_calibration_frames(),
                ),
            ],
            id="observe1_cal1_multi_bucket",
        ),
        pytest.param(
            [
                (
                    input_dataset_frames_part_factory(bucket_count=2),
                    Tag.input_dataset_observe_frames(),
                ),
                (None, Tag.input_dataset_calibration_frames()),
            ],
            id="observe1_cal0_multi_bucket",
        ),
        pytest.param(
            [
                (None, Tag.input_dataset_observe_frames()),
                (
                    input_dataset_frames_part_factory(bucket_count=2),
                    Tag.input_dataset_calibration_frames(),
                ),
            ],
            id="observe0_cal1_multi_bucket",
        ),
        pytest.param(
            [
                (None, Tag.input_dataset_observe_frames()),
                (None, Tag.input_dataset_calibration_frames()),
            ],
            id="observe0_cal0_multi_bucket",
        ),
    ],
)
def test_input_dataset_frames(task_with_input_dataset, input_dataset_parts: list[tuple[Any, str]]):
    """
    Given: a task with the InputDatasetMixin
    When: getting the frames in the input dataset
    Then: it matches the frames used to create the input dataset
    """
    doc_parts = [part for part, _ in input_dataset_parts]
    task = task_with_input_dataset
    expected = []
    for part in doc_parts:
        if part:
            expected.extend(flatten_frame_parts(part))
    expected_set = set(expected)
    actual = [(frame.bucket, frame.object_key) for frame in task.input_dataset_frames]
    actual_set = set(actual)
    assert len(actual) == len(actual_set)
    assert actual_set.difference(expected_set) == set()


@pytest.mark.parametrize(
    "input_dataset_parts",
    [
        pytest.param((None, Tag.input_dataset_parameters()), id="empty"),
        pytest.param(
            (input_dataset_parameters_part_factory(), Tag.input_dataset_parameters()),
            id="single_param_no_date_no_file",
        ),
        pytest.param(
            (input_dataset_parameters_part_factory(has_file=True), Tag.input_dataset_parameters()),
            id="single_param_no_date",
        ),
        pytest.param(
            (
                input_dataset_parameters_part_factory(parameter_count=2, has_file=True),
                Tag.input_dataset_parameters(),
            ),
            id="multi_param_no_date",
        ),
        pytest.param(
            (
                input_dataset_parameters_part_factory(parameter_value_count=2, has_file=True),
                Tag.input_dataset_parameters(),
            ),
            id="multi_param_values_no_date",
        ),
        pytest.param(
            (
                input_dataset_parameters_part_factory(has_date=True, has_file=True),
                Tag.input_dataset_parameters(),
            ),
            id="single_param_with_date",
        ),
        pytest.param(
            (
                input_dataset_parameters_part_factory(
                    parameter_count=2, has_date=True, has_file=True
                ),
                Tag.input_dataset_parameters(),
            ),
            id="multi_param_with_date",
        ),
    ],
)
def test_input_dataset_parameters(
    task_with_input_dataset, input_dataset_parts: list[tuple[Any, str]]
):
    """
    Given: a task with the InputDatasetMixin
    When: getting the parameters in the input dataset
    Then: the names of the parameters match the keys in the returned dictionary
    """
    task = task_with_input_dataset
    doc_part, _ = input_dataset_parts
    doc_part = doc_part or []  # None case parsing of expected values
    """
    expected_parameters is a dict with the parameter names as the keys
    and the values are a list of value dicts for each parameter:
    expected_parameters =
        { 'parameter_name_1': [param_dict_1, param_dict_2, ...],
          'parameter_name_2': [param_dict_1, param_dict_2, ...],
           ...
        }
    where the param_dicts have the following format:
    sample_param_dict =
        { "parameterValueId": <param_id>,
          "parameterValue": <param_value>,
          "parameterValueStartDate": <start_date>
        }
    """
    expected_parameters = dict()
    for item in doc_part:
        expected_parameters[item["parameterName"]] = item["parameterValues"]
    create_parameter_files(task, expected_parameters)
    # key is param name, values is list of InputDatasetParameterValue objects
    for key, values in task.input_dataset_parameters.items():
        assert key in expected_parameters
        expected_values = expected_parameters[key]
        # Iterate through multiple values if they exist
        for value in values:
            # Find the matching expected value for this value object
            expected_value = [
                item
                for item in expected_values
                if value.parameter_value_id == item["parameterValueId"]
            ]
            # Make sure there's only one value
            assert len(expected_value) == 1
            # Now check the value
            expected_value = expected_value[0]
            assert value.parameter_value == json.loads(
                expected_value["parameterValue"], object_hook=task._decode_parameter_value
            )
            expected_date = expected_value.get("parameterValueStartDate", datetime(1, 1, 1))
            assert value.parameter_value_start_date == expected_date


@pytest.mark.parametrize(
    "input_dataset_parts",
    [
        pytest.param((None, Tag.input_dataset_parameters()), id="empty"),
        pytest.param(
            (input_dataset_parameters_part_factory(), Tag.input_dataset_parameters()),
            id="single_param_no_date_no_file",
        ),
        pytest.param(
            (input_dataset_parameters_part_factory(has_file=True), Tag.input_dataset_parameters()),
            id="single_param_no_date",
        ),
        pytest.param(
            (
                input_dataset_parameters_part_factory(parameter_count=2, has_file=True),
                Tag.input_dataset_parameters(),
            ),
            id="multi_param_no_date",
        ),
        pytest.param(
            (
                input_dataset_parameters_part_factory(parameter_value_count=2, has_file=True),
                Tag.input_dataset_parameters(),
            ),
            id="multi_param_values_no_date",
        ),
        pytest.param(
            (
                input_dataset_parameters_part_factory(has_date=True, has_file=True),
                Tag.input_dataset_parameters(),
            ),
            id="single_param_with_date",
        ),
        pytest.param(
            (
                input_dataset_parameters_part_factory(
                    parameter_count=2, has_date=True, has_file=True
                ),
                Tag.input_dataset_parameters(),
            ),
            id="multi_param_with_date",
        ),
    ],
)
def test_input_dataset_parameter_objects(
    task_with_input_dataset, input_dataset_parts: list[tuple[Any, str]]
):
    """
    Given: a task with the InputDatasetMixin
    When: getting the parameters objects in the input dataset
    Then: the InputDatsetObjects returned by the task method match the objects defined by the input
        dataset doc part
    """
    task = task_with_input_dataset
    doc_part, _ = input_dataset_parts
    doc_part = doc_part or []  # None case parsing of expected values

    # Create a list of InputDatasetObjects from the input dataset doc part
    expected_parameters = list()
    for param_item in doc_part:
        param_values_list = param_item["parameterValues"]
        for param_value_dict in param_values_list:
            if "__file__" in param_value_dict["parameterValue"]:
                file_dict = json.loads(
                    param_value_dict["parameterValue"], object_hook=task._decode_parameter_value
                )
                expected_parameters.append(
                    InputDatasetObject(
                        bucket=file_dict["bucket"], object_key=file_dict["objectKey"]
                    )
                )
    # Check that each InputDatasetObject returned by the task is in the list of expected parameters
    input_dataset_parameter_objects = task.input_dataset_parameter_objects
    assert len(input_dataset_parameter_objects) == len(expected_parameters)
    for input_dataset_object in input_dataset_parameter_objects:
        assert input_dataset_object in expected_parameters


@pytest.mark.parametrize(
    "input_parameter_dict",
    [
        {"bucket": "data", "objectKey": "parameters/805c46/714ff939158b4253859cde5e5d6f62c3.dat"},
        {
            "__file__": {
                "bucket": "data",
                "objectKey": "parameters/805c46/714ff939158b4253859cde5e5d6f62c3.dat",
            }
        },
        {"key_name_1": "value_1", "key_name_2": "value_2", "key_name_3": "value_3"},
    ],
)
def test_convert_parameter_file_to_path(recipe_run_id, input_parameter_dict: dict):
    """
    Given: a parameter value field to be json decoded
    When: passing the parameter value string to the json decoder hook
    Then: the hook passes non-file parameter strings without change and modifies file parameter strings
        by replacing the __file__ dict in the value string with a bucket field, an objectKey field
        and adds a param_path field and an is_file field
    """
    # Initial test with no tags
    with InputDatasetTask(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        # Test with no tags...
        input_dict = input_parameter_dict
        output_dict = task._decode_parameter_value(input_dict)
        if "__file__" not in input_dict:
            assert input_dict == output_dict
        else:
            value_dict = input_dict["__file__"]
            assert output_dict["bucket"] == value_dict["bucket"]
            assert output_dict["objectKey"] == value_dict["objectKey"]
            assert output_dict["is_file"]
            assert output_dict["param_path"] is None
        # Test with tags
        if "__file__" not in input_dict:
            output_dict = task._decode_parameter_value(input_dict)
            assert input_dict == output_dict
        else:
            # Create the destination path
            param_path = input_dict["__file__"]["objectKey"]
            destination_path = task.scratch.absolute_path(param_path)
            if not destination_path.parent.exists():
                destination_path.parent.mkdir(parents=True, exist_ok=True)
            destination_path.write_text(data="")
            task.tag(path=destination_path, tags=Tag.parameter(destination_path.name))
            output_dict = task._decode_parameter_value(input_dict)
            value_dict = input_dict["__file__"]
            assert output_dict["bucket"] == value_dict["bucket"]
            assert output_dict["objectKey"] == value_dict["objectKey"]
            assert output_dict["is_file"]
            assert output_dict["param_path"] == destination_path


@pytest.mark.parametrize(
    "input_dataset_parts",
    [
        pytest.param(
            [
                (input_dataset_frames_part_factory(), Tag.input_dataset_observe_frames()),
                (input_dataset_frames_part_factory(), Tag.input_dataset_observe_frames()),
            ],
            id="observe",
        ),
        pytest.param(
            [
                (input_dataset_frames_part_factory(), Tag.input_dataset_calibration_frames()),
                (input_dataset_frames_part_factory(), Tag.input_dataset_calibration_frames()),
            ],
            id="calibration",
        ),
        pytest.param(
            [
                (input_dataset_frames_part_factory(), Tag.input_dataset_parameters()),
                (input_dataset_frames_part_factory(), Tag.input_dataset_parameters()),
            ],
            id="params",
        ),
    ],
)
def test_multiple_input_dataset_parts(
    task_with_input_dataset, input_dataset_parts: list[tuple[Any, str]]
):
    """
    Given: a task with the InputDatasetMixin and multiple tagged input datasets
    When: reading the input dataset document
    Then: an error is raised
    """
    task = task_with_input_dataset
    with pytest.raises(ValueError):
        task.input_dataset_parameters_part_document
        task.input_dataset_observe_frames_part_document
        task.input_dataset_calibration_frames_part_document
