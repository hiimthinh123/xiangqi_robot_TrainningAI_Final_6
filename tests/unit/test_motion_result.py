import unittest
from src.robot.motion_result import MotionStatus, MotionResult


class TestMotionResult(unittest.TestCase):
    def test_motion_status_enum(self):
        self.assertEqual(MotionStatus.SUCCESS.value, "success")
        self.assertEqual(MotionStatus.FAILED.value, "failed")
        self.assertEqual(MotionStatus.UNCERTAIN.value, "uncertain")

    def test_motion_result_success(self):
        res = MotionResult(MotionStatus.SUCCESS, error_code=0, message="OK")
        self.assertTrue(res.is_success())
        self.assertFalse(res.is_failed())
        self.assertFalse(res.is_uncertain())
        self.assertTrue(bool(res))
        self.assertEqual(res.error_code, 0)
        self.assertEqual(res.message, "OK")

    def test_motion_result_failed(self):
        res = MotionResult(MotionStatus.FAILED, error_code=-1, message="Connection failed")
        self.assertFalse(res.is_success())
        self.assertTrue(res.is_failed())
        self.assertFalse(res.is_uncertain())
        self.assertFalse(bool(res))
        self.assertEqual(res.error_code, -1)

    def test_motion_result_uncertain(self):
        # Code 112 from Fairino SDK is an unconfirmed trajectory completion
        res = MotionResult(MotionStatus.UNCERTAIN, error_code=112, message="Motion finished with code 112")
        self.assertFalse(res.is_success(), "UNCERTAIN must NOT be treated as success")
        self.assertFalse(res.is_failed())
        self.assertTrue(res.is_uncertain())
        self.assertFalse(bool(res), "UNCERTAIN must evaluate to False in boolean context")
        self.assertEqual(res.error_code, 112)

    def test_to_dict(self):
        res = MotionResult(MotionStatus.SUCCESS, 0, "All good", {"speed": 25})
        d = res.to_dict()
        self.assertEqual(d["status"], "success")
        self.assertEqual(d["error_code"], 0)
        self.assertEqual(d["message"], "All good")
        self.assertEqual(d["data"], {"speed": 25})


if __name__ == "__main__":
    unittest.main()
