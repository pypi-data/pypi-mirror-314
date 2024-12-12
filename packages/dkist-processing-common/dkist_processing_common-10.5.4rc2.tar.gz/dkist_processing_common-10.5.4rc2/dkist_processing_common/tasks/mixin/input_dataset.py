"""Mixin for a WorkflowDataTaskBase subclass which implements input data set access functionality."""
import json
from dataclasses import dataclass
from datetime import datetime
from itertools import chain
from pathlib import Path
from typing import Any

from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.base import tag_type_hint


frames_part_type_hint = list[dict[str, str | list[str]]] | None


@dataclass
class InputDatasetParameterValue:
    """Data structure for a de-serialized input dataset parameter value."""

    parameter_value_id: int
    parameter_value: Any = None
    parameter_value_start_date: datetime | None = None


@dataclass
class InputDatasetObject:
    """Data structure for a de-serialized input dataset frame."""

    bucket: str
    object_key: str


class InputDatasetMixin:
    """Mixin for WorkflowDataTaskBase that accesses downloaded input dataset part documents."""

    def _input_dataset_part_document(self, tags: tag_type_hint):
        """Get the input dataset document part and deserialize it."""
        paths: list[Path] = list(self.read(tags=tags))
        if not paths:
            return
        if len(paths) > 1:
            raise ValueError(
                f"There are more than one input dataset part documents to parse for {tags=}"
            )
        p = paths[0]
        with p.open(mode="rb") as f:
            return json.load(f)

    @property
    def input_dataset_observe_frames_part_document(self) -> frames_part_type_hint:
        """Get the 'observe frames' part of the input dataset."""
        return self._input_dataset_part_document(tags=Tag.input_dataset_observe_frames())

    @property
    def input_dataset_calibration_frames_part_document(self) -> frames_part_type_hint:
        """Get the 'calibration frames' part of the input dataset."""
        return self._input_dataset_part_document(tags=Tag.input_dataset_calibration_frames())

    @property
    def input_dataset_parameters_part_document(
        self,
    ) -> list[dict[str, str | list[dict[str, int | str]]]] | None:
        """Get the 'parameters' part of the input dataset."""
        return self._input_dataset_part_document(tags=Tag.input_dataset_parameters())

    @property
    def input_dataset_frames(self) -> list[InputDatasetObject]:
        """Get the list of frames for this input dataset."""
        result = []
        observe_frames = self.input_dataset_observe_frames_part_document or []
        calibration_frames = self.input_dataset_calibration_frames_part_document or []
        for frame_set in chain(observe_frames, calibration_frames):
            for key in frame_set.get("object_keys", list()):
                result.append(InputDatasetObject(bucket=frame_set["bucket"], object_key=key))
        return result

    @property
    def input_dataset_parameters(self) -> dict[str, list[InputDatasetParameterValue]]:
        """Get the input dataset parameters."""
        parameters = self.input_dataset_parameters_part_document or []
        result = dict()
        for p in parameters:
            result.update(self._input_dataset_parse_parameter(p))
        return result

    @property
    def input_dataset_parameter_objects(self) -> list[InputDatasetObject]:
        """Parse the parameter object locations out of the set of all parameters."""
        result = []
        for value_list in self.input_dataset_parameters.values():
            for value in value_list:
                param_value = value.parameter_value
                if isinstance(param_value, dict) and param_value.get("is_file", False):
                    result.append(
                        InputDatasetObject(
                            bucket=param_value["bucket"], object_key=param_value["objectKey"]
                        )
                    )
        return result

    def _input_dataset_parse_parameter(
        self, parameter: dict
    ) -> dict[str, list[InputDatasetParameterValue]]:
        name: str = parameter["parameterName"]
        raw_values: list[dict] = parameter["parameterValues"]
        values = self._input_dataset_parse_parameter_values(raw_values=raw_values)
        return {name: values}

    def _input_dataset_parse_parameter_values(
        self, raw_values: list[dict[str, Any]]
    ) -> list[InputDatasetParameterValue]:
        values = list()
        for v in raw_values:
            parsed_value = InputDatasetParameterValue(parameter_value_id=v["parameterValueId"])
            parsed_value.parameter_value = self._input_dataset_parse_parameter_value(
                raw_parameter_value=v["parameterValue"]
            )
            if d := v.get("parameterValueStartDate"):
                parsed_value.parameter_value_start_date = datetime.fromisoformat(d)
            else:
                parsed_value.parameter_value_start_date = datetime(1, 1, 1)
            values.append(parsed_value)
        return values

    def _input_dataset_parse_parameter_value(self, raw_parameter_value: str) -> Any:
        """Return the json decoding of the parameter value."""
        return json.loads(raw_parameter_value, object_hook=self._decode_parameter_value)

    def _decode_parameter_value(self, param_dict: dict):
        """Decode a parameter value."""
        if "__file__" in param_dict:
            return self._convert_parameter_file_value_to_path(param_dict)
        # Nothing to do here, so return control back to json.loads()
        return param_dict

    def _convert_parameter_file_value_to_path(self, param_dict: dict):
        """
        Decode a parameter file value.

        Note: for parameters that are files, the string passed to json.loads() looks like this:
        '{ "__file__":
            {
                "bucket": "data",
                "objectKey": "parameters/parameter_name/uuid.dat"
            }
        }'

        In this hook, we remove the outer __file__ dict and return the inner dict with the addition of
        a key and value for the file path. Because the file path is dependent on the existence of a tag,
        if no tag is found, None is returned for the path. This use case will occur when we construct
        the list of files to be transferred and tagged by the TransferL0Data task.
        """
        file_dict = param_dict["__file__"]
        object_key = file_dict["objectKey"]
        parameter_tag = Tag.parameter(Path(object_key).name)
        paths = list(self.read(tags=parameter_tag))
        num_paths = len(paths)
        if num_paths == 1:
            param_path = paths[0]
        elif num_paths == 0:
            param_path = None
        else:
            raise ValueError(f"Found multiple paths for {parameter_tag = }.")
        file_dict["param_path"] = param_path
        file_dict["is_file"] = True
        return file_dict
