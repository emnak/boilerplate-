import yaml
from pipeline.steps import AbstractDataFrameStep
from tensorflow.keras.models import load_model

from src import data_generators
from src.steps import AbstractStepWithCleanup


class ClassifierPrediction(AbstractStepWithCleanup, AbstractDataFrameStep):
    """
    Step which computes predictions of a Keras classifier on a test data generator.
    """

    def __init__(
        self,
        model_path,
        test_generator,
        ordered_labels_path=None,
        class_mode="categorical",
    ):
        """
        Args:
            model_path (str): path to the file in which the model is saved with its weights.
            test_generator (dict): a dict describing the test data generator that contains:
                name (str): the name of the generator, corresponds to a keras Sequence class in src.data_generators.
                init (dict, default={}): the data generator parameters.
            ordered_labels_path (str): path to a YAML file with ordered list of labels, used to substitute class indices
                with class labels in the outputted DataFrame.
        """
        self._model = None
        self._model_path = model_path
        self._ordered_labels_path = ordered_labels_path
        self._test_generator = getattr(data_generators, test_generator["name"])(
            shuffle=False, **test_generator["init"]
        )

        if class_mode not in ["categorical", "binary"]:
            raise ValueError("class_mode should be 'categorical' or 'binary'")
        self._class_mode = class_mode

    def apply_workflow(self):
        """
        No input for this step.
        Returns:
            pandas.DataFrame: a DataFrame indexed by the 'image_index', with 'true' and 'predicted' columns
                              (true and predicted class for each image).
        """
        self._instantiate_model()

        labels_dict = None
        if self._ordered_labels_path:
            with open(self._ordered_labels_path) as ordered_labels_file:
                labels_dict = dict(
                    enumerate(yaml.load(ordered_labels_file, Loader=yaml.FullLoader))
                )

        y_predicted = self._model.predict_generator(self._test_generator, verbose=1)

        return (
            self._test_generator.annotations_df.assign(
                label_predicted=(
                    y_predicted.round()
                    if self._class_mode == "binary"
                    else y_predicted.argmax(axis=1)
                ),
                confidence=(
                    y_predicted
                    if self._class_mode == "binary"
                    else y_predicted.max(axis=1)
                ),
                y_predicted=list(y_predicted),
            )
            .replace({"label_true": labels_dict, "label_predicted": labels_dict})
            .rename_axis("image_index")
        )

    def _instantiate_model(self):
        self._model = load_model(self._model_path)
