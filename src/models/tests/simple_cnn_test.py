from tensorflow.keras import models

from src.models import simple_cnn


def test_should_return_a_keras_model():
    model = simple_cnn(input_shape=(28, 28, 1), classes=5)

    assert isinstance(model, models.Model)
