# pylint: disable=invalid-name
import numpy as np
import pytest

from src import models


@pytest.fixture(
    params=[model_name for model_name in dir(models) if not model_name.startswith("_")]
)
def model_function(request):
    yield getattr(models, request.param)


def test_should_return_correct_vector_size(model_function):
    model = model_function(input_shape=(50, 50, 3), classes=6)

    input_images = np.zeros((2, 50, 50, 3))
    predicted_classes = model.predict(input_images)

    assert predicted_classes.shape == (2, 6)
