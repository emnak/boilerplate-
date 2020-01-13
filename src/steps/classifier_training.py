from pathlib import Path
import yaml
from tensorflow.keras import losses, optimizers
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard

from src import data_generators, models
from src.steps import AbstractStepWithCleanup
from utils.logger import get_logger

LOGGER = get_logger("train-classifier")


# pylint: disable=too-many-instance-attributes
class ClassifierTraining(AbstractStepWithCleanup):
    """
    Step which trains a Keras classifier on train/val data generators.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        model,
        loss,
        optimizer,
        train_generator,
        val_generator,
        epochs,
        output_folder,
        steps_per_epoch=None,
        validation_steps=None,
    ):
        """
        Args:
            model (dict): a dict describing the model that contains:
                name (str): the name of the model, corresponds to a model function in keras.application (e.g. ResNet50,
                            see https://keras.io/applications), or a custom model of the project in src.models.
                parameters (dict, default={}): the optimizer parameters.
            loss: the name of the loss, corresponds to a loss function in keras.losses (e.g. categorical_crossentropy,
                  see https://keras.io/losses)
            optimizer (dict): a dict describing the optimizer that contains:
                name (str): the name of the optimizer, corresponds to an optimizer class in keras.optimizers
                            (e.g. Adadelta, see https://keras.io/optimizers)
                init (dict, default={}): the optimizer parameters.
            train_generator (dict): a dict describing the train data generator that contains:
                name (str): the name of the generator, corresponds to a keras Sequence class in src.data_generators.
                init (dict, default={}): the data generator parameters.
            val_generator (dict): a dict describing the validation data generator, just like the train_generator.
            epochs (int): the number of epochs.
            output_folder (str): folder to put tensorboard logs and model weights.
            steps_per_epoch (int): number of batches per epoch. If set to None, is equal to `num_train / batch_size`
            validation_steps (int): number of batches per epoch during validation. If set to None, is equal to
                `num_val / batch_size`
        """
        self._model_builder = getattr(models, model["name"])
        self._model_kwargs = model.get("parameters", {})
        self._loss = getattr(losses, loss)
        self._optimizer = getattr(optimizers, optimizer["name"])
        self._optimizer_kwargs = optimizer.get("init", {})
        self._epochs = epochs
        self._train_generator = getattr(data_generators, train_generator["name"])(
            **train_generator.get("init", {})
        )
        self._val_generator = getattr(data_generators, val_generator["name"])(
            **val_generator.get("init", {})
        )
        self._output_folder = output_folder
        self._best_weights_path = str(
            Path(f"{output_folder}/model_with_best_weights.h5")
        )
        self._model = None
        self._steps_per_epoch = steps_per_epoch
        self._validation_steps = validation_steps

    def apply_workflow(self):
        """
        No input and no output for this step.
        """
        if hasattr(self._train_generator, "ordered_labels"):
            self.save_ordered_labels(self._train_generator.ordered_labels)

        self._model = self._model_builder(
            input_shape=self._train_generator.input_shape,
            classes=self._train_generator.num_classes,
            **self._model_kwargs,
        )

        self._model.compile(
            loss=self._loss,
            optimizer=self._optimizer(**self._optimizer_kwargs),
            metrics=["accuracy"],
        )

        self._model.summary()
        LOGGER.info("Training")

        self._model.fit_generator(
            self._train_generator,
            epochs=self._epochs,
            steps_per_epoch=self._steps_per_epoch,
            validation_steps=self._validation_steps,
            verbose=1,
            validation_data=self._val_generator,
            callbacks=self.callbacks,
        )

    def save_ordered_labels(self, ordered_labels):
        ordered_labels_path = Path(f"{self._output_folder}/ordered_labels.yaml")
        with ordered_labels_path.open("w") as ordered_labels_file:
            yaml.dump(ordered_labels, ordered_labels_file)

    def dump_output(self, _, output_folder, output_name, **__):
        output_file_path = Path(f"{output_folder}/{output_name}.txt")
        with output_file_path.open("w") as output_file:
            self._model.summary(print_fn=lambda x: output_file.write(x + "\n"))

    @property
    def callbacks(self):
        tensorboard = TensorBoard(
            log_dir=self._output_folder, profile_batch=0
        )  # to disable profiling (always have training curve on Tensorboard)

        model_checkpoint = ModelCheckpoint(
            self._best_weights_path, monitor="val_loss", save_best_only=True
        )

        return [tensorboard, model_checkpoint]
