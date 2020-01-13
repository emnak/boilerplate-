import abc

import tensorflow.keras.backend as K
from pipeline.steps import AbstractStep


class AbstractStepWithCleanup(AbstractStep):
    """
    A kind of Step which performs tensorflow session cleanup after applying modifications to the input objects
    """

    def apply(self, *input_objects):
        """
        Apply a modification to an input object and then clean up the corresponding tensorflow session
        Args:
            *input_objects (Any): input passed to the Step (ex: a DataFrame, several DataFrames, a dict...)

        Returns:
            apply_output (Any): the output object (ex: a DataFrame, a list of DataFrames, an image...)
        """
        apply_output = self.apply_workflow(*input_objects)
        self.clear_tensorflow_session()
        return apply_output

    @staticmethod
    def clear_tensorflow_session():
        """
        Apply the tensorflow session cleanup
        """
        K.clear_session()

    @abc.abstractmethod
    def apply_workflow(self, *input_objects):
        """
        Apply a modification to an input object.
        Args:
            input_objects (Any): input passed to the Step (ex: a DataFrame, several DataFrames, a dict...)
        """
        pass
