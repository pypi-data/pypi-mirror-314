from wwttoolbox.qaqc.anomaly_detection.quality_codes import (
    QualityCodes,
    get_qc_description,
)
import numpy as np
from datetime import datetime
import pandas as pd
from wwttoolbox.qaqc.anomaly_detection.anomaly_detection_config import (
    AnomalyDetectionConfig,
)
from wwttoolbox.qaqc.anomaly_detection.rolling_window import (
    RollingWindow,
    RollingWindowParams,
)


class AnomalyDetectionAlgorithm:

    def __init__(self, config: AnomalyDetectionConfig):
        self.config: AnomalyDetectionConfig = config
        self.in_data_df: pd.DataFrame = None
        self.out_data_df: pd.DataFrame = None
        self._algo_state: pd.DataFrame = None

    def set_data_from_series(
        self, timestamp: list[datetime], observation: list[float]
    ) -> None:
        self.in_data_df = pd.DataFrame(
            {"timestamp": timestamp, "observation": observation}
        )
        self.in_data_df["timestamp"] = self.in_data_df["timestamp"].astype(
            "datetime64[ns]"
        )
        self.in_data_df["observation"] = self.in_data_df["observation"].astype(
            "float64"
        )

    def set_data_from_dataframe(self, data: pd.DataFrame) -> None:

        if "timestamp" not in data.columns or "observation" not in data.columns:
            raise ValueError(
                "Dataframe must have columns 'timestamp' and 'observation'"
            )

        if data["timestamp"].dtype != "datetime64[ns]":
            raise ValueError("Column 'timestamp' must be of type datetime64[ns]")

        if data["observation"].dtype != "float64":
            raise ValueError("Column 'observation' must be of type float64")

        self.in_data_df = data

    def run(self) -> pd.DataFrame:
        """Executes the anomaly detection algorithm and returns the results as a DataFrame

        Columns:
        - timestamp: The timestamp of the observation
        - observation: The observation value
        - quality_code: The quality code of the observation
        - description: The description of the quality code
        - observation_qa: The quality-assured observation values
        - observation_removed: The flagged observation values
        - observation_qa_interpolated: The quality-assured observation values with linear interpolation
        - std_band_top: The top band standard deviation of the rolling window
        - std_band_bottom: The bottom band standard deviation of the rolling window
        - MA: The mean of the rolling window

        """

        flagged_data_series: list[pd.DataFrame] = []

        data = self._pre_processing(self.in_data_df)
        data = self._flag_sensor_codes(data)

        for run in range(1, 5):
            data, flagged_data = self._rolling_eval(data, run)
            flagged_data_series.append(flagged_data)

        data, flagged_data = self._rolling_eval(data, 5)

        flagged_data_series.append(flagged_data)
        flagged_data_series.insert(0, data)
        data_total = pd.concat(flagged_data_series)

        self.out_data_df = self._post_procesing(data_total)

        return self.out_data_df

    def _flag_sensor_codes(self, data: pd.DataFrame) -> pd.DataFrame:
        """Flags sensor codes based on the configuration.

        Parameters:
        - data (pd.DataFrame): The input data.

        Returns:
        - pd.DataFrame: The input data with flagged sensor codes.
        """

        for index, row in data.iterrows():
            for key, value in self.config.error_codes.items():
                expression = "row.observation" + key
                if eval(expression):
                    data.at[index, "quality_code"] = value

        return data

    def _rolling_eval(
        self, data: pd.DataFrame, run: int
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Applies the rolling window evaluation to the input data.

        Parameters:
        - data (pd.DataFrame): The input data.

        Returns:
        - tuple[pd.DataFrame, pd.DataFrame]: The results of the rolling window evaluation and the removed data.
        """

        good_data_points = data[data["quality_code"] == QualityCodes.GOOD].copy()
        removed_data_points = data[data["quality_code"] != QualityCodes.GOOD].copy()

        rolling_window_params = RollingWindowParams(self.config.config, run)
        rolling_window = RollingWindow(good_data_points, rolling_window_params)
        evaluated_data_points = rolling_window.evaluate_rolling_window()

        return evaluated_data_points, removed_data_points

    def _pre_processing(self, data: pd.DataFrame) -> pd.DataFrame:
        """Pre process the data.

        Applies following steps:
        - Adds 'quality_code' holding the quality code of the sensor values
        """
        data["quality_code"] = QualityCodes.GOOD
        return data

    def _post_procesing(self, data: pd.DataFrame) -> pd.DataFrame:
        """Post process the processed data.

        Applies following steps:
        - Adds 'description' holding a description of the flagging
        - Adds 'observation_qa' holding the quality-assured sensor values
        - Adds 'observation_removed' holding the flagged sensor values
        - Adds 'observation_qa_interpolated' holding the quality-assured sensor values with linear interpolation
        """
        data = data.sort_values(by="timestamp")

        data["observation_qa"] = np.where(
            (data["quality_code"] == QualityCodes.GOOD),
            data["observation"],
            np.nan,
        )
        data["observation_removed"] = np.where(
            (data["quality_code"] != QualityCodes.GOOD),
            data["observation"],
            np.nan,
        )
        data["description"] = data["quality_code"].apply(get_qc_description)
        data["observation_qa_interpolated"] = data["observation_qa"].interpolate(
            method="linear"
        )

        return data
