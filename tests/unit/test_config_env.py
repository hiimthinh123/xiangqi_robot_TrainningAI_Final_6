import unittest
import os
import importlib
import config


class TestConfigEnv(unittest.TestCase):
    def test_simulation_token_loaded_from_env(self):
        test_token = "test_bearer_token_12345"
        os.environ["SIMULATION_TOKEN"] = test_token
        try:
            importlib.reload(config)
            self.assertEqual(config.SIMULATION_TOKEN, test_token)
        finally:
            os.environ.pop("SIMULATION_TOKEN", None)
            importlib.reload(config)

    def test_robot_ip_loaded_from_env(self):
        test_ip = "192.168.1.99"
        os.environ["ROBOT_IP"] = test_ip
        try:
            importlib.reload(config)
            self.assertEqual(config.ROBOT_IP, test_ip)
        finally:
            os.environ.pop("ROBOT_IP", None)
            importlib.reload(config)

    def test_simulation_token_not_hardcoded(self):
        # Ensure that no hardcoded JWT token exists in config default
        os.environ.pop("SIMULATION_TOKEN", None)
        importlib.reload(config)
        self.assertFalse(config.SIMULATION_TOKEN.startswith("eyJ"), "Hardcoded JWT must not be present in source code")


if __name__ == "__main__":
    unittest.main()
