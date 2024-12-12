import json
from pathlib import Path
from uuid import uuid4

import pytest
from pydantic.dataclasses import dataclass as validating_dataclass

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem
from dkist_processing_common.tasks.trial_output_data import TransferTrialData
from dkist_processing_common.tests.conftest import FakeGQLClient


@pytest.fixture
def destination_bucket() -> str:
    return "wild"


@pytest.fixture
def recipe_run_configuration(
    custom_root_name,
    custom_dir_name,
    destination_bucket,
):
    class GQLClientWithConfiguration(FakeGQLClient):
        def execute_gql_query(self, **kwargs):
            response = super().execute_gql_query(**kwargs)
            if isinstance(response, list):
                if isinstance(response[0], RecipeRunResponse):
                    response[0].configuration = json.dumps(
                        {
                            "trial_root_directory_name": custom_root_name,
                            "trial_directory_name": custom_dir_name,
                            "destination_bucket": destination_bucket,
                        }
                    )
            return response

    return GQLClientWithConfiguration


@pytest.fixture
def recipe_run_configuration_with_tag_lists(
    custom_root_name, custom_dir_name, destination_bucket, exclusive_tag_lists
):
    class GQLClientWithConfiguration(FakeGQLClient):
        def execute_gql_query(self, **kwargs):
            response = super().execute_gql_query(**kwargs)
            if isinstance(response, list):
                if isinstance(response[0], RecipeRunResponse):
                    response[0].configuration = json.dumps(
                        {
                            "trial_root_directory_name": custom_root_name,
                            "trial_directory_name": custom_dir_name,
                            "destination_bucket": destination_bucket,
                            "trial_exclusive_transfer_tag_lists": exclusive_tag_lists,
                        }
                    )
            return response

    return GQLClientWithConfiguration


@pytest.fixture
def trial_output_task() -> type[TransferTrialData]:
    return TransferTrialData


@pytest.fixture
def basic_trial_output_task(
    recipe_run_id, recipe_run_configuration, trial_output_task, tmp_path, mocker
):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=recipe_run_configuration,
    )
    proposal_id = "test_proposal_id"
    with trial_output_task(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.constants._update({"PROPOSAL_ID": proposal_id})
        yield task, proposal_id
        task._purge()


@validating_dataclass
class OutputFileObjects:
    """File objects returned by complete_trial_output_task"""

    debug_file_obj: bytes
    intermediate_file_obj: bytes
    dataset_inv_file_obj: bytes
    asdf_file_obj: bytes
    quality_data_obj: bytes
    quality_report_file_obj: bytes
    movie_file_obj: bytes


@validating_dataclass
class OutputFileNames:
    """File names returned by complete_trial_output_task"""

    debug_file_name: str
    intermediate_file_name: str
    dataset_inv_file_name: str
    asdf_file_name: str
    quality_data_name: str
    quality_report_file_name: str
    movie_file_name: str


@pytest.fixture
def complete_trial_output_task(
    request, recipe_run_id, trial_output_task, tmp_path, mocker
) -> tuple[TransferTrialData, str, OutputFileObjects]:
    recipe_run = request.param
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=request.getfixturevalue(recipe_run),
    )
    proposal_id = "test_proposal_id"
    with trial_output_task(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id,
            scratch_base_path=tmp_path,
        )
        task.constants._update({"PROPOSAL_ID": proposal_id})

        # Write a debug frame
        debug_file_obj = uuid4().hex.encode("utf8")
        debug_file_name = "debug.ext"
        task.write(debug_file_obj, relative_path=debug_file_name, tags=[Tag.debug(), Tag.frame()])

        # Write a dataset inventory file
        dataset_inv_file_obj = uuid4().hex.encode("utf8")
        dataset_inv_file_name = "dataset_inv.ext"
        task.write(
            dataset_inv_file_obj,
            relative_path=dataset_inv_file_name,
            tags=[Tag.output(), Tag.dataset_inventory()],
        )

        # Write an asdf file
        asdf_file_obj = uuid4().hex.encode("utf8")
        asdf_file_name = "asdf.ext"
        task.write(asdf_file_obj, relative_path=asdf_file_name, tags=[Tag.output(), Tag.asdf()])

        # Write quality data
        # quality data is not tagged as OUTPUT
        quality_data_obj = uuid4().hex.encode("utf8")
        quality_data_name = "quality_data.json"
        task.write(
            quality_data_obj,
            relative_path=quality_data_name,
            tags=Tag.quality_data(),
        )

        # Write a quality report file
        quality_report_file_obj = uuid4().hex.encode("utf8")
        quality_report_file_name = "quality_report.pdf"
        task.write(
            quality_report_file_obj,
            relative_path=quality_report_file_name,
            tags=[Tag.output(), Tag.quality_report()],
        )

        # Write a movie file
        movie_file_obj = uuid4().hex.encode("utf8")
        movie_file_name = "movie.mp4"
        task.write(movie_file_obj, relative_path=movie_file_name, tags=[Tag.output(), Tag.movie()])

        # Write an intermediate frame
        intermediate_file_obj = uuid4().hex.encode("utf8")
        intermediate_file_name = "intermediate.ext"
        task.write(
            intermediate_file_obj,
            relative_path=intermediate_file_name,
            tags=[Tag.intermediate(), Tag.frame(), Tag.task("TASKY_MCTASKERSON")],
        )

        output_file_objects = OutputFileObjects(
            debug_file_obj=debug_file_obj,
            intermediate_file_obj=intermediate_file_obj,
            dataset_inv_file_obj=dataset_inv_file_obj,
            asdf_file_obj=asdf_file_obj,
            quality_data_obj=quality_data_obj,
            quality_report_file_obj=quality_report_file_obj,
            movie_file_obj=movie_file_obj,
        )

        output_file_names = OutputFileNames(
            debug_file_name=debug_file_name,
            intermediate_file_name=intermediate_file_name,
            dataset_inv_file_name=dataset_inv_file_name,
            asdf_file_name=asdf_file_name,
            quality_data_name=quality_data_name,
            quality_report_file_name=quality_report_file_name,
            movie_file_name=movie_file_name,
        )

        yield task, proposal_id, output_file_objects, output_file_names
        task._purge()


