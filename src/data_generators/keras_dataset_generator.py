import pandas as pd
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras import datasets
from tensorflow.keras.utils import Sequence, to_categorical


class KerasDatasetGenerator(Sequence):
    """
    Generates images batches from a Keras dataset, for the chosen subset ('training', 'validation' or 'test').
    """

    def __init__(
        self,
        dataset_name,
        batch_size,
        shuffle=True,
        subset="training",
        validation_split=0.3,
        data_augmentation=None,
    ):
        """
        Args:
            dataset_name (str): a dataset that can be downloaded with Keras. The list of available datasets is here:
                          https://keras.io/datasets/
            batch_size (int): number of images per batch.
            shuffle (bool): whether to shuffle the data (default: True)
            subset (str): 'training', 'validation' or 'test'.
                Keras datasets are already split into 'train' and 'test', and here:
                    - 'training' corresponds to a subset of Keras 'train' set, determined by 'validation_split'.
                    - 'validation' corresponds to the other subset of Keras 'train' set
                    - 'test' exactly corresponds to Keras 'test' set
            validation_split (float): how to split Keras 'train' set into 'training' and 'validation' subsets.
                    - 'training' set will be images: validation_split * len(train set) -> len(train set)
                    - 'validation' set will be images: 0 -> validation_split * len(train set)
            data_augmentation (dict): parameters to be passed to Keras ImageDataGenerator to randomly augment images.
        """
        if subset not in ["training", "validation", "test"]:
            raise ValueError("subset should be 'training', 'validation' or 'test'")

        self._batch_size = batch_size

        dataset = getattr(datasets, dataset_name)

        (x_train_val, y_train_val), (x_test, y_test) = dataset.load_data()
        x_subset, y_subset = (
            (x_test, y_test) if subset == "test" else (x_train_val, y_train_val)
        )

        if len(x_subset.shape) == 3:
            x_subset = x_subset.reshape(x_subset.shape + (1,))

        self._input_shape = x_subset[0].shape
        self._num_classes = len(pd.np.unique(y_subset))

        y_subset = to_categorical(y_subset, self._num_classes)

        self._iterator = ImageDataGenerator(
            validation_split=validation_split,
            rescale=1 / 255,
            **data_augmentation or {}
        ).flow(
            x_subset,
            y_subset,
            batch_size=batch_size,
            shuffle=shuffle,
            **{"subset": subset} if subset != "test" else {}
        )

        self._annotations_df = pd.DataFrame(
            {"label_true": self._iterator.y.argmax(axis=1)}
        )

    def __len__(self):
        return len(self._iterator)

    def __getitem__(self, index):
        return self._iterator[index]

    @property
    def input_shape(self):
        return self._input_shape

    @property
    def num_classes(self):
        return self._num_classes

    @property
    def annotations_df(self):
        return self._annotations_df
