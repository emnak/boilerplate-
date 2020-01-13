from pathlib import Path

import pandas as pd
import pytest
from pipeline import Pipeline
from pipeline.utils.config_utils import get_from_config
from pipeline.utils.run_pipeline_config import (
    RUN_PIPELINE_CONFIG_KEY,
    run_pipeline_config,
)
from pipeline.utils.yaml_utils import parse_yaml_with_variables_files


TEST_CONFIGS = [
    (
        "pipelines/fashion-mnist-simple-cnn-pipeline.yaml",
        {"number_of_epochs": 1},
        (10, 11),
    ),
    (
        "pipelines/local-dataset-simple-cnn-pipeline.yaml",
        {
            "class_mode": "binary",
            "target_size": [26, 26],
            "number_of_epochs": 1,
            "horizontal_flip": False,
            "batch_size": 2,
        },
        (2, 3),
    ),
]


# pylint: disable=invalid-name
@pytest.mark.parametrize(
    "pipeline_name,pipeline_parameters,expected_output_shape", TEST_CONFIGS
)
def test_pipeline_produces_final_output(
    pipeline_name, pipeline_parameters, expected_output_shape, tmp_path
):
    run_pipeline_config(get_from_config(RUN_PIPELINE_CONFIG_KEY))

    pipeline_parameters["output_folder"] = f"{tmp_path}/output"
    parsed_parameters = parse_yaml_with_variables_files(
        pipeline_name, [], pipeline_parameters
    )

    pipeline = Pipeline(**parsed_parameters.get("init", {}))
    pipeline.run(**parsed_parameters.get("run", {}))

    # Test if the pipeline produced the last file
    output_path = Path(f"{tmp_path}/output")
    confusion_matrix_files = list(output_path.glob("*-ConfusionMatrix.csv"))
    confusion_matrix = pd.read_csv(confusion_matrix_files[0])
    assert not confusion_matrix.empty
    assert confusion_matrix.shape == expected_output_shape
