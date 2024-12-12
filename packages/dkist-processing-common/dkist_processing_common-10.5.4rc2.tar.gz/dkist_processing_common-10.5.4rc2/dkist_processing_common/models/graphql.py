"""GraphQL Data models for the metadata store api."""
from dataclasses import dataclass


@dataclass
class RecipeRunMutation:
    """Recipe run mutation record."""

    recipeRunId: int
    recipeRunStatusId: int


@dataclass
class RecipeRunStatusQuery:
    """Recipe run status query for the recipeRunStatuses endpoint."""

    recipeRunStatusName: str


@dataclass
class RecipeRunStatusMutation:
    """Recipe run status mutation record."""

    recipeRunStatusName: str
    isComplete: bool
    recipeRunStatusDescription: str


@dataclass
class RecipeRunStatusResponse:
    """Response to a recipe run status query."""

    recipeRunStatusId: int


@dataclass
class InputDatasetPartTypeResponse:
    """Response class for the input dataset part type entity."""

    inputDatasetPartTypeName: str


@dataclass
class InputDatasetPartResponse:
    """Response class for the input dataset part entity."""

    inputDatasetPartId: int
    inputDatasetPartDocument: str
    inputDatasetPartType: InputDatasetPartTypeResponse


@dataclass
class InputDatasetInputDatasetPartResponse:
    """Response class for the join entity between input datasets and input dataset parts."""

    inputDatasetPart: InputDatasetPartResponse


@dataclass
class InputDatasetResponse:
    """Input dataset query response."""

    inputDatasetId: int
    isActive: bool
    inputDatasetInputDatasetParts: list[InputDatasetInputDatasetPartResponse]


@dataclass
class InputDatasetRecipeInstanceResponse:
    """Recipe instance query response."""

    inputDataset: InputDatasetResponse


@dataclass
class InputDatasetRecipeRunResponse:
    """Recipe run query response."""

    recipeInstance: InputDatasetRecipeInstanceResponse


@dataclass
class RecipeInstanceResponse:
    """Recipe instance query response."""

    recipeId: int
    inputDatasetId: int


@dataclass
class RecipeRunProvenanceResponse:
    """Response for the metadata store recipeRunProvenances and mutations endpoints."""

    recipeRunProvenanceId: int
    isTaskManual: bool


@dataclass
class RecipeRunResponse:
    """Recipe run query response."""

    recipeInstance: RecipeInstanceResponse
    recipeInstanceId: int
    recipeRunProvenances: list[RecipeRunProvenanceResponse]
    configuration: str = None


@dataclass
class RecipeRunMutationResponse:
    """Recipe run mutation response."""

    recipeRunId: int


@dataclass
class RecipeRunQuery:
    """Query parameters for the metadata store endpoint recipeRuns."""

    recipeRunId: int


@dataclass
class DatasetCatalogReceiptAccountMutation:
    """
    Dataset catalog receipt account mutation record.

    It sets an expected object count for a dataset so that dataset inventory creation
    doesn't happen until all objects are transferred and inventoried.
    """

    datasetId: str
    expectedObjectCount: int


@dataclass
class DatasetCatalogReceiptAccountResponse:
    """Dataset catalog receipt account response for query and mutation endpoints."""

    datasetCatalogReceiptAccountId: int


@dataclass
class RecipeRunProvenanceMutation:
    """Recipe run provenance mutation record."""

    inputDatasetId: int
    isTaskManual: bool
    recipeRunId: int
    taskName: str
    libraryVersions: str
    workflowVersion: str
    codeVersion: str = None


@dataclass
class QualityCreation:
    """Quality data creation record."""

    datasetId: str
    metricCode: str
    facet: str | None = None
    name: str | None = None
    description: str | None = None
    statement: str | None = None
    # JSON array
    warnings: str | None = None
    # JSON objects
    plotData: str | None = None
    tableData: str | None = None
    histogramData: str | None = None
    modmatData: str | None = None
    raincloudData: str | None = None
    efficiencyData: str | None = None


@dataclass
class QualitiesRequest:
    """Query parameters for quality data."""

    datasetId: str


@dataclass
class QualityResponse:
    """Query Response for quality data."""

    qualityId: int
