from __future__ import annotations

import datetime
from dataclasses import asdict

import pandas as pd

from typing import Any, Optional, Tuple

from proteobench.modules.template.datapoint import Datapoint
from proteobench.modules.template.parse import ParseInputs
from proteobench.modules.template.parse_settings import TEMPLATE_RESULTS_PATH, ParseSettings


class Module:
    """Description of the Module."""

    def is_implemented() -> bool:
        """Returns whether the module is fully implemented."""
        return True

    def generate_intermediate(standard_format: dict, parse_settings: ParseSettings) -> pd.DataFrame:
        """
        Calculate intermediate values from the uploaded file.

        Parameters
        ----------
        standard_format
            The uploaded file in a standard format.
        parse_settings
            The settings used to parse the uploaded file.

        Returns
        -------
        intermediate
            The intermediate values calculated from the uploaded file.
        """

        # TODO calculate intermediate values
        intermediate = pd.DataFrame()

        return intermediate

    def generate_datapoint(intermediate: pd.DataFrame, input_format: str, user_input: dict) -> Datapoint:
        """
        Method used to compute benchmarks for the provided intermediate structure.

        Parameters
        ----------
        intermediate
            The intermediate data structure.
        input_format
            The format of the input file.
        user_input
            The user input settings.

        Returns
        -------
        df
            The computed benchmark values.
        """

        # Leave these lines as they are
        result_datapoint = Datapoint(
            id=input_format + "_" + user_input["version"] + "_" + str(datetime.datetime.now()),
            # Add/remove your own metadata here
            search_engine=input_format,
            software_version=user_input["version"],
            fdr_psm=user_input["fdr_psm"],
            fdr_peptide=user_input["fdr_peptide"],
            fdr_protein=user_input["fdr_protein"],
            MBR=user_input["mbr"],
            precursor_tol=user_input["precursor_mass_tolerance"],
            fragment_tol=user_input["fragment_mass_tolerance"],
            enzyme_name=user_input["search_enzyme_name"],
            missed_cleavages=user_input["allowed_missed_cleavage"],
            min_pep_length=user_input["min_peptide_length"],
            max_pep_length=user_input["max_peptide_length"],
        )
        result_datapoint.generate_id()
        result_datapoint.calculate_plot_data(intermediate)
        df = pd.Series(asdict(result_datapoint))

        return df

    def load_input_file(input_csv: str, input_format: str) -> pd.DataFrame:
        """
        Method loads dataframe from a input file depending on its format.

        Parameters
        ----------
        input_csv
            The path to the input file.
        input_format
            The format of the input file.

        Returns
        -------
        input_data_frame
            The dataframe loaded from the input file.
        """

        input_data_frame: pd.DataFrame

        # Format1 are the results from e.g. different search engines
        # Add simple format manupulations here if necessary
        if input_format == "Format1":
            input_data_frame = pd.read_csv(input_csv, sep="\t", low_memory=False)
        elif input_format == "Format2":
            input_data_frame = pd.read_csv(input_csv, low_memory=False)

        return input_data_frame

    def add_current_data_point(
        self, current_datapoint: pd.Series, all_datapoints: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Add current data point to all data points and load them from file if empty.

        Parameters
        ----------
        all_datapoints
            The data points from previous runs.
        current_datapoint
            The current data point to be added.

        Returns
        -------
        all_datapoints
            The data points with the current data point added.
        """

        if not isinstance(all_datapoints, pd.DataFrame):
            all_datapoints = pd.read_json(TEMPLATE_RESULTS_PATH)
        else:
            all_datapoints = all_datapoints.T
        all_datapoints = pd.concat([all_datapoints, current_datapoint], axis=1)
        all_datapoints = all_datapoints.T.reset_index(drop=True)
        return all_datapoints

    def benchmarking(self, input_file: str, input_format: str, user_input: dict, all_datapoints):
        """
        Main workflow of the module. Used to benchmark workflow results.

        Parameters
        ----------
        input_file
            Path to the workflow output file.
        input_format
            Format of the workflow output file.
        user_input
            User provided parameters for plotting.
        all_datapoints
            DataFrame containing all datapoints from the proteobench repo.
        default_cutoff_min_prec
            Minimum number of runs an ion has to be identified in.

        Returns
        -------
        tuple[DataFrame, DataFrame]
            Tuple containing the intermediate data structure, and all datapoints.
        """

        # Read input file
        # call load_input_file() method
        input_df = self.load_input_file(input_file, input_format)

        # Parse user config
        parse_settings = ParseSettings(input_format)

        # Converte uploaded data to standard format
        standard_format = ParseInputs().convert_to_standard_format(input_df, parse_settings)

        # Create intermediate data structure for benchmarking
        intermediate_data_structure = self.generate_intermediate(standard_format, parse_settings)

        # Compute performance metrics
        current_datapoint = self.generate_datapoint(intermediate_data_structure, input_format, user_input)

        # Add data point to all data points
        all_datapoints = self.add_current_data_point(all_datapoints, current_datapoint)

        return intermediate_data_structure, all_datapoints
