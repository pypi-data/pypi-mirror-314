import os
import os.path
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly
from wwttoolbox.qaqc.anomaly_detection import (
    AnomalyDetectionAlgorithm,
    AnomalyDetectionConfig,
)


def plot_dataframe(
    data: pd.DataFrame, file_path: str, title: str = None, open_browser: bool = False
):
    """Plots the data frame returned by the anomaly detection algorithm."""

    plot_file_path = file_path if file_path.endswith(".html") else f"{file_path}.html"

    outliers = go.Scatter(
        x=data["timestamp"],
        y=data["observation_removed"],
        name="outliers",
        mode="markers",
        text=[
            "(Description: " + "{}".format(description) + ")<br>"
            "(datetime:"
            + "{}".format(ts)
            + ")"
            + " , value: "
            + "{:.2f}".format(val)
            + ")"
            for description, ts, val in zip(
                list(data["description"]),
                list(data["timestamp"]),
                list(data["observation_removed"]),
            )
        ],
        hoverinfo="text",
        line=dict(color="RED"),
        opacity=0.9,
    )
    qa = go.Scatter(
        x=data["timestamp"],
        y=data["observation_qa"],
        name="QA",
        mode="markers",
        line=dict(color="#7F7F7F"),
        opacity=0.9,
    )

    std_top = go.Scatter(
        x=data["timestamp"],
        y=data["std_band_top"],
        name="std_band_top",
        mode="lines",
        line=dict(color="blue"),
        opacity=0.9,
    )
    std_bottom = go.Scatter(
        x=data["timestamp"],
        y=data["std_band_bottom"],
        name="std_band_bottom",
        mode="lines",
        line=dict(color="blue"),
        opacity=0.9,
    )

    MA = go.Scatter(
        x=data["timestamp"],
        y=data["MA"],
        name="MA",
        mode="lines",
        line=dict(color="green"),
        opacity=0.9,
    )
    qa_interpolated = go.Scatter(
        x=data["timestamp"],
        y=data["observation_qa_interpolated"],
        name="qa-interpolated",
        mode="lines",
        line=dict(color="grey"),
        opacity=0.9,
    )
    data = [qa, outliers, std_top, std_bottom, MA, qa_interpolated]
    layout = dict(
        title=title,
        legend=dict(orientation="v", x=1.0, font=dict(size=9)),
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=plot_file_path, auto_open=open_browser)
