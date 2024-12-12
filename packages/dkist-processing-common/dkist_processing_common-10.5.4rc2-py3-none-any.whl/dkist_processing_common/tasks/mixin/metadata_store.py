"""Mixin for a WorkflowDataTaskBase subclass which implements Metadata Store data access functionality."""
import json
import logging
from functools import cached_property

from dkist_processing_common._util.graphql import GraphQLClient
from dkist_processing_common.codecs.quality import QualityDataEncoder
from dkist_processing_common.config import common_configurations
from dkist_processing_common.models.graphql import DatasetCatalogReceiptAccountMutation
from dkist_processing_common.models.graphql import DatasetCatalogReceiptAccountResponse
from dkist_processing_common.models.graphql import InputDatasetPartResponse
from dkist_processing_common.models.graphql import InputDatasetRecipeRunResponse
from dkist_processing_common.models.graphql import QualitiesRequest
from dkist_processing_common.models.graphql import QualityCreation
from dkist_processing_common.models.graphql import QualityResponse
from dkist_processing_common.models.graphql import RecipeRunMutation
from dkist_processing_common.models.graphql import RecipeRunMutationResponse
from dkist_processing_common.models.graphql import RecipeRunProvenanceMutation
from dkist_processing_common.models.graphql import RecipeRunProvenanceResponse
from dkist_processing_common.models.graphql import RecipeRunQuery
from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.models.graphql import RecipeRunStatusMutation
from dkist_processing_common.models.graphql import RecipeRunStatusQuery
from dkist_processing_common.models.graphql import RecipeRunStatusResponse


logger = logging.getLogger(__name__)

input_dataset_part_document_type_hint = list | dict | str | int | float | None


