from tensorflow.keras import Model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Dense


def vgg16(classes, input_shape):
    """ Builds a simple Keras CNN model with two convolutional layers and two dense layers.

    Args:
        classes (int): the number of output classes.
        input_shape (tuple[int]): a triple (image_height, image_width, num_channels).

    Returns:
        keras.Model: A keras model
    """
    base_model = VGG16(
        input_shape=input_shape, weights="imagenet", include_top=False, pooling="max"
    )

    for layer in base_model.layers:
        layer.trainable = False

    output = base_model.output
    output = Dense(classes, activation="softmax")(output)

    model = Model(base_model.input, output)

    return model
