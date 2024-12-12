from dataclasses import asdict
from dataclasses import dataclass
from typing import Literal
from unittest.mock import Mock

import astropy.units as u
import numpy as np
import pytest
from astropy.coordinates import EarthLocation
from astropy.io import fits
from astropy.time import Time
from astropy.time import TimeDelta
from dkist_fits_specifications import __version__ as spec_version
from dkist_header_validator import spec214_validator

from dkist_processing_common import __version__ as common_version
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.codecs.fits import fits_hdu_decoder
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.models.graphql import RecipeRunProvenanceResponse
from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.models.wavelength import WavelengthRange
from dkist_processing_common.tasks.write_l1 import WriteL1Frame
from dkist_processing_common.tests.conftest import FakeGQLClient
from dkist_processing_common.tests.conftest import FakeGQLClientNoRecipeConfiguration
from dkist_processing_common.tests.conftest import TILE_SIZE


class CompleteWriteL1Frame(WriteL1Frame):
    def add_dataset_headers(
        self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"]
    ) -> fits.Header:
        # Because all these keys aren't part of SPEC-122
        header["DAAXES"] = 2
        header["DEAXES"] = 3
        header["DNAXIS"] = 5
        header["FRAMEWAV"] = 123.45
        header["LEVEL"] = 1
        header["WAVEREF"] = "Air"
        header["WAVEUNIT"] = -9
        header["DINDEX3"] = 3
        header["DINDEX4"] = 2
        header["DINDEX5"] = 1
        header["DNAXIS1"] = header["NAXIS1"]
        header["DNAXIS2"] = header["NAXIS2"]
        header["DNAXIS3"] = 10
        header["DNAXIS4"] = 1
        header["DNAXIS5"] = 4
        header["DPNAME1"] = ""
        header["DPNAME2"] = ""
        header["DPNAME3"] = ""
        header["DPNAME4"] = ""
        header["DPNAME5"] = ""
        header["DTYPE1"] = "SPATIAL"
        header["DTYPE2"] = "SPATIAL"
        header["DTYPE3"] = "TEMPORAL"
        header["DTYPE4"] = "SPECTRAL"
        header["DTYPE5"] = "STOKES"
        header["DUNIT1"] = ""
        header["DUNIT2"] = ""
        header["DUNIT3"] = ""
        header["DUNIT4"] = ""
        header["DUNIT5"] = ""
        header["DWNAME1"] = ""
        header["DWNAME2"] = ""
        header["DWNAME3"] = ""
        header["DWNAME4"] = ""
        header["DWNAME5"] = ""
        header["NBIN"] = 1
        for i in range(1, header["NAXIS"] + 1):
            header[f"NBIN{i}"] = 1

        header["VSPNMAPS"] = 1
        header["VSPMAP"] = 1
        header["POL_NOIS"] = 1.0
        header["POL_SENS"] = 1.0

        return header

    def calculate_date_end(self, header: fits.Header) -> str:
        start_time = Time(header["DATE-BEG"], format="isot", precision=6)
        exposure = TimeDelta(float(header["TEXPOSUR"]) / 1000, format="sec")
        return (start_time + exposure).to_value("isot")

    def get_wavelength_range(self, header: fits.Header) -> WavelengthRange:
        return WavelengthRange(min=1075.0 * u.nm, max=1085.0 * u.nm)


@dataclass
class FakeConstantDb:
    INSTRUMENT: str = "TEST"
    DATASET_ID: str = "DATASETID"
    AVERAGE_CADENCE: float = 10.0
    MINIMUM_CADENCE: float = 10.0
    MAXIMUM_CADENCE: float = 10.0
    VARIANCE_CADENCE: float = 0.0
    STOKES_PARAMS: tuple = ("I", "Q", "U", "V")
    PROPOSAL_ID: str = ("PROPID1",)
    CONTRIBUTING_PROPOSAL_IDS: tuple = (("PROPID1"),)
    EXPERIMENT_ID: str = ("EXPERID1",)
    CONTRIBUTING_EXPERIMENT_IDS: tuple = ("EXPERID1", "EXPERID2", "EXPERID3")