class MetadataStoreMixin:
    """Mixin for a WorkflowDataTaskBase which implements Metadata Store access functionality."""

    @property
    def metadata_store_client(self) -> GraphQLClient:
        """Get the graphql client."""
        return GraphQLClient(common_configurations.metadata_store_api_base)

    def metadata_store_change_recipe_run_to_inprogress(self):
        """Set the recipe run status to "INPROGRESS"."""
        self._metadata_store_change_status(status="INPROGRESS", is_complete=False)

    def metadata_store_change_recipe_run_to_completed_successfully(self):
        """Set the recipe run status to "COMPLETEDSUCCESSFULLY"."""
        self._metadata_store_change_status(status="COMPLETEDSUCCESSFULLY", is_complete=True)

    def metadata_store_change_recipe_run_to_trial_success(self):
        """Set the recipe run status to "TRIALSUCCESS"."""
        self._metadata_store_change_status(status="TRIALSUCCESS", is_complete=False)

    def metadata_store_add_dataset_receipt_account(
        self, dataset_id: str, expected_object_count: int
    ):
        """Set the number of expected objects."""
        params = DatasetCatalogReceiptAccountMutation(
            datasetId=dataset_id, expectedObjectCount=expected_object_count
        )
        self.metadata_store_client.execute_gql_mutation(
            mutation_base="createDatasetCatalogReceiptAccount",
            mutation_parameters=params,
            mutation_response_cls=DatasetCatalogReceiptAccountResponse,
        )

    def metadata_store_record_provenance(self, is_task_manual: bool, library_versions: str):
        """Record the provenance record in the metadata store."""
        params = RecipeRunProvenanceMutation(
            inputDatasetId=self.metadata_store_input_dataset_id,
            isTaskManual=is_task_manual,
            recipeRunId=self.recipe_run_id,
            taskName=self.task_name,
            libraryVersions=library_versions,
            workflowVersion=self.workflow_version,
        )
        self.metadata_store_client.execute_gql_mutation(
            mutation_base="createRecipeRunProvenance",
            mutation_parameters=params,
            mutation_response_cls=RecipeRunProvenanceResponse,
        )

    def metadata_store_add_quality_data(self, dataset_id: str, quality_data: list[dict]):
        """Add the quality data to the metadata-store."""
        if self.metadata_store_quality_data_exists(dataset_id):
            raise RuntimeError(f"Quality data already persisted for dataset {dataset_id!r}")
        for metric in quality_data:
            if (metric_code := metric.get("metric_code")) is None:
                name = metric.get("name")
                raise ValueError(f"No metric_code for {name!r} in dataset {dataset_id!r}")
            params = QualityCreation(
                datasetId=dataset_id,
                metricCode=metric_code,
                facet=metric.get("facet"),
                name=metric.get("name"),
                description=metric.get("description"),
                statement=metric.get("statement"),
                # JSON array
                warnings=json.dumps(metric.get("warnings")),
                # JSON objects
                plotData=json.dumps(metric.get("plot_data"), cls=QualityDataEncoder),
                tableData=json.dumps(metric.get("table_data"), cls=QualityDataEncoder),
                histogramData=json.dumps(metric.get("histogram_data"), cls=QualityDataEncoder),
                modmatData=json.dumps(metric.get("modmat_data"), cls=QualityDataEncoder),
                raincloudData=json.dumps(metric.get("raincloud_data"), cls=QualityDataEncoder),
                efficiencyData=json.dumps(metric.get("efficiency_data"), cls=QualityDataEncoder),
            )
            self.metadata_store_client.execute_gql_mutation(
                mutation_base="createQuality",
                mutation_parameters=params,
                mutation_response_cls=QualityResponse,
            )

    def metadata_store_quality_data_exists(self, dataset_id: str) -> bool:
        """Return True if quality data exists in the metadata-store for the given dataset id."""
        params = QualitiesRequest(datasetId=dataset_id)
        response = self.metadata_store_client.execute_gql_query(
            query_base="qualities",
            query_response_cls=QualityResponse,
            query_parameters=params,
        )
        return bool(response)

    def metadata_store_recipe_run_configuration(self) -> dict:
        """Get the recipe run configuration from the metadata store."""
        configuration_json = self._metadata_store_recipe_run().configuration
        if configuration_json is None:
            return {}
        try:
            configuration = json.loads(configuration_json)
            if not isinstance(configuration, dict):
                raise ValueError(
                    f"Invalid recipe run configuration format.  "
                    f"Expected json encoded dictionary, received json encoded {type(configuration)}"
                )
            return configuration
        except (json.JSONDecodeError, ValueError, TypeError, UnicodeDecodeError) as e:
            logger.error(f"Invalid recipe run configuration")
            raise e

    @cached_property
    def metadata_store_input_dataset_parts(self) -> list[InputDatasetPartResponse]:
        """Get the input dataset parts from the metadata store."""
        params = RecipeRunQuery(recipeRunId=self.recipe_run_id)
        response = self.metadata_store_client.execute_gql_query(
            query_base="recipeRuns",
            query_response_cls=InputDatasetRecipeRunResponse,
            query_parameters=params,
        )  # queried independently of other recipe run metadata for performance
        recipe_run = response[0]
        return [
            part_link.inputDatasetPart
            for part_link in recipe_run.recipeInstance.inputDataset.inputDatasetInputDatasetParts
        ]

    def _metadata_store_filter_input_dataset_parts(
        self, input_dataset_part_type_name: str
    ) -> InputDatasetPartResponse | list[InputDatasetPartResponse] | None:
        """Filter the input dataset parts based on the input dataset part type name."""
        target_parts = [
            part
            for part in self.metadata_store_input_dataset_parts
            if part.inputDatasetPartType.inputDatasetPartTypeName == input_dataset_part_type_name
        ]
        if not target_parts:
            return
        if len(target_parts) == 1:
            return target_parts[0]
        raise ValueError(
            f"Multiple ({len(target_parts)}) input dataset parts found for "
            f"{input_dataset_part_type_name=}."
        )

    @property
    def _metadata_store_input_dataset_observe_frames_part(
        self,
    ) -> InputDatasetPartResponse | None:
        """Get the input dataset part for observe frames."""
        return self._metadata_store_filter_input_dataset_parts(
            input_dataset_part_type_name="observe_frames",
        )

    @property
    def metadata_store_input_dataset_observe_frames_part_id(self) -> int | None:
        """Get the input dataset part id for observe frames."""
        if part := self._metadata_store_input_dataset_observe_frames_part:
            return part.inputDatasetPartId

    @property
    def metadata_store_input_dataset_observe_frames_part_document(
        self,
    ) -> input_dataset_part_document_type_hint:
        """Get the input dataset part document for observe frames."""
        if part := self._metadata_store_input_dataset_observe_frames_part:
            return part.inputDatasetPartDocument

    @property
    def _metadata_store_input_dataset_calibration_frames_part(
        self,
    ) -> InputDatasetPartResponse | None:
        """Get the input dataset part for calibration frames."""
        return self._metadata_store_filter_input_dataset_parts(
            input_dataset_part_type_name="calibration_frames"
        )

    @property
    def metadata_store_input_dataset_calibration_frames_part_id(self) -> int | None:
        """Get the input dataset part id for calibration frames."""
        if part := self._metadata_store_input_dataset_calibration_frames_part:
            return part.inputDatasetPartId

    @property
    def metadata_store_input_dataset_calibration_frames_part_document(
        self,
    ) -> input_dataset_part_document_type_hint:
        """Get the input dataset part document for calibration frames."""
        if part := self._metadata_store_input_dataset_calibration_frames_part:
            return part.inputDatasetPartDocument

    @property
    def _metadata_store_input_dataset_parameters_part(
        self,
    ) -> InputDatasetPartResponse | None:
        """Get the input dataset part for parameters."""
        return self._metadata_store_filter_input_dataset_parts(
            input_dataset_part_type_name="parameters"
        )

    @property
    def metadata_store_input_dataset_parameters_part_id(self) -> int | None:
        """Get the input dataset part id for parameters."""
        if part := self._metadata_store_input_dataset_parameters_part:
            return part.inputDatasetPartId

    @property
    def metadata_store_input_dataset_parameters_part_document(
        self,
    ) -> input_dataset_part_document_type_hint:
        """Get the input dataset part document for parameters."""
        if part := self._metadata_store_input_dataset_parameters_part:
            return part.inputDatasetPartDocument

    @property
    def metadata_store_input_dataset_id(self) -> int:
        """Get the input dataset id from the metadata store."""
        return self._metadata_store_recipe_run().recipeInstance.inputDatasetId

    @property
    def metadata_store_recipe_instance_id(self) -> int:
        """Get the recipe instance id from the metadata store."""
        return self._metadata_store_recipe_run().recipeInstanceId

    @property
    def metadata_store_recipe_id(self) -> int:
        """Get the recipe id from the metadata store."""
        return self._metadata_store_recipe_run().recipeInstance.recipeId

    @property
    def metadata_store_recipe_run_provenance(self) -> list[RecipeRunProvenanceResponse]:
        """Get all the provenance records for the recipe run."""
        return self._metadata_store_recipe_run().recipeRunProvenances

    def _metadata_store_recipe_run(self, allow_cache: bool = True) -> RecipeRunResponse:
        is_cached = bool(getattr(self, "_recipe_run_cache", False))
        if is_cached and allow_cache:
            return self._recipe_run_cache
        params = RecipeRunQuery(recipeRunId=self.recipe_run_id)
        response = self.metadata_store_client.execute_gql_query(
            query_base="recipeRuns",
            query_response_cls=RecipeRunResponse,
            query_parameters=params,
        )
        self._recipe_run_cache = response[0]
        return self._recipe_run_cache

    def _metadata_store_change_status(self, status: str, is_complete: bool):
        """Change the recipe run status of a recipe run to the given status."""
        recipe_run_status_id = self._metadata_store_recipe_run_status_id(status=status)
        if not recipe_run_status_id:
            recipe_run_status_id = self._metadata_store_create_recipe_run_status(
                status=status, is_complete=is_complete
            )
        self._metadata_store_update_status(recipe_run_status_id=recipe_run_status_id)

    def _metadata_store_recipe_run_status_id(self, status: str) -> None | int:
        """Find the id of a recipe run status."""
        params = RecipeRunStatusQuery(recipeRunStatusName=status)
        response = self.metadata_store_client.execute_gql_query(
            query_base="recipeRunStatuses",
            query_response_cls=RecipeRunStatusResponse,
            query_parameters=params,
        )
        if len(response) > 0:
            return response[0].recipeRunStatusId

    def _metadata_store_create_recipe_run_status(self, status: str, is_complete: bool) -> int:
        """
        Add a new recipe run status to the db.

        :param status: name of the status to add
        :param is_complete: does the new status correspond to an accepted completion state
        """
        recipe_run_statuses = {
            "INPROGRESS": "Recipe run is currently undergoing processing",
            "COMPLETEDSUCCESSFULLY": "Recipe run processing completed with no errors",
            "TRIALSUCCESS": "Recipe run trial processing completed with no errors. Recipe run not "
            "marked complete.",
        }

        if not isinstance(status, str):
            raise TypeError(f"status must be of type str: {status}")
        if not isinstance(is_complete, bool):
            raise TypeError(f"is_complete must be of type bool: {is_complete}")
        params = RecipeRunStatusMutation(
            recipeRunStatusName=status,
            isComplete=is_complete,
            recipeRunStatusDescription=recipe_run_statuses[status],
        )
        recipe_run_status_response = self.metadata_store_client.execute_gql_mutation(
            mutation_base="createRecipeRunStatus",
            mutation_response_cls=RecipeRunStatusResponse,
            mutation_parameters=params,
        )
        return recipe_run_status_response.recipeRunStatus.recipeRunStatusId

    def _metadata_store_update_status(
        self,
        recipe_run_status_id: int,
    ):
        """
        Change the status of a given recipe run id.

        :param recipe_run_status_id: the new status to use
        """
        params = RecipeRunMutation(
            recipeRunId=self.recipe_run_id, recipeRunStatusId=recipe_run_status_id
        )
        self.metadata_store_client.execute_gql_mutation(
            mutation_base="updateRecipeRun",
            mutation_parameters=params,
            mutation_response_cls=RecipeRunMutationResponse,
        )
