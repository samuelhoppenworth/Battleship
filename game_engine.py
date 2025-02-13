
# TODO: note stich from SHIP_LENGTHS dictionary to Ship class

# Define valid shipname, orientation, and coordinate inputs
SHIP_NAMES = set(["Aircraft Carrier", "Battleship", "Cruiser", "Destroyer", "Submarine"])
ORIENTATIONS = set(["V", "H"])
X_BOUNDS = [ord('A'), ord('J')]
Y_BOUNDS = [1, 10]
TOTAL_SHIPS = 14

# TODO: talk about decision to not include name
class ShipData:
    def __init__(self, length, num_available):
        self.length = length
        self.num_available = num_available
        
    def get_length(self):
        return self.length
    
    def get_available(self):
        return self.num_available
    


class Player:
    def __init__(self, id: 1):
        self.id = id
        self.hits_received = 0
        self.board = [[0] * 10] * 10
        self.ship_inventory = {
            "Aircraft Carrier" : ShipData(length=5, num_available=1),
            "Battleship" : ShipData(length=4, num_available=1),
            "Cruiser" : ShipData(length=3, num_available=1),
            "Destroyer" : ShipData(length=2, num_available=2),
            "Submarine" : ShipData(length=1, num_available=2)
        }
        
    def get_inventory(self):
        return self.ship_inventory

    def get_ship_data(self, ship_name):
        return self.ship_inventory[ship_name]

    def ship_available(self, ship_name: str):
        if ship_name not in self.ships:
            return False
        return (self.ship_inventory[ship_name].num_available > 0)
    
    def valid_ship_bounds(self, ship_data: ShipData, orientation: str, input_coords):
        x, y = input_coords
        if orientation == 'H':
            if x + ship_data.length > 10:
                return False
        else:
            if y + ship_data.length > 10:
                return False
        return True
    
    def valid_nonoverlap(self, placement_args):
        pass
    
    def valid_placement(self, placement_args):
        pass
    
    def place_ship(self, user_input): # TODO: Handle invalid ship placements
        
        pass

        
class Engine:
    def __init__(self):
        self.player1_turn = True
        self.ships_placed = 0
        self.player1 = Player(1)
        self.player2 = Player(2)
     
    def prompt_ship_placement(self, player: Player):
        print("""INSTRUCTIONS
              The orientation specifies whether the ship is placed vertically or horizontally, and the
              coordinate species the location of the top-left square of the ship. So if a ship is vertical, the coordinate
              specifies the ship's top-most square. If the ship is horizontal, the coordinate specifies the ship's left-most square.
              Example: \"Cruiser V A4\" indicates placing a Cruiser vertically such that its top most digit is on A4
              """)
        print(f"""ORIENTATIONS
              V (vertical)
              H (horizontal)
              """)
        print(f"""COORDINATES
              First coordinate: letters between A and J, inclusive
              Second coordinate: numbers between 1 and 10, inclusive
              """)

        ship_name_width = 20 
        ship_length_width = 20
        inventory_width = 10
        
        print(f"{'SHIP NAME':<{ship_name_width}}{'SHIP LENGTH':<{ship_length_width}}{'LEFT TO PLACE':<{inventory_width}}")
        inventory = player.get_inventory()
        for ship, ship_data in inventory.items():
            ship_length = ship_data.get_length()
            num_left = ship_data.get_available()
            print(f"{ship:<{ship_name_width}}({ship_length} squares)\t\t{num_left:<{inventory_width}}")

        user_input = input(f"\nPLAYER {player.id} INPUT:")
        return user_input
        
    def parse_placement_input(self, user_input: str):
        args = user_input.split()
        if len(args) != 3: #TODO: handle input errors
            return (None, None, None) # TODO: discuss this None choice
        
        ship_name, orientation, coords = args
        if ship_name not in SHIP_NAMES or orientation not in ORIENTATIONS or len(coords) != 2:
            return (None, None, None)
        
        x, y = coords
        if not (X_BOUNDS[0] <= ord(x) <= X_BOUNDS[1]) or not ((Y_BOUNDS[0] <= int(y) <= Y_BOUNDS[1])):
            return (None, None, None)
        x_idx, y_idx = ord(x) - ord('A'), int(y) - 1 # Convert game coords to matrix indices
        return (ship_name, orientation, [x_idx, y_idx])
        
    def run(self):
        
        # handle ship placements
        ships_placed = 0
        while ships_placed < TOTAL_SHIPS:
            input = self.prompt_ship_placement(self.player1)
            ship_name, orientation, coords = self.parse_placement_input(input) or (None, None, None)
            print(f"{ship_name} {orientation} {coords}")
        
        
        
    
    
engine = Engine()
engine.run()


