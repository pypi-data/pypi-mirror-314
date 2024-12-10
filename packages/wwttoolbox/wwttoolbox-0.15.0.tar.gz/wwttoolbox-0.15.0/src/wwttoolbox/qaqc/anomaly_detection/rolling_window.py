import pandas as pd
import numpy as np
from typing import Union
from pandas.api.typing import Rolling, Window
from wwttoolbox.qaqc.anomaly_detection.quality_codes import QualityCodes


class RollingWindowParams:

    def __init__(self, configuration: dict, execution_number: int):
        self.configuration = configuration
        self.execution_number = execution_number
        self.window_size = int(configuration[f"window_size{execution_number}"])
        self.center = bool(configuration[f"center{execution_number}"])
        self.window_type = configuration.get(f"window_type{execution_number}", None)
        self.topadd = float(configuration[f"topadd{execution_number}"])
        self.bottomsub = float(configuration[f"bottomsub{execution_number}"])
        self.std_factor = float(configuration[f"std_factor{execution_number}"])
        self.uncertainty_pct = (
            float(configuration["uncertainty_pct"])
            if "uncertainty_pct" in configuration
            else None
        )
        self.uncertainty_constant = (
            float(configuration["uncertainty_con"])
            if "uncertainty_con" in configuration
            else None
        )
        self.outlier_qc = QualityCodes.OUTLIER_RUN_1 + execution_number - 1


class RollingWindow:

    def __init__(self, data: pd.DataFrame, params: RollingWindowParams):
        self.data = data
        self.params = params

    def evaluate_rolling_window(self) -> pd.DataFrame:
        """Evaluates the rolling window of the data and returns the results.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame]: The results of the rolling window evaluation.

        """

        rolling_window = self._get_rolling_window_of_observations()
        self.data.sort_values(by="timestamp")
        self.data["std"] = rolling_window.std()
        self.data["MA"] = (
            rolling_window.median()
            if self.params.execution_number == 3
            else rolling_window.mean()
        )
        self._set_window_top_and_bottom()
        self._set_uncertainty_band()
        self._flag_observations_outside_window()
        self._clean_up()

        return self.data

    ##############################
    # Private methods
    ##############################

    def _get_rolling_window_of_observations(self) -> Union[Rolling, Window]:
        """Returns the rolling window of the observation.

        Returns:
            pd.DataFrame: The rolling window of the observation.

        """
        return self.data["observation"].rolling(
            window=self.params.window_size,
            center=self.params.center,
            win_type=self.params.window_type,
            min_periods=0,
        )

    def _set_window_top_and_bottom(self) -> None:
        """Sets the top and bottom of the rolling window.

        Note: expects 'MA' and 'std' as column in the data.

        """
        MA_series = self.data["MA"]
        std_series = self.params.std_factor * self.data["std"]

        self.data["topwin"] = MA_series + self.params.topadd + std_series
        self.data["botwin"] = MA_series - self.params.bottomsub - std_series

    def _set_uncertainty_band(self):
        """Sets the uncertainty band of the rolling window."""

        observations = self.data["observation"]

        if self.params.uncertainty_pct:
            self.data["topunc"] = observations * (1 + self.params.uncertainty_pct)
            self.data["botunc"] = observations * (1 - self.params.uncertainty_pct)

        elif self.params.uncertainty_constant:
            self.data["topunc"] = observations + self.params.uncertainty_constant
            self.data["botunc"] = observations - self.params.uncertainty_constant

        else:
            self.data["topunc"] = observations
            self.data["botunc"] = observations

    def _flag_observations_outside_window(self) -> None:
        """Flags the observation outside the window."""
        self.data["quality_code"] = np.where(
            (self.data["botunc"] > self.data["topwin"])
            | (self.data["topunc"] < self.data["botwin"]),
            self.params.outlier_qc,
            QualityCodes.GOOD,
        )

    def _clean_up(self) -> None:
        """Cleans up the data."""
        self.data["std_band_top"] = self.data["topwin"]
        self.data["std_band_bottom"] = self.data["botwin"]
        self.data.drop(
            columns=["topwin", "botwin", "topunc", "botunc", "std"],
            axis=1,
            inplace=True,
        )