@pytest.fixture(
    scope="function",
    params=[
        pytest.param((1, "complete_common_header"), id="Intensity"),
        pytest.param((4, "complete_polarimetric_header"), id="Polarimetric"),
    ],
)
def write_l1_task(request, recipe_run_id, tmp_path):
    with CompleteWriteL1Frame(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        task.scratch = WorkflowFileSystem(recipe_run_id=recipe_run_id, scratch_base_path=tmp_path)
        num_of_stokes_params, header_fixture_name = request.param
        header = request.getfixturevalue(header_fixture_name)
        stokes_params = ["I", "Q", "U", "V"]
        used_stokes_params = []
        hdu = fits.PrimaryHDU(data=np.random.random(size=(1, 128, 128)) * 10, header=header)
        hdul = fits.HDUList([hdu])
        for i in range(num_of_stokes_params):
            task.write(
                data=hdul,
                tags=[
                    Tag.calibrated(),
                    Tag.frame(),
                    Tag.stokes(stokes_params[i]),
                    Tag.dsps_repeat(i),
                ],
                encoder=fits_hdulist_encoder,
            )
            used_stokes_params.append(stokes_params[i])
        task.constants._update(asdict(FakeConstantDb()))
        yield task, used_stokes_params, header
        task._purge()


@pytest.fixture()
def make_mock_gql_client_with_provenance():
    """Factory to create GraphQL client Mocks that will return customizable provenance records."""

    def factory(provenances: list[RecipeRunProvenanceResponse]):
        class WriteL1FakeGQLClient(FakeGQLClient):
            def execute_gql_query(self, **kwargs):
                response = super().execute_gql_query(**kwargs)
                if isinstance(response, list):
                    if isinstance(response[0], RecipeRunResponse):
                        response: list[RecipeRunResponse]
                        response[0].recipeRunProvenances = provenances
                return response

        return WriteL1FakeGQLClient

    return factory


@pytest.mark.parametrize(
    "provenances, is_manual",
    [
        pytest.param(
            [RecipeRunProvenanceResponse(recipeRunProvenanceId=1, isTaskManual=False)],
            False,
            id="auto_single",
        ),
        pytest.param(
            [
                RecipeRunProvenanceResponse(recipeRunProvenanceId=1, isTaskManual=False),
                RecipeRunProvenanceResponse(recipeRunProvenanceId=2, isTaskManual=False),
            ],
            False,
            id="auto_multiple",
        ),
        pytest.param(
            [RecipeRunProvenanceResponse(recipeRunProvenanceId=1, isTaskManual=True)],
            True,
            id="manual_single",
        ),
        pytest.param(
            [
                RecipeRunProvenanceResponse(recipeRunProvenanceId=1, isTaskManual=False),
                RecipeRunProvenanceResponse(recipeRunProvenanceId=2, isTaskManual=True),
            ],
            True,
            id="manual_multiple",
        ),
    ],
)
def test_write_l1_frame(
    write_l1_task,
    mocker,
    make_mock_gql_client_with_provenance,
    provenances: list[RecipeRunProvenanceResponse],
    is_manual,
):
    """
    :Given: a write L1 task
    :When: running the task
    :Then: no errors are raised and the MANPROC and FRAMEVOL headers are correct
    """
    WriteL1GQLClient = make_mock_gql_client_with_provenance(provenances=provenances)

    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=WriteL1GQLClient
    )
    mocker.patch(
        "dkist_processing_common.tasks.write_l1.WriteL1Frame.version_from_module_name",
        new_callable=Mock,
        return_value="fake_version_number",
    )

    task, used_stokes_params, _ = write_l1_task
    task()
    for stokes_param in used_stokes_params:
        files = list(task.read(tags=[Tag.frame(), Tag.output(), Tag.stokes(stokes_param)]))
        assert len(files) == 1
        for file in files:
            assert file.exists
            spec214_validator.validate(file, extra=False)
            hdu = fits_hdu_decoder(file)
            assert hdu.header["MANPROCD"] == is_manual

            # Test that FRAMEVOL is within 3% of the actual, on-disk size
            on_disk_size_mb = file.stat().st_size / 1024 / 1024
            np.testing.assert_allclose(hdu.header["FRAMEVOL"], on_disk_size_mb, rtol=0.03)

            # Test that FRAMEVOL still has its comment
            assert hdu.header.comments["FRAMEVOL"]


