import os
from time import sleep
from game_engine import Engine, Player, Placement

class UserInferface():            
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
        ship_name_width = 25
        ship_length_width = 15
        inventory_width = 15
        divider_width = 140
        print("\n" + "-" * divider_width)
        print(f"{'SHIP SYMBOL/NAME':<{ship_name_width}}{'SHIP LENGTH':<{ship_length_width}}{'LEFT TO PLACE':<{inventory_width}}")
        for ship_symbol, ship in curr_player.get_inventory().items():
            # Credit: spacing was improved with ChatGPT
            name, length, available = ship
            print(f"({ship_symbol}) {name:<{ship_name_width - 4}}{length} squares{'':<{ship_length_width - len(str(length)) - 8}}{available:<{inventory_width}}")
        print("\n" + "-" * divider_width + "\nCurrent placements: ")
        for row in curr_player.get_player_board():
            print(f"\t{row}")
        user_input = input("\n" + "-" * divider_width + f"\nPLAYER {curr_player.id} INPUT: ")
        return user_input
    
    def check_ship_name(self, user_ship: str):
        SHIP_SYMBOLS = {"A", "B", "C", "D", "S"}
        return user_ship in SHIP_SYMBOLS
    
    def check_orientation(self, user_orientation):
        ORIENTATIONS = {"V", "H"}
        return user_orientation in ORIENTATIONS

    def check_coord_format(self, user_coords: str):
        """"Ensures coordinate input can be converted to ASCII"""
        if len(user_coords) != 2 and len(user_coords) != 3:
            return False
        if not user_coords[0].isalpha() or not user_coords[1:].isnumeric(): 
            return False
        return True

    def check_input_format(self, user_input: str):
        """Runs all checks on input format, but not necessarily input legality"""
        args = user_input.split()
        if len(args) != 3:
            return False
        ship_name, orientation, user_coords = args
        return (self.check_ship_name(ship_name) and self.check_orientation(orientation) and self.check_coord_format(user_coords))

    def convert_coordinates(self, user_input):
        """Converts coordinate input to indices of a 2D array of shape (10, 10)"""
        internal_x = ord(user_input[0]) - ord('A')
        internal_y = int(user_input[1]) - 1 if len(user_input) == 2 else int(user_input[1:]) - 1
        return internal_x, internal_y
    
    def get_placement(self, user_input: str, engine: Engine):
        """Encapsulates all placement information in Placement object"""
        ship_name, orientation, user_coords = user_input.split()
        internal_x, internal_y = self.convert_coordinates(user_coords)
        ship_length = engine.get_player(1).get_ship_data(ship_name).get_length()
        return Placement(name=ship_name, x=internal_x, y=internal_y, length=ship_length, orientation=orientation)
    
    def prompt_attack(self, engine: Engine):
        curr_player = engine.get_player(1) if engine.is_player_turn(1) else engine.get_player(2)
        divider_width = 140
        print("-" * divider_width + "\nHits/Misses:")            
        for row in curr_player.get_hits_misses():
            print(f"\t{row}")
        return input("\n" + "-" * divider_width  + f"\nPLAYER {curr_player.get_id()}, input coordinates to attack: ")
            
    def run_placement_phase(self, engine: Engine):
        """Manages placement phase until all ships have been placed"""
        SHIPS_PER_PLAYER = 7
        ships_placed = 0
        while ships_placed < SHIPS_PER_PLAYER * 2:
            self.print_placement_instructions()
            curr_player = engine.get_player(1) if ships_placed < SHIPS_PER_PLAYER else engine.get_player(2)
            valid_placement = self.handle_ship_placement(curr_player, engine)
            if valid_placement:
                ships_placed += 1
            os.system('cls' if os.name == 'nt' else 'clear')  # Clears terminal output

    def handle_ship_placement(self, curr_player: Player, engine: Engine):
        """Handles the placement of a single ship for the current player"""
        user_input = self.prompt_ship_placement(curr_player)
        if self.check_input_format(user_input):
            placement = self.get_placement(user_input, engine)
            if engine.valid_placement(placement, curr_player):
                curr_player.place_ship(placement)
                return True
            else:
                print("Illegal placement. Please try again.")
                sleep(1.5)
                return False

    def run_battle_phase(self, engine: Engine):
        """Manages the battle phase until all of one player's ships are sunk"""
        while not engine.check_game_end():
            self.play_turn(engine)
            os.system('cls' if os.name == 'nt' else 'clear')  # Clears terminal output
            print(f"{engine.player1.hits_received}, {engine.player2.hits_received}")
        print("Game end")

    def play_turn(self, engine: Engine):
        """Plays a single turn for the current player"""
        curr_player, opponent = self.get_current_and_opponent_players(engine)
        attack_input = self.prompt_attack(engine)
        if self.is_valid_attack(attack_input, engine):
            x, y = self.convert_coordinates(attack_input)
            self.process_attack(curr_player, opponent, x, y, engine)
        else:
            print("Invalid attack input.")
            sleep(1.5)

    def get_current_and_opponent_players(self, engine: Engine):
        """Returns the current player and opponent"""
        curr_player = engine.get_player(1) if engine.is_player_turn(1) else engine.get_player(2)
        opponent = engine.get_player(1) if not engine.is_player_turn(1) else engine.get_player(2)
        return curr_player, opponent

    def is_valid_attack(self, attack_input: str, engine: Engine):
        """Checks if the attack input is valid in format and within bounds"""
        if not self.check_coord_format(attack_input):
            return False
        x, y = self.convert_coordinates(attack_input)
        return engine.check_coord_bounds(x, y)

    def process_attack(self, curr_player: Player, opponent: Player, x: int, y: int, engine: Engine):
        """Processes an attack and updates the game state"""
        hit = curr_player.attack(opponent, x, y)
        print("Hit!" if hit else "Miss!")
        engine.pass_turn()

    def declare_winner(self, engine: Engine):
        HITS_POSSIBLE = 18 # Sum of lengths of each ship in a player's inventory
        winner = engine.get_player(1) if engine.get_player(2).get_hits_received() == HITS_POSSIBLE else engine.get_player(2)
        print("Player 1 hits/misses")
        for row in engine.get_player(1).get_hits_misses():
            print(f"\t{row}")
        print("Player 2 hits/misses")
        for row in engine.get_player(2).get_hits_misses():
            print(f"\t{row}")
        print(f"Player {winner.get_id()} wins!")