import unittest
from src.core import xiangqi


class TestAIMoveValidation(unittest.TestCase):
    def setUp(self):
        self.board = xiangqi.get_board()

    def test_valid_black_moves_at_start(self):
        # Cannon c2 -> e2 (col 1, row 2 -> col 4, row 2) is valid
        self.assertTrue(xiangqi.is_valid_move((1, 2), (4, 2), self.board, "b"))
        # Horse b0 -> c2 (col 1, row 0 -> col 2, row 2) is valid
        self.assertTrue(xiangqi.is_valid_move((1, 0), (2, 2), self.board, "b"))
        # Horse h0 -> g2 (col 7, row 0 -> col 6, row 2) is valid
        self.assertTrue(xiangqi.is_valid_move((7, 0), (6, 2), self.board, "b"))

    def test_invalid_black_moves_rejected(self):
        # Moving wrong color (trying to move red piece as black)
        self.assertFalse(xiangqi.is_valid_move((0, 9), (0, 8), self.board, "b"))
        # Moving empty spot
        self.assertFalse(xiangqi.is_valid_move((4, 4), (4, 5), self.board, "b"))
        # Rook jumping over piece
        self.assertFalse(xiangqi.is_valid_move((0, 0), (0, 5), self.board, "b"))
        # Horse blocked by obstacle (mã kẹt chân)
        # Place blocking piece at (1, 1) directly in front of horse at (1, 0)
        blocked_board = [row[:] for row in self.board]
        blocked_board[1][1] = 'b_P'
        self.assertFalse(xiangqi.is_valid_move((1, 0), (2, 2), blocked_board, "b"))

    def test_flying_general_check(self):
        # If both kings face each other on the same file with no pieces between, move is illegal
        custom_board = [['.' for _ in range(9)] for _ in range(10)]
        custom_board[0][4] = 'b_K'
        custom_board[9][4] = 'r_K'
        custom_board[5][4] = 'b_R' # Black rook is shielding the kings
        
        # Moving the black rook off the file (col 4 -> col 0) exposes kings directly -> illegal
        self.assertFalse(xiangqi.is_valid_move((4, 5), (0, 5), custom_board, "b"))
        # Moving along the file stays shielding -> legal
        self.assertTrue(xiangqi.is_valid_move((4, 5), (4, 6), custom_board, "b"))


if __name__ == "__main__":
    unittest.main()