def test_replace_header_values(write_l1_task):
    """
    :Given: an input header
    :When: replacing specific header values
    :Then: the header values have changed
    """
    task, _, header = write_l1_task
    original_file_id = header["FILE_ID"]
    original_date = header["DATE"]
    data = np.ones(shape=(1, 1))
    header = task.replace_header_values(header=header, data=data)
    assert header["FILE_ID"] != original_file_id
    assert header["DATE"] != original_date
    assert header["NAXIS"] == len(data.shape)
    assert header["DATE-END"] == "2020-01-02T00:00:00.100000"


def test_l1_filename(write_l1_task):
    """
    :Given: an input header
    :When: asking for the corresponding L1 filename
    :Then: the filename is formatted as expected
    """
    task, _, header = write_l1_task
    assert (
        task.l1_filename(header=header, stokes="Q")
        == f"VISP_2020_01_02T00_00_00_000000_01080000_Q_{task.constants.dataset_id}_L1.fits"
    )


def test_calculate_date_avg(write_l1_task):
    """
    :Given: an input header
    :When: finding the average date
    :Then: the correct datetime string is returned
    """
    task, _, header = write_l1_task
    assert task.calculate_date_avg(header=header) == "2020-01-02T12:00:00.000000"


def test_calculate_telapse(write_l1_task):
    """
    :Given: an input header
    :When: finding the time elapsed in an observation
    :Then: the correct time value is returned
    """
    task, _, header = write_l1_task
    assert task.calculate_telapse(header=header) == 86400


def test_solarnet_keys(write_l1_task, mocker):
    """
    :Given: files with headers converted to SPEC 214 L1
    :When: checking the solarnet extra headers
    :Then: the correct values are found
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    mocker.patch(
        "dkist_processing_common.tasks.write_l1.WriteL1Frame.version_from_module_name",
        new_callable=Mock,
        return_value="fake_version_number",
    )

    task, _, _ = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output()]))
    for file in files:
        header = fits.open(file)[1].header
        assert header["DATEREF"] == header["DATE-BEG"]
        assert round(header["OBSGEO-X"]) == -5466045
        assert round(header["OBSGEO-Y"]) == -2404389
        assert round(header["OBSGEO-Z"]) == 2242134
        assert header["SOLARRAD"] == 975.58
        assert header["SPECSYS"] == "TOPOCENT"
        assert header["VELOSYS"] == 0.0
        assert header["WAVEBAND"] == "Fe XIII (1079.8 nm)"
        assert header["WAVEMIN"] == 1075.0
        assert header["WAVEMAX"] == 1085.0


def test_documentation_keys(write_l1_task, mocker):
    """
    :Given: files with headers converted to SPEC 214 L1
    :When: checking the documentation header URLs
    :Then: the correct values are found
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    mocker.patch(
        "dkist_processing_common.tasks.write_l1.WriteL1Frame.version_from_module_name",
        new_callable=Mock,
        return_value="fake_version_number",
    )

    task, _, _ = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output()]))
    for file in files:
        header = fits.open(file)[1].header
        assert header["INFO_URL"] == task.docs_base_url
        assert header["HEADVERS"] == spec_version
        assert (
            header["HEAD_URL"] == f"{task.docs_base_url}/projects/data-products/en/v{spec_version}"
        )
        calvers = task.version_from_module_name()
        assert header["CALVERS"] == calvers
        assert (
            header["CAL_URL"]
            == f"{task.docs_base_url}/projects/{task.constants.instrument.lower()}/en/v{calvers}/{task.workflow_name}.html"
        )


def test_get_version_from_module(write_l1_task):
    task, _, _ = write_l1_task
    assert task.version_from_module_name() == common_version


