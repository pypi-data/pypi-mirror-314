from typing import Dict, Any


class CustomFeatureLogic:
    """
    Creates CustomFeatureLogic object for the feature logic provided from custom UDF.

    Attributes:
        custom_class_name (str): Class name from custom file.
        file_path (str): File path containing custom UDF script.
        is_feature_logic_custom (bool): Flag to decide weather the logic is custom or predefined, Default value is True.

    Examples
    --------
    >>>    custom_class_name="CreditScoreProcessor",
    ...    custom_file_path="/opt/spark/work-dir/bob/src/v2/external_udfs/features/custom_udf.py",
    ...    custom_docker_image="private-repo/custom-image:v1.0",
    ...    custom_feature_args={
    ...        "timestamp_column": "timestamp",
    ...        "groupby_keys": ["id", "timestamp"]
    ...    },
    ...    mode="spark_sql"
    """

    def __init__(
        self,
        class_name: str = "",
        file_path: str = "",
        docker_image: str = "",
        feature_args: Dict[str, Any] = {},
        mode: str = "",
    ):
        self.custom_class_name = class_name
        self.custom_file_path = file_path
        self.function_type = "custom_udf"
        self.custom_docker_image = docker_image
        self.custom_feature_args = feature_args
        self.mode = mode

    def to_json(self) -> Dict:
        """
        Returns:
            Dict: A dictionary representing the feature attributes in JSON format.
        """
        return {
            "custom_class_name": self.custom_class_name,
            "custom_file_path": self.custom_file_path,
            "custom_docker_image": self.custom_docker_image,
            "function_type": self.function_type,
            "mode": self.mode,
            **self.custom_feature_args,
        }
