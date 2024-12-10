class QualityCodes:
    GOOD = 100
    BAD = 200
    OUTLIER_RUN_1 = 201
    OUTLIER_RUN_2 = 202
    OUTLIER_RUN_3 = 203
    OUTLIER_RUN_4 = 204
    OUTLIER_RUN_5 = 205
    SENSOR_ERROR = 300


def get_qc_description(qc: int) -> str:
    """Returns the description of the quality code.

    Args:
        qc (int): The quality code.

    Returns:
        str: The description of the quality code.

    """
    if qc == QualityCodes.GOOD:
        return "Good"
    elif qc == QualityCodes.BAD:
        return "Bad"
    elif qc == QualityCodes.OUTLIER_RUN_1:
        return "Outlier Run 1"
    elif qc == QualityCodes.OUTLIER_RUN_2:
        return "Outlier Run 2"
    elif qc == QualityCodes.OUTLIER_RUN_3:
        return "Outlier Run 3"
    elif qc == QualityCodes.OUTLIER_RUN_4:
        return "Outlier Run 4"
    elif qc == QualityCodes.OUTLIER_RUN_5:
        return "Outlier Run 5"
    elif qc == QualityCodes.SENSOR_ERROR:
        return "Sensor Error"
    else:
        return "Unknown"