@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name",
    [
        pytest.param("root", "foo", id="Custom trial dir and trial root names"),
        pytest.param(None, None, id="Default trial dir and trial root name"),
    ],
)
def test_format_object_key(
    basic_trial_output_task,
    custom_root_name,
    custom_dir_name,
):
    """
    :Given: A base task made from TransferTrialData
    :When: Formatting a path into an object key
    :Then: The expected object key is produced and includes a custom dir name if requested
    """
    task, proposal_id = basic_trial_output_task
    expected_root_name = custom_root_name or proposal_id
    expected_dir_name = custom_dir_name or task.constants.dataset_id
    filename = "test_filename.ext"
    path = Path(f"a/b/c/d/{filename}")
    assert task.format_object_key(path) == str(
        Path(expected_root_name, expected_dir_name, filename)
    )


@pytest.mark.parametrize("complete_trial_output_task", ["recipe_run_configuration"], indirect=True)
@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name",
    [
        pytest.param(None, None, id="Default trial dir and trial root names"),
        pytest.param(None, "foo", id="Custom trial dir"),
        pytest.param("root", None, id="Custom root name"),
    ],
)
def test_build_transfer_list(
    complete_trial_output_task,
    destination_bucket,
    custom_dir_name,
    custom_root_name,
):
    """
    :Given: A Task based on TransferTrialData
    :When: Building the transfer list with the default tag list
    :Then: The resulting transfer list has the correct type, source and destination paths, and references the correct files
    """
    task, proposal_id, output_file_objects, output_file_names = complete_trial_output_task
    transfer_list = task.build_transfer_list()

    assert len(transfer_list) == 7

    sorted_transfer_list = sorted(transfer_list, key=lambda x: x.source_path.name)
    sorted_output_file_objects = [
        getattr(output_file_objects, key) for key in sorted(vars(output_file_objects))
    ]
    sorted_output_file_names = sorted(vars(output_file_names).values())

    for transfer_item, file_name, file_obj in zip(
        sorted_transfer_list, sorted_output_file_names, sorted_output_file_objects
    ):
        assert isinstance(transfer_item, GlobusTransferItem)
        assert transfer_item.source_path == task.scratch.workflow_base_path / file_name
        expected_destination = Path(
            destination_bucket,
            custom_root_name or proposal_id,
            custom_dir_name or task.constants.dataset_id,
            file_name,
        )
        assert transfer_item.destination_path == expected_destination
        with transfer_item.source_path.open(mode="rb") as f:
            assert file_obj == f.read()


@pytest.mark.parametrize(
    "complete_trial_output_task", ["recipe_run_configuration_with_tag_lists"], indirect=True
)
@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name, exclusive_tag_lists, expected_output",
    [
        pytest.param(
            None,
            None,
            [[Tag.task("TASKY_MCTASKERSON")]],
            "intermediate_file",
            id="Default trial dir and trial root names",
        )
    ],
)
def test_build_transfer_list_with_exclusive_tag_lists(
    complete_trial_output_task,
    destination_bucket,
    custom_dir_name,
    custom_root_name,
    exclusive_tag_lists,
    expected_output,
):
    """
    :Given: A Task based on TransferTrialData
    :When: Building the transfer list while the exclusive tag list is set in the recipe run configuration
    :Then: The resulting transfer list has the correct source and destination path, and references the correct file
    """
    task, proposal_id, output_file_objects, output_file_names = complete_trial_output_task

    transfer_list = task.build_transfer_list()
    assert len(transfer_list) == 1

    file_obj = getattr(output_file_objects, expected_output + "_obj")
    expected_destination_name = getattr(output_file_names, expected_output + "_name")
    expected_destination_path = Path(
        destination_bucket, task.format_object_key(Path(expected_destination_name))
    )

    transfer_item = transfer_list[0]
    assert transfer_item.source_path == task.scratch.workflow_base_path / expected_destination_name
    assert transfer_item.destination_path == expected_destination_path
    with transfer_item.source_path.open(mode="rb") as f:
        assert file_obj == f.read()


@pytest.mark.parametrize(
    "complete_trial_output_task", ["recipe_run_configuration_with_tag_lists"], indirect=True
)
@pytest.mark.parametrize(
    "custom_root_name, custom_dir_name, exclusive_tag_lists",
    [
        pytest.param(
            None, None, [Tag.task("TASKY_MCTASKERSON")], id="Default trial dir and trial root names"
        )
    ],
)
def test_build_transfer_list_with_bad_exclusive_tag_lists(
    complete_trial_output_task,
    destination_bucket,
    custom_dir_name,
    custom_root_name,
    exclusive_tag_lists,
):
    """
    :Given: A Task based on TrialTransferDataBase
    :When: The exclusive tag list is a simple list instead of the required list of lists
    :Then: The correct value error is raised
    """
    task, proposal_id, output_file_objects, output_file_names = complete_trial_output_task

    with pytest.raises(ValueError) as ve:
        transfer_list = task.build_transfer_list()
    assert f"tag_lists={exclusive_tag_lists} must" in str(ve)
