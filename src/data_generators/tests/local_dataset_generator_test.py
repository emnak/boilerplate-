import pandas as pd

from src.data_generators.local_dataset_generator import LocalDatasetGenerator


class TestLocalDatasetGenerator:
    class TestInit:
        @staticmethod
        def test_should_should_initialize_with_correct_attributes():

            dataset_path = "data/samples/"
            batch_size = 2
            target_size = [200, 200]

            local_dataset_generator = LocalDatasetGenerator(
                dataset_path,
                batch_size,
                target_size,
                shuffle=False,
                subset="training",
                validation_split=0.0,
            )

            expected_input_shape = (200, 200, 3)
            expected_num_classes = 2
            expected_annotation_df = pd.DataFrame(
                {
                    "image_name": [
                        "chat_mignon1.jpg",
                        "chat_mignon2.jpg",
                        "chat_mignon3.jpg",
                        "chien_moche1.jpg",
                        "chien_moche2.jpg",
                        "chien_moche3.jpg",
                    ],
                    "label_true": [0, 0, 0, 1, 1, 1],
                }
            )

            input_shape = local_dataset_generator.input_shape
            num_classes = local_dataset_generator.num_classes
            annotation_df = local_dataset_generator.annotations_df

            pd.testing.assert_frame_equal(
                annotation_df, expected_annotation_df, check_dtype=False
            )
            assert input_shape == expected_input_shape
            assert num_classes == expected_num_classes
            assert len(local_dataset_generator) == 3
            assert local_dataset_generator[0][0].shape == (2, 200, 200, 3)
