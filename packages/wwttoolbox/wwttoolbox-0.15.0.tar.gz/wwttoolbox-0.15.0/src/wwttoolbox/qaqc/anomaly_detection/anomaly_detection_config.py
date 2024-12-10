class AnomalyDetectionConfig:

    def __init__(self):
        self.config: dict = {}
        self.error_codes: dict = {}

    @staticmethod
    def create_config_from_template(
        sensor: str, parameter: str
    ) -> "AnomalyDetectionConfig":
        """Create a configuration object from a template.

        Parameters:
        - sensor (str): The sensor that the parameter is from.
        - parameter (str): The parameter to create a configuration for.

        Returns:
        - AnomalyDetectionConfig: The configuration object.
        """

        for template in templates:
            if template["sensor"] == sensor and template["parameter"] == parameter:
                config = AnomalyDetectionConfig()
                config.config = template["config"]
                return config

        raise ValueError(
            f"No template found for sensor {sensor} and parameter {parameter}"
        )

    @staticmethod
    def get_all_templates():
        """Get all templates for anomaly detection algorithms.

        Returns:
        - list: List of templates with sensor, parameter and config keys.
        """
        return templates

    def add_error_code(self, condition: str, error_code: int):
        """Add condition for when to handle a value as error/sensor code.

        Args:
            condition (str): The condition to check for.
            error_code (int): The error code to assign to the value.

        The condition is a string that can be evaluated as a boolean expression.
        - "==9999" is all values that are 9999 will be assigned the error code.
        - "<0" is all values that are less than 0 will be assigned the error code.
        - ">=100" is all values that are greater than or equal to 100 will be assigned the error code

        """
        self.error_codes[condition] = error_code


##############################################
# Templates for anomaly detection algorithms #
##############################################

templates = [
    {
        "sensor": "proteus",
        "parameter": "ecoli",
        "config": {
            "name": "ecoli",
            "window_size1": 5,
            "std_factor1": 2.5,
            "center1": True,
            "topadd1": 1.4,
            "bottomsub1": 0.05,
            "window_size2": 5,
            "std_factor2": 1.5,
            "center2": True,
            "topadd2": 0.3,
            "bottomsub2": 0.05,
            "window_size3": 5,
            "std_factor3": 1,
            "center3": True,
            "topadd3": 0.35,
            "bottomsub3": 0.01,
            "window_size4": 3,
            "std_factor4": 0.2,
            "center4": True,
            "topadd4": 0.03,
            "bottomsub4": 0.01,
            "window_size5": 3,
            "win_type5": "triang",
            "std_factor5": 0.9,
            "center5": True,
            "topadd5": 0.05,
            "bottomsub5": 0.025,
            "uncertainty_pct": 0.03,
        },
    }
]
