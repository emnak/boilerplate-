"""
Configure Tensorflow for GPU use
"""
import tensorflow as tf
from pipeline.steps import AbstractStep

from utils.logger import get_logger

LOGGER = get_logger("set-gpu-config")


# pylint: disable=W0221
class SetGPUConfig(AbstractStep):
    """
    A class to configure Tensorflow for rtx GPU
    """

    def __init__(self):
        """
        Configure Tensorflow for GPU use.
        Memory growth setting should be done before any tensor allocation or operation.
        """
        physical_devices = tf.config.experimental.list_physical_devices("GPU")
        if physical_devices:
            tf.config.experimental.set_memory_growth(physical_devices[0], True)
            LOGGER.info("GPU device found, memory growth set to True")
        else:
            LOGGER.info("No GPU device found")

    def apply(self):
        pass

    @staticmethod
    def dump_output(output_object, *args, **kwargs):
        pass
