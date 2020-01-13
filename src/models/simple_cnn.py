from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential


def simple_cnn(classes, input_shape, class_mode="categorical"):
    """ Builds a simple Keras CNN model with two convolutional layers and two dense layers.

    Args:
        classes (int): the number of output classes.
        input_shape (tuple[int]): a triple (image_height, image_width, num_channels).
        class_mode (str): 'categorical' or 'binary'.
            - if 'categorical': output has a length of classes
            - if 'binary': output has a length of 1 (and an error is raised if classes != 2)
    Returns:
        keras.models.Sequential: A keras sequential model
    """
    output_length = classes
    activation = "softmax"
    if class_mode == "binary":
        if classes != 2:
            raise ValueError("class_mode cannot be 'binary' with classes != 2")
        output_length = 1
        activation = "sigmoid"

    model = Sequential()

    model.add(
        Conv2D(
            filters=32, kernel_size=(3, 3), activation="relu", input_shape=input_shape
        )
    )

    model.add(Conv2D(filters=64, kernel_size=(3, 3), activation="relu"))

    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(output_length, activation=activation))

    return model
