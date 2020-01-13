# pylint: disable=E0110

from unittest.mock import patch

from src.steps import AbstractStepWithCleanup


class TestAbstractStepWithCleanup:
    @staticmethod
    @patch.object(
        AbstractStepWithCleanup, "__abstractmethods__", set()
    )  # to be able to instantiate the abstract class
    def test_should_clear_tf_session():
        with patch.object(
            AbstractStepWithCleanup, "clear_tensorflow_session"
        ) as mock_clear_session:
            step = AbstractStepWithCleanup()
            step.apply()
        mock_clear_session.assert_called_once()
