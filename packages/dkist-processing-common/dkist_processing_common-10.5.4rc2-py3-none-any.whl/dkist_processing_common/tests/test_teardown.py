import json
from typing import Type

import pytest

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.str import str_encoder
from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.teardown import Teardown
from dkist_processing_common.tests.conftest import FakeGQLClient


class TeardownTest(Teardown):
    def metadata_store_change_recipe_run_to_completed_successfully(self):
        pass


@pytest.fixture()
def make_mock_GQL_with_configuration():
    def class_generator(configuration: dict):
        class TeardownFakeGQLClient(FakeGQLClient):
            def execute_gql_query(self, **kwargs):
                response = super().execute_gql_query(**kwargs)
                if isinstance(response, list):
                    if isinstance(response[0], RecipeRunResponse):
                        response[0].configuration = json.dumps(configuration)
                return response

        return TeardownFakeGQLClient

    return class_generator


@pytest.fixture(scope="session")
def config_with_teardown_enabled() -> dict:
    return {"teardown_enabled": True}


@pytest.fixture(scope="session")
def config_with_teardown_disabled() -> dict:
    return {"teardown_enabled": False}


@pytest.fixture(scope="session")
def config_with_no_teardown() -> dict:
    return dict()


@pytest.fixture(scope="function")
def teardown_task_factory(tmp_path, recipe_run_id):
    def factory(teardown_task_cls: Type[Teardown]):
        number_of_files = 10
        tag_object = Tag.output()
        filenames = []
        with teardown_task_cls(
            recipe_run_id=recipe_run_id,
            workflow_name="workflow_name",
            workflow_version="workflow_version",
        ) as task:
            task.scratch = WorkflowFileSystem(
                recipe_run_id=recipe_run_id,
                scratch_base_path=tmp_path,
            )
            task.scratch.workflow_base_path = tmp_path / str(recipe_run_id)
            for file_num in range(number_of_files):
                file_path = task.write(f"file_{file_num}", tag_object, encoder=str_encoder)
                filenames.append(file_path.name)

            task.constants._update({"teardown_constant": 1234})

            return task, filenames, tag_object

    yield factory


def test_purge_data(
    teardown_task_factory, make_mock_GQL_with_configuration, config_with_teardown_enabled, mocker
):
    """
    :Given: A Teardown task with files and tags linked to it and teardown enabled
    :When: Running the task
    :Then: All the files are deleted and the tags are removed
    """
    FakeGQLClass = make_mock_GQL_with_configuration(config_with_teardown_enabled)
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClass
    )
    task, filenames, tag_object = teardown_task_factory(TeardownTest)
    tagged_data = list(task.read(tags=tag_object))
    for filepath in tagged_data:
        assert filepath.exists()
    task()
    for filepath in tagged_data:
        assert not filepath.exists()
    post_purge_tagged_data = list(task.read(tags=tag_object))
    assert len(post_purge_tagged_data) == 0
    # audit data removed
    assert not task.scratch._audit_db.tags
    assert not task.constants._db_dict._audit_db.tags
    assert not task.filename_counter.tags


def test_purge_data_disabled(
    teardown_task_factory, make_mock_GQL_with_configuration, config_with_teardown_disabled, mocker
):
    """
    :Given: A Teardown task with files and tags linked to it and teardown disabled
    :When: Running the task
    :Then: All the files are not deleted and the tags remain
    """
    FakeGQLClass = make_mock_GQL_with_configuration(config_with_teardown_disabled)
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClass
    )
    task, filenames, tag_object = teardown_task_factory(TeardownTest)
    tagged_data = list(task.read(tags=tag_object))
    for filepath in tagged_data:
        assert filepath.exists()
    task()
    for filepath in tagged_data:
        assert filepath.exists()  # still exists
    post_purge_tagged_data = list(task.read(tags=tag_object))
    assert len(post_purge_tagged_data) == len(tagged_data)
    # audit data still present
    assert task.scratch._audit_db.tags
    assert task.constants._db_dict._audit_db.tags
    assert task.filename_counter.tags


def test_purge_data_no_config(
    teardown_task_factory, make_mock_GQL_with_configuration, config_with_no_teardown, mocker
):
    """
    :Given: A Teardown task with files and tags linked and teardown not specified in the configuration
    :When: Running the task
    :Then: All the files are deleted and the tags are removed
    """
    FakeGQLClass = make_mock_GQL_with_configuration(config_with_no_teardown)
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClass
    )
    task, filenames, tag_object = teardown_task_factory(TeardownTest)
    tagged_data = list(task.read(tags=tag_object))
    for filepath in tagged_data:
        assert filepath.exists()
    task()
    for filepath in tagged_data:
        assert not filepath.exists()
    post_purge_tagged_data = list(task.read(tags=tag_object))
    assert len(post_purge_tagged_data) == 0
