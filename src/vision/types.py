# =============================================================================
# === FILE: src/vision/types.py ===
# === Data Contracts & Immutable Snapshots cho Perception Pipeline (V3/V4) ===
# =============================================================================

from dataclasses import dataclass, field
import time
from typing import Optional, List, Any


@dataclass
class BaselineSnapshot:
    """Ảnh chụp baseline bất biến lưu trữ toàn vẹn trạng thái trước khi người chơi đi.
    
    Khắc phục triệt để lỗi phân mảnh (lưu riêng occupancy, quên lưu frame thực,
    không lưu pose_version của bàn cờ).
    """
    frame: Any                         # OpenCV image frame (BGR)
    detections: list                   # list of (cls_id, conf, (x1, y1, x2, y2))
    occupancy: List[List[bool]]        # 10x9 grid of bool (True=có quân, False=trống)
    timestamp: float = field(default_factory=time.time)
    board_state: Optional[Any] = None  # Bản sao trạng thái memory board (10x9)
    board_pose: Optional[Any] = None   # T_camera_board transform nếu có
    pose_version: int = 0              # Phiên bản góc đặt của bàn cờ (BoardPose version)


@dataclass
class FramePacket:
    """Gói dữ liệu đồng bộ giữa camera capture và pipeline suy luận.
    
    Đảm bảo frame và detection luôn gắn liền với đúng frame_id và timestamp,
    tránh hiện tượng ghép detection cũ của frame trước với frame hiện tại.
    """
    frame_id: int
    timestamp: float
    frame: Any
    detections: list = field(default_factory=list)
    board_pose: Optional[Any] = None
    pose_version: int = 0
