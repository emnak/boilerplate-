from src.data_generators.keras_dataset_generator import KerasDatasetGenerator


class TestLocalDatasetGenerator:
    class TestInit:
        @staticmethod
        def test_should_should_initialize_with_correct_attributes():

            dataset_name = "mnist"
            batch_size = 2

            keras_dataset_generator = KerasDatasetGenerator(
                dataset_name, batch_size, subset="training", validation_split=0.1
            )

            assert keras_dataset_generator.input_shape == (28, 28, 1)
            assert keras_dataset_generator.num_classes == 10
            assert (
                len(keras_dataset_generator.annotations_df.label_true.value_counts())
                == 10
            )
            assert len(keras_dataset_generator) == 30000 * 0.9
            assert keras_dataset_generator[0][0].shape == (2, 28, 28, 1)
