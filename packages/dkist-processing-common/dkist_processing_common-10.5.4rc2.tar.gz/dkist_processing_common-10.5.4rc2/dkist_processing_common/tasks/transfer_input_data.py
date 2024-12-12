"""Task(s) for the transfer in of data sources for a processing pipeline."""
import logging
from pathlib import Path

from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.base import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.globus import GlobusMixin
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetObject

__all__ = ["TransferL0Data"]

logger = logging.getLogger(__name__)


class TransferL0Data(WorkflowTaskBase, GlobusMixin, InputDatasetMixin):
    """Transfers Level 0 data and required parameter files to the scratch store."""

    def download_input_dataset(self):
        """Get the input dataset document parts and save it to scratch with the appropriate tags."""
        if doc := self.metadata_store_input_dataset_observe_frames_part_document:
            self.write(doc.encode("utf-8"), tags=Tag.input_dataset_observe_frames())
        if doc := self.metadata_store_input_dataset_calibration_frames_part_document:
            self.write(doc.encode("utf-8"), tags=Tag.input_dataset_calibration_frames())
        if doc := self.metadata_store_input_dataset_parameters_part_document:
            self.write(doc.encode("utf-8"), tags=Tag.input_dataset_parameters())

    def format_transfer_items(
        self, input_dataset_objects: list[InputDatasetObject]
    ) -> list[GlobusTransferItem]:
        """Format a list of InputDatasetObject(s) as GlobusTransferItem(s)."""
        transfer_items = []
        for obj in input_dataset_objects:
            source_path = Path("/", obj.bucket, obj.object_key)
            destination_path = self.scratch.absolute_path(obj.object_key)
            transfer_items.append(
                GlobusTransferItem(
                    source_path=source_path,
                    destination_path=destination_path,
                    recursive=False,
                )
            )
        return transfer_items

    def format_frame_transfer_items(self) -> list[GlobusTransferItem]:
        """Format the list of frames as transfer items to be used by globus."""
        return self.format_transfer_items(self.input_dataset_frames)

    def format_parameter_transfer_items(self) -> list[GlobusTransferItem]:
        """Format the list of parameter objects as transfer items to be used by globus."""
        return self.format_transfer_items(self.input_dataset_parameter_objects)

    def tag_input_frames(self, transfer_items: list[GlobusTransferItem]) -> None:
        """
        Tag all the input files with 'frame' and 'input' tags.

        Parameters
        ----------
        transfer_items
            List of items to be tagged

        Returns
        -------
        None
        """
        scratch_items = [
            self.scratch.scratch_base_path / ti.destination_path for ti in transfer_items
        ]
        for si in scratch_items:
            self.tag(si, tags=[Tag.input(), Tag.frame()])

    def tag_parameter_objects(self, transfer_items: list[GlobusTransferItem]) -> None:
        """
        Tag all the parameter files with 'parameter'.

        Parameters
        ----------
        transfer_items
            List of items to be tagged

        Returns
        -------
        None
        """
        scratch_items = [
            self.scratch.scratch_base_path / ti.destination_path for ti in transfer_items
        ]
        for si in scratch_items:
            self.tag(si, tags=[Tag.parameter(si.name)])

    def run(self) -> None:
        """Execute the data transfer."""
        with self.apm_task_step("Change Status to InProgress"):
            self.metadata_store_change_recipe_run_to_inprogress()

        with self.apm_task_step("Download Input Dataset"):
            self.download_input_dataset()

        with self.apm_task_step("Format Frame Transfer Items"):
            frame_transfer_items = self.format_frame_transfer_items()
            if not frame_transfer_items:
                raise ValueError("No input dataset frames found")

        with self.apm_task_step("Format Parameter Transfer Items"):
            parameter_transfer_items = self.format_parameter_transfer_items()

        with self.apm_task_step("Transfer Input Frames and Parameter Files via Globus"):
            self.globus_transfer_object_store_to_scratch(
                transfer_items=frame_transfer_items + parameter_transfer_items,
                label=f"Transfer Inputs for Recipe Run {self.recipe_run_id}",
            )

        with self.apm_processing_step("Tag Input Frames and Parameter Files"):
            self.tag_input_frames(transfer_items=frame_transfer_items)
            self.tag_parameter_objects(transfer_items=parameter_transfer_items)

    def rollback(self):
        """Warn that depending on the progress of the task all data may not be removed because it hadn't been tagged."""
        super().rollback()
        logger.warning(
            f"Rolling back only removes data that has been tagged.  The data persisted by this task may not have been tagged prior to rollback."
        )
