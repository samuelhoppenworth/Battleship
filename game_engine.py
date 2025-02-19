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
    
            
    def receive_hit(self, x, y):
        self.player_board[x][y] = "X"
    

    def inc_hits(self):
        self.hits_received += 1
        
    
    def attack(self, opponent: 'Player', x, y):
        opponent_placements = opponent.get_player_board()
        if opponent_placements[x][y] == '1':
            opponent.inc_hits()
            opponent.receive_hit()
            self.opponent_board[x][y] = "X"
        elif opponent_placements[x][y] == '-':
            self.opponent_board[x][y] = "O"


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
                

class Engine:
    def __init__(self):
        self.player1_turn = True
        self.ships_placed = 0
        self.player1 = Player(id=1)
        self.player2 = Player(id=2)
     

    def print_placement_instructions(self):
        os.system('cls' if os.name == 'nt' else 'clear') # Clears terminal output
        divider_width = 140
        print("-" * divider_width + """\nINSTRUCTIONS
              The orientation specifies whether the ship is placed vertically or horizontally, and the
              coordinate species the location of the top-left square of the ship. So if a ship is vertical, the coordinate
              specifies the ship's top-most square. If the ship is horizontal, the coordinate specifies the ship's left-most square.
              Example: \"C V A4\" indicates placing a Cruiser vertically such that its top most digit is on A4
              """)
        print("-" * divider_width + """\nORIENTATIONS
              V (vertical)
              H (horizontal)
              """)
        print("-" * divider_width + """\nCOORDINATES
              First coordinate: letters between A and J, inclusive
              Second coordinate: numbers between 1 and 10, inclusive
              """)
    

    def prompt_ship_placement(self, curr_player: Player):
        # Credit: the formatting of the output of this function was improved with ChatGPT
        ship_name_width = 25
        ship_length_width = 15
        inventory_width = 15
        divider_width = 140

        print("\n" + "-" * divider_width)
        print(f"{'SHIP SYMBOL/NAME':<{ship_name_width}}{'SHIP LENGTH':<{ship_length_width}}{'LEFT TO PLACE':<{inventory_width}}")
        for ship_symbol, ship in curr_player.get_inventory().items():
            name, length, available = ship
            print(f"({ship_symbol}) {name:<{ship_name_width - 4}}{length} squares{'':<{ship_length_width - len(str(length)) - 8}}{available:<{inventory_width}}")

        print("\n" + "-" * divider_width + "\nCurrent placements: ")
        for row in curr_player.get_player_board():
            print(f"\t{row}")

        user_input = input("\n" + "-" * divider_width + f"\nPLAYER {curr_player.id} INPUT: ")
        return user_input
            
    
    def prompt_attack(self):
        curr_player = self.player1 if self.player1_turn else self.player2
        divider_width = 140
        print("-" * divider_width + "\nHits/Misses:")            
        for row in curr_player.get_opponent_board():
            print(f"\t{row}")

        return input("\n" + "-" * divider_width  + f"\nPLAYER {curr_player.get_id()}, input coordinates to attack: ")


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
           
           
    def run_battle_phase(self):
        game_end = 0
        while not game_end:
            curr_player = self.player1 if self.player1_turn else self.player2
            opponent = self.player1 if not self.player1_turn else self.player2
            attack_input = self.prompt_attack()
            if self.check_coord_format(attack_input):                
                x, y = self.convert_coordinates(attack_input)
                if self.check_coord_bounds(x, y): 
                    curr_player.attack(opponent, x, y) # nothing stops player from guessing same square more than once
                    self.player1_turn = not self.player1_turn
                else:
                    print("Coordinates not in bounds")
            else:
                print("Coordinates improperly formatted")
            game_end = self.check_game_end()
            os.system('cls' if os.name == 'nt' else 'clear') # Clears terminal output                
        print("Game end")
        
    
    def declare_winner(self):
        winner = self.player1 if self.player1.get_hits_taken() == 15 else self.player2
        print(f"Player {winner.get_id()} wins!")
        print("\nPlayer 1 board: ")
        