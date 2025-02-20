import os


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
        self.opponent_board = [["-" for _ in range(10)] for _ in range(10)]
        self.inventory = {
            "A" : Ship(name="Aircraft_Carrier",length=5, num_available=1),
            "B" : Ship(name="Battleship", length=4, num_available=1),
            "C" : Ship(name="Cruiser", length=3, num_available=1),
            "D" : Ship(name="Destroyer", length=2, num_available=2),
            "S" : Ship(name="Submarine", length=1, num_available=2)
        }
    
    
    def get_id(self):
        return self.id
    
    
    def get_hits_taken(self):
        return self.hits_received
    
    
    def get_player_board(self):
        return self.player_board
    
    
    def get_opponent_board(self):
        return self.opponent_board
    
        
    def get_inventory(self):
        return self.inventory
    
    
    def get_ship_data(self, ship_name):
        return self.inventory[ship_name]
    

    def ship_available(self, placement: Placement):
        ship_name = placement.get_ship_name()
        return (self.inventory[ship_name].num_available > 0)

        
    def check_nonoverlap(self, placement: Placement):
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
        ship_name, x, y, length, orientation = placement
        for i in range(length):
            if orientation == "V":
                self.player_board[x + i][y] = "1"
            else:
                self.player_board[x][y + i] = '1'
        self.inventory[ship_name].num_available -= 1
        
    
    def receive_hit(self, x, y):
        self.player_board[x][y] = "X"
    

    def inc_hits(self):
        self.hits_received += 1
        
    
    def attack(self, opponent: 'Player', x, y):
        opponent_placements = opponent.get_player_board()
        if opponent_placements[x][y] == '1':
            opponent.inc_hits()
            opponent.receive_hit(x, y)
            self.opponent_board[x][y] = "X"
        elif opponent_placements[x][y] == '-':
            self.opponent_board[x][y] = "O"

                
class Engine:
    def __init__(self):
        self.player1_turn = True
        self.ships_placed = 0
        self.player1 = Player(id=1)
        self.player2 = Player(id=2)
     
     
    def get_player(self, id): # TODO: input error checking
         return self.player1 if id == 1 else self.player2
     
     
    def is_player_turn(self, id):
        return self.player1_turn if id == 1 else not self.player1_turn
    
    
    def pass_turn(self):
        self.player1_turn = not self.player1_turn
     
    
    def check_ship_name(self, user_ship):
        SHIP_SYMBOLS = {"A", "B", "C", "D", "S"}
        return user_ship in SHIP_SYMBOLS
    
    
    def check_orientation(self, user_orientation):
        ORIENTATIONS = {"V", "H"}
        return user_orientation in ORIENTATIONS


    def check_coord_format(self, user_coords):
        if len(user_coords) != 2 and len(user_coords) != 3:
            return False
        if not user_coords[0].isalpha() or not user_coords[1:].isnumeric(): 
            return False
        return True
 

    def check_input_format(self, user_input):
        args = user_input.split()
        if len(args) != 3:
            return False
        ship_name, orientation, user_coords = args
        return (self.check_ship_name(ship_name) and self.check_orientation(orientation) and self.check_coord_format(user_coords))


    def convert_coordinates(self, user_input):
        internal_x = ord(user_input[0]) - ord('A')
        internal_y = int(user_input[1]) - 1 if len(user_input) == 2 else int(user_input[1:]) - 1
        return internal_x, internal_y
    
    
    def check_coord_bounds(self, x, y):
        lower_bound, upper_bound = 0, 9
        return (lower_bound <= x <= upper_bound) and (lower_bound <= y <= upper_bound)
        
    
    def get_placement(self, user_input: str):
        ship_name, orientation, user_coords = user_input.split()
        internal_x, internal_y = self.convert_coordinates(user_coords)
        ship_length = self.player1.get_ship_data(ship_name).get_length()
        return Placement(name=ship_name, x=internal_x, y=internal_y, length=ship_length, orientation=orientation)

    
    def placement_in_bounds(self, placement: Placement):
        _, x, y, length, orientation = placement
        if (orientation == 'V') and (x + length > 10):
            return False
        elif (orientation == 'H') and (y + length > 10):
            return False
        return True

    
    def valid_placement(self, placement, player: Player):
        return (
            self.placement_in_bounds(placement) and 
            player.check_nonoverlap(placement) and 
            player.ship_available(placement)
        )
    
    
    def run_placement_phase(self):
        SHIPS_PER_PLAYER = 7
        ships_placed = 0
        while ships_placed < SHIPS_PER_PLAYER * 2:            
            self.print_placement_instructions()
            curr_player = self.player1 if ships_placed < SHIPS_PER_PLAYER else self.player2
            user_input = self.prompt_ship_placement(curr_player)
            if self.check_input_format(user_input):
                placement = self.get_placement(user_input)
                is_valid = self.valid_placement(placement, curr_player)
                if is_valid:                    
                    curr_player.place_ship(placement)
                    ships_placed += 1
                else:
                    print("Illegal placement. Please try again.")
            os.system('cls' if os.name == 'nt' else 'clear') # Clears terminal output                
            
            
    def check_game_end(self):
        HITS_POSSIBLE = 15 # Sum of lengths of each ship in a player's inventory
        return (self.player1.get_hits_taken() == HITS_POSSIBLE) or (self.player2.get_hits_taken() == HITS_POSSIBLE)