import unittest
import numpy as np
from src.vision.types import BaselineSnapshot
from src.vision.snapshot_detector import SnapshotDetector
from src.core import xiangqi


class TestBaselineSnapshot(unittest.TestCase):
    def setUp(self):
        # Create a mock detector with dummy perspective
        self.detector = SnapshotDetector(perspective_path="dummy.npy")
        # Override perspective matrix with identity to avoid needing dummy.npy on disk
        self.detector.M = np.eye(3, dtype=np.float32)

    def test_snapshot_dataclass(self):
        occ = [[False]*9 for _ in range(10)]
        occ[0][0] = True
        snapshot = BaselineSnapshot(
            frame=np.zeros((100, 100, 3), dtype=np.uint8),
            detections=[(0, 0.95, (10, 10, 20, 20))],
            occupancy=occ,
            timestamp=12345.67,
            pose_version=1
        )
        self.assertEqual(snapshot.pose_version, 1)
        self.assertEqual(snapshot.timestamp, 12345.67)
        self.assertTrue(snapshot.occupancy[0][0])
        self.assertEqual(len(snapshot.detections), 1)

    def test_detector_baseline_encapsulation(self):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = []
        
        self.assertFalse(self.detector.has_baseline())
        self.assertIsNone(self.detector.get_baseline())

        success = self.detector.capture_baseline(frame, detections, pose_version=2)
        self.assertTrue(success)
        self.assertTrue(self.detector.has_baseline())
        
        snapshot = self.detector.get_baseline()
        self.assertIsNotNone(snapshot)
        self.assertIsInstance(snapshot, BaselineSnapshot)
        self.assertEqual(snapshot.pose_version, 2)
        
        # Test backward-compatibility properties
        self.assertIsNotNone(self.detector._baseline_occ)
        self.assertIsNotNone(self.detector._baseline_frame)
        self.assertIsNotNone(self.detector._baseline_time)

        # Test clear
        self.detector.clear_baseline()
        self.assertFalse(self.detector.has_baseline())
        self.assertIsNone(self.detector.get_baseline())

        # Test set_baseline
        self.detector.set_baseline(snapshot)
        self.assertTrue(self.detector.has_baseline())
        self.assertEqual(self.detector.get_baseline().pose_version, 2)

    def test_multi_piece_change_refusal(self):
        # Simulate baseline with 2 red pieces
        board = xiangqi.get_board()
        # Red Cannon at (1, 7) and (7, 7)
        t1_occ = [[False]*9 for _ in range(10)]
        t1_occ[7][1] = True
        t1_occ[7][7] = True
        
        # T2: both red cannons disappeared
        t2_occ = [[False]*9 for _ in range(10)]
        
        snapshot = BaselineSnapshot(
            frame=np.zeros((480, 640, 3), dtype=np.uint8),
            detections=[],
            occupancy=t1_occ,
            timestamp=100.0
        )
        self.detector.set_baseline(snapshot)

        # Mock _build_occupancy to return t2_occ
        self.detector._build_occupancy = lambda dets: t2_occ

        # When detecting move with 2 disappeared red pieces, it must reject (anti-cheat)
        src, dst, piece = self.detector.detect_move(
            frame=np.zeros((480, 640, 3), dtype=np.uint8),
            detections=[],
            board=board
        )
        self.assertIsNone(src, "Multi-piece change must return None for src")
        self.assertIsNone(dst, "Multi-piece change must return None for dst")
        self.assertIsNone(piece, "Multi-piece change must return None for piece")


if __name__ == "__main__":
    unittest.main()
