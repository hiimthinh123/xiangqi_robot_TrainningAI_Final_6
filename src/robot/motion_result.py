# =============================================================================
# === FILE: src/robot/motion_result.py ===
# === Chuẩn hóa kết quả vận hành cánh tay Robot (Closed-loop semantics) ===
# =============================================================================

from enum import Enum
from typing import Optional, Dict, Any


class MotionStatus(Enum):
    """Trạng thái thực thi chuyển động của robot."""
    SUCCESS = "success"        # Lệnh đã thực thi thành công hoàn toàn
    FAILED = "failed"          # Lỗi vật lý hoặc SDK từ chối thực thi
    UNCERTAIN = "uncertain"    # Trạng thái chưa rõ ràng (cần vision/cảm biến xác minh lại)


class MotionResult:
    """Đối tượng phản hồi tiêu chuẩn sau mỗi hành động vật lý của Robot.
    
    Nguyên tắc vàng: Command sent != Action succeeded.
    Không bao giờ giả định một lệnh gửi qua mạng/SDK là đã thành công nếu controller
    hoặc cảm biến chưa chứng minh được điều đó.
    """

    def __init__(
        self,
        status: MotionStatus,
        error_code: int = 0,
        message: str = "",
        details: Optional[Dict[str, Any]] = None
    ):
        self.status = status
        self.error_code = error_code
        self.message = message
        self.details = details or {}

    def is_success(self) -> bool:
        """Kiểm tra nếu chuyển động hoàn toàn thành công."""
        return self.status == MotionStatus.SUCCESS

    def is_failed(self) -> bool:
        """Kiểm tra nếu chuyển động thất bại."""
        return self.status == MotionStatus.FAILED

    def is_uncertain(self) -> bool:
        """Kiểm tra nếu trạng thái chuyển động không chắc chắn (cần xác minh thêm)."""
        return self.status == MotionStatus.UNCERTAIN

    def __bool__(self) -> bool:
        """Cho phép dùng 'if result:' tương đương 'if result.is_success():'"""
        return self.is_success()

    def __repr__(self) -> str:
        return (
            f"MotionResult(status={self.status.value}, "
            f"code={self.error_code}, msg='{self.message}')"
        )
