import os
from time import sleep
from game_engine import Engine, Player

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
            name, length, available = ship
            print(f"({ship_symbol}) {name:<{ship_name_width - 4}}{length} squares{'':<{ship_length_width - len(str(length)) - 8}}{available:<{inventory_width}}")
            # Credit: formatting of above output function was improved with ChatGPT

        print("\n" + "-" * divider_width + "\nCurrent placements: ")
        for row in curr_player.get_player_board():
            print(f"\t{row}")

        user_input = input("\n" + "-" * divider_width + f"\nPLAYER {curr_player.id} INPUT: ")
        return user_input
            
    
    def prompt_attack(self, engine: Engine):
        curr_player = engine.get_player(1) if engine.is_player_turn(1) else engine.get_player(2)
        divider_width = 140
        print("-" * divider_width + "\nHits/Misses:")            
        for row in curr_player.get_opponent_board():
            print(f"\t{row}")

        return input("\n" + "-" * divider_width  + f"\nPLAYER {curr_player.get_id()}, input coordinates to attack: ")
    
    
    def run_placement_phase(self, engine: Engine):
        SHIPS_PER_PLAYER = 7
        ships_placed = 0
        while ships_placed < SHIPS_PER_PLAYER * 2:            
            self.print_placement_instructions()
            curr_player = engine.get_player(1) if ships_placed < SHIPS_PER_PLAYER else engine.get_player(2)
            user_input = self.prompt_ship_placement(curr_player)
            if engine.check_input_format(user_input):
                placement = engine.get_placement(user_input)
                is_valid = engine.valid_placement(placement, curr_player)
                if is_valid:                    
                    curr_player.place_ship(placement)
                    ships_placed += 1
                else:
                    print("Illegal placement. Please try again.")
                    sleep(1.5)
            os.system('cls' if os.name == 'nt' else 'clear') # Clears terminal output                
            
    
    def run_battle_phase(self, engine: Engine):
        game_end = 0
        while not game_end:
            curr_player = engine.get_player(1) if engine.is_player_turn(1) else engine.get_player(2)
            opponent = engine.get_player(1) if not engine.is_player_turn(1) else engine.get_player(2)
            
            attack_input = self.prompt_attack(engine)
            if engine.check_coord_format(attack_input):                
                x, y = engine.convert_coordinates(attack_input)
                if engine.check_coord_bounds(x, y): 
                    curr_player.attack(opponent, x, y) # nothing stops player from guessing same square more than once
                    engine.pass_turn()
                else:
                    print("Coordinates not in bounds")
                    sleep(1.5)
            else:
                print("Coordinates improperly formatted")
                sleep(1.5)
            game_end = engine.check_game_end()
            os.system('cls' if os.name == 'nt' else 'clear') # Clears terminal output                
        print("Game end")
        
    
    def declare_winner(self, engine: Engine):
        winner = engine.get_player(1) if engine.get_player(1).get_hits_taken() == 15 else engine.get_player(2)
        print(f"Player {winner.get_id()} wins!")
        print("\nPlayer 1 board: ")
        


