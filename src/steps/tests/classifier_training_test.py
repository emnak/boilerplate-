from unittest.mock import patch, MagicMock

import pandas as pd

from src.steps import ClassifierTraining

TRAIN_CLASSIFIER_PARAMETERS = {
    "model": {"name": "model_name", "parameters": {"model_kwarg": "model_kwarg_value"}},
    "loss": "loss_name",
    "optimizer": {
        "name": "optimizer_name",
        "init": {"optimizer_kwarg": "optimizer_kwarg_value"},
    },
    "train_generator": {
        "name": "train_generator_name",
        "init": {"train_generator_kwarg": "train_generator_kwarg_value"},
    },
    "val_generator": {
        "name": "val_generator_name",
        "init": {"val_generator_kwarg": "val_generator_kwarg_value"},
    },
    "epochs": 100,
    "output_folder": "output",
}

DATASET_SHAPE = (9, 50, 50, 3)
LABELS = [0, 1, 2, 3, 0, 1, 1, 1, 1]
DATASET_CLASS = pd.np.unique(LABELS)
X_DATA = pd.np.zeros(DATASET_SHAPE)
Y_DATA = pd.np.array(LABELS).reshape(len(LABELS), 1)
DATA_SET = (X_DATA, Y_DATA)


class TestClassifierTraining:
    class TestInit:
        @staticmethod
        @patch("src.steps.classifier_training.models")
        @patch("src.steps.classifier_training.losses")
        @patch("src.steps.classifier_training.optimizers")
        @patch("src.steps.classifier_training.data_generators")
        def test_should_instantiate_correctly(data_generators_mocks, *_):
            ClassifierTraining(**TRAIN_CLASSIFIER_PARAMETERS)
            data_generators_mocks.train_generator_name.assert_called_once_with(
                train_generator_kwarg="train_generator_kwarg_value"
            )
            data_generators_mocks.val_generator_name.assert_called_once_with(
                val_generator_kwarg="val_generator_kwarg_value"
            )

    class TestApply:
        @staticmethod
        @patch("src.steps.classifier_training.models")
        @patch("src.steps.classifier_training.losses")
        @patch("src.steps.classifier_training.optimizers")
        @patch("src.steps.classifier_training.data_generators")
        @patch("src.steps.classifier_training.ModelCheckpoint")
        @patch("src.steps.classifier_training.TensorBoard")
        def test_should_train_the_model(
            tensorboard_mock,
            model_checkpoint_mock,
            data_generators_mocks,
            optimizers_mock,
            losses_mock,
            models_mock,
        ):
            data_generators_mocks.train_generator_name().ordered_labels = [
                "LABEL_A",
                "LABEL_B",
            ]
            classifier_training = ClassifierTraining(**TRAIN_CLASSIFIER_PARAMETERS)
            classifier_training.save_ordered_labels = MagicMock()
            classifier_training.apply()
            models_mock.model_name.assert_called_once_with(
                input_shape=data_generators_mocks.train_generator_name().input_shape,
                classes=data_generators_mocks.train_generator_name().num_classes,
                model_kwarg="model_kwarg_value",
            )
            optimizers_mock.optimizer_name.assert_called_once_with(
                optimizer_kwarg="optimizer_kwarg_value"
            )
            models_mock.model_name().compile.assert_called_once_with(
                loss=losses_mock.loss_name,
                optimizer=optimizers_mock.optimizer_name(),
                metrics=["accuracy"],
            )
            models_mock.model_name().summary.assert_called_once_with()
            tensorboard_mock.assert_called_once_with(log_dir="output", profile_batch=0)
            model_checkpoint_mock.assert_called_once_with(
                "output/model_with_best_weights.h5",
                monitor="val_loss",
                save_best_only=True,
            )
            models_mock.model_name().fit_generator.assert_called_once_with(
                data_generators_mocks.train_generator_name(),
                epochs=100,
                steps_per_epoch=None,
                validation_steps=None,
                verbose=1,
                validation_data=data_generators_mocks.val_generator_name(),
                callbacks=[tensorboard_mock(), model_checkpoint_mock()],
            )
            classifier_training.save_ordered_labels.assert_called_with(
                ["LABEL_A", "LABEL_B"]
            )
