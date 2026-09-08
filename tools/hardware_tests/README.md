# Hardware Commissioning & Calibration Scripts

Thư mục này chứa các kịch bản kiểm tra phần cứng (Hardware Commissioning / Bring-up Scripts) trực tiếp với robot FR5 thật hoặc chế độ mô phỏng (`--dry`).

> ⚠️ **LƯU Ý AN TOÀN:**
> Các kịch bản này yêu cầu tương tác thủ công của kỹ sư vận hành (bấm phím, quan sát thực tế bàn cờ và robot).
> Chúng **KHÔNG PHẢI** là automated unit/regression tests và đã được tách riêng khỏi thư mục `tests/` để không làm gián đoạn CI/CD pipeline tự động.

## Danh sách kịch bản

1. **`test_corners.py`**:
   - Di chuyển tay robot đến 4 góc bàn cờ (R1: Xe Đen Trái, R2: Xe Đen Phải, R3: Xe Đỏ Phải, R4: Xe Đỏ Trái).
   - Kiểm tra ma trận nội suy bilinear và điểm teaching R1-R4.
   - Chạy: `python tools/hardware_tests/test_corners.py --dry` hoặc `python tools/hardware_tests/test_corners.py`

2. **`test_4_rooks.py`**:
   - Test chu trình gắp đặt 4 quân Xe ở 4 góc.
   - Chạy: `python tools/hardware_tests/test_4_rooks.py --dry`

3. **`test_goto_xe_den.py`**:
   - Test di chuyển an toàn đến vị trí Xe đen.
   - Chạy: `python tools/hardware_tests/test_goto_xe_den.py --dry`

4. **`test_calculate_cell_size.py`**:
   - Tính toán kích thước ô cờ thực tế dựa trên camera và điểm chiếu.
   - Chạy: `python tools/hardware_tests/test_calculate_cell_size.py`

5. **`test_move_to_pos.py`**:
   - Di chuyển robot đến một vị trí grid `(col, row)` cụ thể.
   - Chạy: `python tools/hardware_tests/test_move_to_pos.py --col 4 --row 5 --dry`

6. **`test_tool_do0.py`**:
   - Kiểm tra thiết lập tool frame độ 0 của gripper.
   - Chạy: `python tools/hardware_tests/test_tool_do0.py`
