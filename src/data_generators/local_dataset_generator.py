import os

import pandas as pd
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import Sequence


class LocalDatasetGenerator(Sequence):
    """
    Generates images batches from local dataset, for the chosen subset ('training', 'validation' or 'test').
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        dataset_path,
        batch_size,
        target_size,
        shuffle=True,
        class_mode="categorical",
        subset="training",
        validation_split=0.0,
        data_augmentation=None,
    ):
        """
        Args:
            dataset_path (str): a path to a folder containing images split into 'train' / 'test' and classes:
                |_ train
                |  |_ class_A
                |  |  |_ image_1.jpg
                |  |  |_ image_2.jpg
                |  |  |_ ...
                |  |
                |  |_ class_B
                |
                |_ test
                   |_ class_A
                   |  |_ ...
                   |_ ...
                > Note that you're not supposed to have a val folder. The validation split can be made among the train
                    folder thanks to the `validation_split` parameter.
            batch_size (int): number of images per batch.
            target_size (Tuple[int]): tuple with (image width, images height) to use.
            shuffle (bool): whether to shuffle the data (default: True).
                > Note that data is shuffled after splitting between validation and training.
            class_mode (str): 'categorical', 'binary' or None, see Keras `flow_from_directory` documentation
            subset (str): 'training', 'validation' or 'test'.
                    - 'training' corresponds to a subset of the 'train' sub_folder, determined by 'validation_split'.
                    - 'validation' corresponds to the other subset of  the 'train' sub_folder.
                    - 'test' exactly corresponds to the 'test' sub_folder
            validation_split (float): how to split images from 'train' sub_folder into 'training' and 'validation'.
                    - 'training' set will be images: validation_split * len(train set) -> len(train set)
                    - 'validation' set will be images: 0 -> validation_split * len(train set)
            data_augmentation (dict): parameters to be passed to Keras ImageDataGenerator to randomly augment images.
        """
        if subset not in ["training", "validation", "test"]:
            raise ValueError("subset should be 'training', 'validation' or 'test'")

        self._batch_size = batch_size

        sub_folder = os.path.join(dataset_path, "test" if subset == "test" else "train")

        self._input_shape = tuple(target_size) + (3,)

        self._iterator = ImageDataGenerator(
            validation_split=validation_split,
            rescale=1 / 255,
            **data_augmentation or {}
        ).flow_from_directory(
            sub_folder,
            batch_size=batch_size,
            target_size=target_size,
            shuffle=shuffle,
            class_mode=class_mode,
            **{"subset": subset} if subset != "test" else {}
        )

        # Iterator filename scheme is '{class}/{image_name}'. We extract only image_names from it.
        image_names = [
            image_scheme.split("/", 1)[1] for image_scheme in self._iterator.filenames
        ]

        self._annotations_df = pd.DataFrame(
            {"image_name": image_names, "label_true": self._iterator.labels}
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
        return self._iterator.num_classes

    @property
    def annotations_df(self):
        return self._annotations_df

    @property
    def ordered_labels(self):
        return sorted(
            list(self._iterator.class_indices),
            key=lambda label: self._iterator.class_indices[label],
        )
