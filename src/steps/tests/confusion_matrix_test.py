from unittest.mock import patch

import pandas as pd

from src.steps import confusion_matrix


class TestConfusionMatrix:
    class TestApply:
        @staticmethod
        def test_should_return_confusion_matrix_dataframe():
            input_df = pd.DataFrame(
                {
                    "label_true": ["dog", "dog", "dog", "cat"],
                    "label_predicted": ["dog", "dog", "dog", "cat"],
                }
            )
            expected_confusion_matrix_df = pd.DataFrame(
                {"cat": [1, 0], "dog": [0, 3]}, index=["cat", "dog"]
            )

            computed_confusion_matrix_df = confusion_matrix.ConfusionMatrix().apply(
                input_df
            )

            pd.testing.assert_frame_equal(
                expected_confusion_matrix_df,
                computed_confusion_matrix_df,
                check_like=True,
            )

        @staticmethod
        @patch.object(confusion_matrix, "Metrics")
        def test_should_save_confusion_matrix(mock_metrics):
            input_df = pd.DataFrame(
                {
                    "label_true": ["dog", "dog", "dog", "cat"],
                    "label_predicted": ["dog", "dog", "dog", "cat"],
                }
            )

            mock_metrics().class_names = ["dog", "cat"]
            confusion_matrix.ConfusionMatrix(image_output_path="data/samples").apply(
                input_df
            )

            mock_metrics().save_confusion_matrix.assert_called_once_with("data/samples")
