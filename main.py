from game_engine import Engine


def main():
    game = Engine()
    game.run_placement_phase()    
    game.run_battle_phase()
    game.declare_winner()


if __name__ == "__main__":
    main()
    
    
# TODO: generate tests for ship placements
# TODO: generate tests for battle stage logistics
# TODO: Generalize engine class to support different ships, board dimension sizes