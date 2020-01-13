from unittest.mock import patch

from src.steps.init_gpu_on_tensorflow import SetGPUConfig


class TestSetGPUConfig:
    @staticmethod
    @patch("tensorflow.config.experimental.list_physical_devices")
    @patch("tensorflow.config.experimental.set_memory_growth")
    def test_should_not_configure_when_no_gpu_found(
        mock_set_memory_growth, mock_list_physical_devices
    ):
        mock_list_physical_devices.return_value = []
        set_gpu_config = SetGPUConfig()
        set_gpu_config.apply()
        mock_set_memory_growth.assert_not_called()

    @staticmethod
    @patch("tensorflow.config.experimental.list_physical_devices")
    @patch("tensorflow.config.experimental.set_memory_growth")
    def test_should_configure_when_gpu_found(
        mock_set_memory_growth, mock_list_physical_devices
    ):
        mock_list_physical_devices.return_value = [1]
        set_gpu_config = SetGPUConfig()
        set_gpu_config.apply()
        mock_set_memory_growth.assert_called_once()
