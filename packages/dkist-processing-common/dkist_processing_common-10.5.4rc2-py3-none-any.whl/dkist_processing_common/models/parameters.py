"""Base class for parameter-parsing object."""
import logging
from datetime import datetime
from typing import Any
from typing import Literal

import numpy as np
import scipy.interpolate as spi
from astropy.io import fits

from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetParameterValue

logger = logging.getLogger(__name__)


class ParameterBase:
    """
    Class to put all parameters parsed from the input dataset document in a single property on task classes.

    There are two main reasons for this:

    1. Segregate the parameters as a .parameters attribute to Science Tasks. This keeps the top-level namespace clean
    2. Allow subclasses to introduce arbitrary logic when parsing instrument-specific parameters (i.e., all of them)

    To use in an instrument pipeline a subclass is required. Here's a simple, but complete example::

        class InstParameters(ParameterBase)
            def __init__(self, input_dataset_parameters, some_other_parameter):
                super().__init__(input_dataset_parameters)
                self._thing = self._some_function(some_other_parameters)

            @property
            def some_parameter(self):
                return self._find_most_recent_past_value("some_parameter_name")

            @property
            def complicate_parameter(self):
                return self._some_complicated_parsing_function("complicated_parameter_name", another_argument)


    Note that you can do whatever you want in the definition for each parameter

    Once you have the parameter class it needs to be added to the base Task. This is done by adding/updating
    the instrument's ScienceTask.__init__ function to look similar to this::

             def __init__(
                self,
                recipe_run_id: int,
                workflow_name: str,
                workflow_version: str,
            ):
                super().__init__(
                    recipe_run_id=recipe_run_id,
                    workflow_name=workflow_name,
                    workflow_version=workflow_version,
                )

                self.parameters = InstParameters(self.input_dataset_parameters)  #<------ This is the important line

    Note that the first argument to the ConstantsSubclass with *always* be self.input_dataset_parameters, but
    additional argument can be passed if the subclass requires them.

    Parameters
    ----------
    input_dataset_parameters
        The input parameters

    obs_ip_start_time
        A string containing the start date of the Observe IP task type frames. Must be in isoformat.

    kwargs
        Any additional keyword arguments
    """

    def __init__(
        self,
        input_dataset_parameters: dict[str, list[InputDatasetParameterValue]],
        obs_ip_start_time: str | None = None,
        **kwargs,
    ):
        self.input_dataset_parameters = input_dataset_parameters
        if obs_ip_start_time is not None:
            # Specifically `not None` because we want to error normally on badly formatted strings (including "").
            self._obs_ip_start_datetime = datetime.fromisoformat(obs_ip_start_time)
        else:
            logger.info(
                "WARNING: "
                "The task containing this parameters object did not provide an obs ip start time. "
                "This really only makes sense for Parsing tasks."
            )

        for parent_class in self.__class__.__bases__:
            if hasattr(parent_class, "is_param_mixin"):
                parent_class.__init__(self, **kwargs)

    def _find_most_recent_past_value(
        self,
        parameter_name: str,
        start_date: datetime | None = None,
    ) -> Any:
        """Get a single value from the input_dataset_parameters."""
        start_date = start_date or self._obs_ip_start_datetime
        values = self.input_dataset_parameters[parameter_name]  # Force KeyError if it doesn't exist
        sorted_values_from_before = sorted(
            [v for v in values if v.parameter_value_start_date <= start_date],
            key=lambda x: x.parameter_value_start_date,
        )
        try:
            result = sorted_values_from_before.pop().parameter_value
        except IndexError:
            raise ValueError(
                f"{parameter_name} has no values before {start_date.isoformat()} ({len(values)} values in total)"
            )
        return result

    @staticmethod
    def _load_param_value_from_fits(param_dict: dict, hdu: int = 0) -> np.ndarray:
        """Load a numpy array from a parameter pointing to a FITS file."""
        file_path = param_dict["param_path"]

        hdul = fits.open(file_path)
        return hdul[hdu].data

    @staticmethod
    def _load_param_value_from_numpy_save(param_dict: dict) -> np.ndarray:
        """Return the data associated with a parameter file saved in numpy format."""
        file_path = param_dict["param_path"]
        result = np.load(file_path)
        return result


class _ParamMixinBase:
    """Simple class with sentinel class variable to identify subclasses as ParameterMixins."""

    is_param_mixin = True


class ParameterWavelengthMixin(_ParamMixinBase):
    """
    Mixin that provides support for wavelength-dependent parameters.

    It allows for the "wavelength" kwarg to `__init__` and provides the `self._wavelength` attribute and methods for
    finding parameterValues based on that wavelength.
    """

    def __init__(self, wavelength: float, **kwargs):
        self._wavelength = wavelength

    def _find_parameter_closest_wavelength(self, parameter_name: str) -> Any:
        """
        Find the database value for a parameter that is closest to the requested wavelength.

        The returned value is guaranteed to exist in the database record. If you want to interpolate between the
        database wavelength values then use `_interpolate_wavelength_parameter`.

        NOTE: If the requested wavelength is exactly between two database values, the value from the smaller wavelength
        will be returned.
        """
        parameter_dict = self._find_most_recent_past_value(parameter_name)
        wavelengths = np.array(parameter_dict["wavelength"])
        values = parameter_dict["values"]
        idx = np.argmin(np.abs(wavelengths - self._wavelength))
        chosen_value = values[idx]
        return chosen_value

    def _interpolate_wavelength_parameter(
        self, parameter_name: str, method: Literal["nearest", "linear", "cubic"] = "linear"
    ) -> float:
        """
        Interpolate database value(wavelength) function to a specific wavelength.

        The interpolation method can be specified. See the docs for `scipy.interpolate.griddata` for more information.

        NOTE: If using `method="nearest"` you might also consider `_find_parameter_closest_wavelength`.
        """
        parameter_dict = self._find_most_recent_past_value(parameter_name)
        wavelengths = np.array(parameter_dict["wavelength"])
        values = np.array(parameter_dict["values"])

        return float(spi.griddata(wavelengths, values, self._wavelength, method=method))


class ParameterArmIdMixin(_ParamMixinBase):
    """
    Mixin that provides support for arm-dependent parameters.

    It allows for the "arm_id" kwarg to `__init__` and provides the `self._arm_id` attribute and methods for
    finding parameterValues based on that wavelength.
    """

    def __init__(self, arm_id: str, **kwargs):
        self._arm_id = arm_id.casefold()

    def _find_parameter_for_arm(self, parameter_name: str) -> Any:
        full_param_name = f"{parameter_name}_{self._arm_id}"
        param = self._find_most_recent_past_value(full_param_name)
        return param
