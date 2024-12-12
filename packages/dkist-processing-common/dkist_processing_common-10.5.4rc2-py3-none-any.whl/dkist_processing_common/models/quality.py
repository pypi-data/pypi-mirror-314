"""Support classes used to create a quality report."""
from typing import Any

from pydantic import BaseModel


class Plot2D(BaseModel):
    """Support class use to hold the data for creating a 2D plot in the quality report."""

    xlabel: str
    ylabel: str
    series_data: dict[str, list[list[Any]]]
    series_name: str | None = None
    ylabel_horizontal: bool = False


class SimpleTable(BaseModel):
    """Support class to hold a simple table to be inserted into the quality report."""

    rows: list[list[Any]]
    header_row: bool = True
    header_column: bool = False


class ModulationMatrixHistograms(BaseModel):
    """Support class for holding the big ol' grid of histograms that represent the modulation matrix fits."""

    modmat_list: list[list[list[float]]]


class EfficiencyHistograms(BaseModel):
    """Support class for holding 4 histograms that correspond to efficiencies of the 4 stokes components."""

    efficiency_list: list[list[float]]


class PlotHistogram(BaseModel):
    """Support class to hold 1D data for plotting a histogram."""

    xlabel: str
    series_data: dict[str, list[float]]
    series_name: str | None = None
    vertical_lines: dict[str, float] | None


class PlotRaincloud(BaseModel):
    """Support class to hold data series for fancy-ass violin plots."""

    xlabel: str
    ylabel: str
    categorical_column_name: str
    distribution_column_name: str
    dataframe_json: str
    hue_column_name: str | None
    ylabel_horizontal: bool | None


class ReportMetric(BaseModel):
    """
    A Quality Report is made up of a list of metrics with the schema defined by this class.

    Additionally, this class can produce a Flowable or List of Flowables to be render the metric in the PDF Report
    """

    name: str
    description: str
    metric_code: str
    facet: str | None = None
    statement: str | list[str] | None = None
    plot_data: Plot2D | list[Plot2D] | None = None
    histogram_data: PlotHistogram | list[PlotHistogram] | None = None
    table_data: SimpleTable | list[SimpleTable] | None = None
    modmat_data: ModulationMatrixHistograms | None = None
    efficiency_data: EfficiencyHistograms | None = None
    raincloud_data: PlotRaincloud | None = None
    warnings: list[str] | None = None
