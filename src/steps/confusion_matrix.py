import pandas as pd
import yaml
from chani import Metrics
from pipeline.steps import AbstractDataFrameStep


class ConfusionMatrix(AbstractDataFrameStep):
    """
    Step which computes a confusion matrix from predictions, and generates an image of this matrix.
    """

    def __init__(self, ordered_labels_path=None, image_output_path=None):
        """
        Args:
            ordered_labels_path (str): path to a YAML file with ordered list of labels, used to substitute class indices
                with class labels in the confusion matrix.
            image_output_path (str): path to save confusion matrix image (if not specified, only the csv is outputted).
        """
        self._ordered_labels_path = ordered_labels_path
        self._image_output_path = image_output_path

    def apply(self, predictions_df):
        """
        Args:
            predictions_df (pandas.DataFrame): a predictions DataFrame with 'label_true' and 'label_predicted' columns.

        Returns:
            pandas.DataFrame: a confusion matrix DataFrame with true classes (indices, or labels if ordered_labels is
                              specified) as index, predicted classes as columns names, and occurrence numbers as values.
        """
        ordered_labels = None
        if self._ordered_labels_path:
            with open(self._ordered_labels_path) as ordered_labels_file:
                ordered_labels = yaml.load(ordered_labels_file, Loader=yaml.FullLoader)
        metrics = Metrics(
            predictions_df.label_true, predictions_df.label_predicted, ordered_labels
        )

        if self._image_output_path:
            metrics.save_confusion_matrix(self._image_output_path)

        return pd.DataFrame(
            metrics.confusion_matrix,
            columns=metrics.class_names,
            index=metrics.class_names,
        )