def test_get_tile_size(write_l1_task, mocker):
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, _, _ = write_l1_task
    test_array = np.zeros((1, TILE_SIZE // 2, TILE_SIZE * 2))
    tile_size = task.compute_tile_size_for_array(test_array)
    assert tile_size == [1, TILE_SIZE // 2, TILE_SIZE]


def test_rice_compression_with_specified_tile_size(write_l1_task, mocker):
    """
    :Given: a write_L1 task with a specified tile size in the recipe configuration
    :When: running the task
    :Then: data is written with the compression tile size specified in the recipe configuration
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, _, _ = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output()]))
    for file in files:
        hdul = fits.open(file)
        bintable = hdul[1]._get_bintable_without_data()
        comp_header = bintable.header
        data_shape = list(hdul[1].data.shape)
        data_shape.reverse()
        for i, dim in enumerate(data_shape):
            assert comp_header["ZTILE" + str(i + 1)] == min(dim, TILE_SIZE)


def test_rice_compression_with_default_tile_size(write_l1_task, mocker):
    """
    :Given: a write_L1 task with no specified tile size in the recipe configuration
    :When: running the task
    :Then: data is written with astropy's default compression tile size

    Each tile size should be the length of the axis or 1 due to how astropy chooses default tiles.
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=FakeGQLClientNoRecipeConfiguration,
    )
    task, _, _ = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output()]))
    for file in files:
        hdul = fits.open(file)
        bintable = hdul[1]._get_bintable_without_data()
        comp_header = bintable.header
        data_shape = list(hdul[1].data.shape)
        data_shape.reverse()
        assert comp_header["ZTILE1"] == data_shape[0]
        assert comp_header["ZTILE2"] == 1
        assert comp_header["ZTILE3"] == 1


def test_reprocessing_keys(write_l1_task, mocker):
    """
    :Given: a write_L1 task with reprocessing keys present
    :When: running the task
    :Then: the reprocessing keys are correctly written
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=FakeGQLClient,
    )
    task, _, _ = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output()]))
    for file in files:
        header = fits.open(file)[1].header
        assert header["IDSPARID"] == task.metadata_store_input_dataset_parameters_part_id
        assert header["IDSOBSID"] == task.metadata_store_input_dataset_observe_frames_part_id
        assert header["IDSCALID"] == task.metadata_store_input_dataset_calibration_frames_part_id
        assert header["WKFLNAME"] == task.workflow_name
        assert header["WKFLVERS"] == task.workflow_version


def test_calculate_date_end(write_l1_task):
    """
    :Given: a write_L1 task with the DATE-END keyword
    :When: running the task
    :Then: the DATE-END keyword is inserted as expected
    """
    task, _, header = write_l1_task
    assert task.calculate_date_end(header=header) == "2020-01-02T00:00:00.100000"


def test_add_contributing_id_headers(write_l1_task):
    """
    :Given: a header and proposal id / experiment id constants
    :When: adding ids to the headers
    :Then: the correct ids are added
    """
    task, _, header = write_l1_task
    header = task.add_contributing_id_headers(header=header)
    # Ensure there is one contributing proposal ID
    assert header["PROPID01"] == "PROPID1"
    # Ensure that there are contributing experiment IDs
    assert header["EXPRID01"] == "EXPERID1"
    assert header["EXPRID02"] == "EXPERID2"
    assert header["EXPRID03"] == "EXPERID3"
    # Check total numbers
    assert header["NPROPOS"] == 1
    assert header["NEXPERS"] == 3


def test_spectral_line_keys(write_l1_task, mocker):
    """
    :Given: a header
    :When: adding spectral line information to the headers
    :Then: the correct values are added
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient",
        new=FakeGQLClient,
    )
    task, _, header = write_l1_task
    header = task.add_datacenter_headers(header=header, hdu_size=1024, stokes="I")
    assert header["SPECLN01"] == "Fe XIII (1079.8 nm)"
    assert header["SPECLN02"] == "He I (1083.0 nm)"
    assert header["NSPECLNS"] == 2
    with pytest.raises(KeyError):
        assert header["SPECLN03"]


@pytest.mark.flaky(max_reruns=10)
def test_location_of_dkist(write_l1_task):
    """
    Given: function for retrieving the dkist location on earth
    When: Call function
    Then: result is the same as what is in the astropy online database
    """
    task, _, _ = write_l1_task
    itrs = task.location_of_dkist
    assert itrs == EarthLocation.of_site("dkist")
