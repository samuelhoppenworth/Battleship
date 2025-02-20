from game_engine import Engine
from user_interface import UserInferface

def main():
    engine = Engine()
    ui = UserInferface()
    ui.print_placement_instructions()
    ui.run_placement_phase(engine)
    ui.run_battle_phase(engine)
    ui.declare_winner(engine)
    

if __name__ == "__main__":
    main()
    
    
# TODO: generate tests for ship placements
# TODO: generate tests for battle stage logistics
# TODO: Generalize engine class to support different ships, board dimension sizes