import unittest
from unittest.mock import patch
from game_engine import Engine, Placement, Player

# Credit: tests written by ChatGPT, revised by me
class TestBattleshipGame(unittest.TestCase):
    def setUp(self):
        """Initialize engine and players before each test."""
        self.engine = Engine()
        self.player1 = self.engine.player1
        self.player2 = self.engine.player2


    def test_ship_placement_within_bounds_vertical(self):
        """Test placing a ship within the board boundaries (vertical orientation)."""
        placement = Placement(name="A", x=0, y=0, orientation="V", length=5)
        valid_placement = self.engine.valid_placement(placement, self.player1)
        self.assertTrue(valid_placement, "Ship placement should be within bounds.")


    def test_ship_placement_within_bounds_horizontal(self):
        """Test placing a ship within the board boundaries (horizontal orientation)."""
        placement = Placement(name="A", x=0, y=0, orientation="H", length=5)
        valid_placement = self.engine.valid_placement(placement, self.player1)
        self.assertTrue(valid_placement, "Ship placement should be within bounds.")
    
    
    def test_ship_placement_outside_bounds_vertical(self):
        """Test placing a ship outside the board boundaries (vertical orientation)."""
        placement = Placement(name="A", x=6, y=0, orientation="V", length=5)
        valid_placement = self.engine.valid_placement(placement, self.player1)
        self.assertFalse(valid_placement, "Ship placement should be outside bounds.")


    def test_ship_placement_outside_bounds_horizontal(self):
        """Test placing a ship outside the board boundaries (horizontal orientation)."""
        placement = Placement(name="A", x=0, y=6, orientation="H", length=5)
        valid_placement = self.engine.valid_placement(placement, self.player1)
        self.assertFalse(valid_placement, "Ship placement should be outside bounds.")
    
    
    def test_no_overlap_between_ships(self):
        """Test that ships do not overlap when placed."""
        # Place the first ship
        placement1 = Placement(name="A", x=0, y=0, orientation="H", length=5)
        self.player1.place_ship(placement1)
        
        # Place the second ship which overlaps with the first
        placement2 = Placement(name="B", x=0, y=4, orientation="V", length=4)
        valid_placement = self.engine.valid_placement(placement2, self.player1)
        self.assertFalse(valid_placement, "Ships should not overlap.")
    
    
    def test_attack_hit(self):
        """Test an attack that hits the opponent's ship."""
        placement = Placement(name="A", x=0, y=0, orientation="H", length=5)
        self.player2.place_ship(placement)

        # Player 1 attacks at (0, 0) where Player 2 has a ship
        self.player1.attack(self.player2, 0, 0)
        self.assertEqual(self.player2.get_player_board()[0][0], "X", "Player 2's ship should be hit.")
    
    
    def test_attack_miss(self):
        """Test an attack that misses the opponent's ship."""
        # Player 2 has no ships placed yet
        self.player1.attack(self.player2, 0, 0)
        self.assertEqual(self.player1.get_hits_misses()[0][0], "O", "Missed attack should be marked with 'O'.")


    def test_attack_on_same_spot_multiple_times(self):
        """Test attacking the same spot multiple times."""
        placement = Placement(name="A", x=0, y=0, orientation="H", length=5)
        self.player2.place_ship(placement)
        
        # Player 1 attacks at (0, 0) and (0, 0) again
        self.player1.attack(self.player2, 0, 0)
        self.player1.attack(self.player2, 0, 0)
        self.assertEqual(self.player2.get_player_board()[0][0], "X", "Second attack should not change the result.")


    def test_attack_out_of_bounds(self):
        """Test attacking out of bounds (coordinates outside the 10x10 board)."""
        attack_input = "K11"
        x, y = self.engine.convert_coordinates(attack_input)
        valid_format = self.engine.check_coord_bounds(x, y)
        self.assertFalse(valid_format, "Input coordinates should be invalid (out of bounds).")


    def test_invalid_ship_placement_format(self):
        """Test invalid ship placement format."""
        invalid_input = "A Z 12"  # Invalid format for ship placement
        valid_format = self.engine.check_input_format(invalid_input)
        self.assertFalse(valid_format, "Ship placement format should be invalid.")
    
    
    def test_valid_ship_placement_format(self):
        """Test valid ship placement format."""
        valid_input = "A H A1"
        valid_format = self.engine.check_input_format(valid_input)
        self.assertTrue(valid_format, "Ship placement format should be valid.")


if __name__ == "__main__":
    unittest.main()
