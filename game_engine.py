from time import sleep

class Ship:
    def __init__(self, name, length, num_available):
        self.name = name
        self.length = length
        self.num_available = num_available

    def get_name(self):
        return self.name
        
    def get_length(self):
        return self.length

    def get_available(self):
        return self.num_available
    
    def __iter__(self):
        return iter((self.name, self.length, self.num_available))


class Placement:
    def __init__(self, name, x, y, orientation, length):
        self.name = name
        self.x = x
        self.y = y
        self.orientation = orientation
        self.length = length
        
    def get_coords(self):
        return (self.x, self.y)

    def get_orientation(self):
        return self.orientation

    def get_length(self):
        return self.length

    def get_ship_name(self):
        return self.name
    
    def __iter__(self):
        return iter((self.name, self.x, self.y, self.length, self.orientation))


class Player:
    def __init__(self, id):
        self.id = id
        self.hits_received = 0
        self.player_board = [["-" for _ in range(10)] for _ in range(10)]
        self.hits_misses = [["-" for _ in range(10)] for _ in range(10)]
        self.inventory = {
            "A" : Ship(name="Aircraft_Carrier",length=5, num_available=1),
            "B" : Ship(name="Battleship", length=4, num_available=1),
            "C" : Ship(name="Cruiser", length=3, num_available=1),
            "D" : Ship(name="Destroyer", length=2, num_available=2),
            "S" : Ship(name="Submarine", length=1, num_available=2)
        }
    
    def get_id(self):
        return self.id
    
    def get_hits_received(self):
        return self.hits_received
    
    def get_player_board(self):
        return self.player_board
    
    def get_hits_misses(self):
        return self.hits_misses
        
    def get_inventory(self):
        return self.inventory
    
    def get_ship_data(self, ship_name):
        return self.inventory[ship_name]

    def ship_available(self, placement: Placement):
        ship_name = placement.get_ship_name()
        return (self.inventory[ship_name].num_available > 0)
        
    def check_nonoverlap(self, placement: Placement):
        """Ensures placement does not overlap with existing ships"""
        _, x, y, length, orientation = placement
        for i in range(length):
            if orientation == "V":
                if self.player_board[x + i][y] == '1':
                    return False
            else:
                if self.player_board[x][y + i] == '1':
                    return False
        return True
        
    def place_ship(self, placement: Placement):
        """Demarkates a placement with 1s on self.player_board"""
        ship_name, x, y, length, orientation = placement
        for i in range(length):
            if orientation == "V":
                self.player_board[x + i][y] = "1"
            else:
                self.player_board[x][y + i] = '1'
        self.inventory[ship_name].num_available -= 1
            
    def inc_hits(self):
        self.hits_received += 1
    
    def attack(self, opponent: 'Player', x, y):
        """Marks attack on (x,y) as hit or miss
        Returns True on hit, False on miss"""
        opponent_placements = opponent.get_player_board()
        if opponent_placements[x][y] == '1' and self.hits_misses[x][y] == '-':
            opponent.inc_hits()
            self.hits_misses[x][y] = "X"
            return True
        elif opponent_placements[x][y] == '-':
            self.hits_misses[x][y] = "O"
        return False

                
class Engine:
    def __init__(self):
        self.player1_turn = True
        self.ships_placed = 0
        self.player1 = Player(id=1)
        self.player2 = Player(id=2)
     
    def get_player(self, id):
         return self.player1 if id == 1 else self.player2 if id == 2 else None
     
    def is_player_turn(self, id):
        return self.player1_turn if id == 1 else not self.player1_turn if id == 2 else None
    
    def pass_turn(self):
        self.player1_turn = not self.player1_turn
        
    def check_coord_bounds(self, x, y):
        """Checks that coordinates, but not necessarily placement, are within bounds"""
        lower_bound, upper_bound = 0, 9
        return (lower_bound <= x <= upper_bound) and (lower_bound <= y <= upper_bound)
        
    def placement_in_bounds(self, placement: Placement):
        """Checks ship remains within bounds when placed"""
        _, x, y, length, orientation = placement
        if (orientation == 'V') and (x + length > 10):
            return False
        elif (orientation == 'H') and (y + length > 10):
            return False
        return True

    def valid_placement(self, placement: Placement, player: Player):
        """Ensures a placement is legal"""
        return (
            self.placement_in_bounds(placement) and 
            player.check_nonoverlap(placement) and 
            player.ship_available(placement)
        )
            
    def check_game_end(self):
        """Returns true when all of a player's ships have been sunk"""
        HITS_POSSIBLE = 18 # Sum of lengths of each ship in a player's inventory
        return (self.player1.get_hits_received() == HITS_POSSIBLE) or (self.player2.get_hits_received() == HITS_POSSIBLE)