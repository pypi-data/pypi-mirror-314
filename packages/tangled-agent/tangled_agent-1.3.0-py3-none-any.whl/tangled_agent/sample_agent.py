from __future__ import annotations
import random
import logging

from typing import Tuple

from tangled_game_engine import Game

# Import the GameAgentBase class from tangled_agent
from tangled_agent import GameAgentBase

# Import the args object if you need to access command line arguments (defaults or custom)
from tangled_agent import args

class SampleAgent(GameAgentBase):
    """
    This is an example of a simple SampleAgent that makes random moves.

    Use this template to build your own agents. Here are the basic steps:

    1. Import the GameAgentBase class from tangled_game_engine.tangled_game_agent.base_agent.
        This will be the base class for your agent.
    2. Import the Game class from tangled_game_engine.tangled_game.
        This will be the state of the game that your agent will interact with. See the class for more details,
        but generally you'll have access to the full state of the game (the vertices and edges and their states)
        and some helpful methods for interacting with the game (get_legal_moves, etc.)
    3. Create a new class that inherits from GameAgentBase and implement the make_move method.
        The make_move method should take a Game object as an argument and return a tuple of the move type,
        move index, and move state.
        move_type is Game.MoveType IntEnum, and has values of VERTEX, EDGE, or QUIT.
        move_index is the index of the vertex or edge to change the state of.
        move_state is the state to change the vertex or edge.
            for VERTEX: 
                Vertex.State.P1
                Vertex.State.P2
                (Vertex.State.NONE is the initial state)
            for EDGE: 
                Edge.State.NEITHER
                Edge.State.FM
                Edge.State.AFM
                (Edge.State.NONE is the initial state)

        The move should be returned as a tuple of these three values as integers.
        e.g. (Game.MoveType.VERTEX.value, 3, Vertex.State.P1.value)
    """

    def __init__(self, player_id: str = None, **kwargs):
        """
        Do custom initialization of your game agent. Do not use command line arguments here.
        """
        
        super().__init__(player_id)
        
        
    @staticmethod
    def add_cli_options(parser):
        """
        Hook for agents to add their CLI options. Override for subclasses that need custom cli options.
        
        Example:        
            parser.add_argument('--my_custom_option', type=int, default=0, help='My custom option')
            
        Args:
            parser (configargparse.ArgParser): The argument parser instance to add options to.
        """
        pass

    def on_game_start(self, game: Game, **kwargs):
        """
        Called when a game starts. This is a good place to do any setup that is needed for the agent.
        This method can be overridden by a subclass if needed. Use any custom options set in add_cli_options here.
        
        Example:
            self.my_custom_option = args.my_custom_option
            
        Args:
            game (Game): The game object that has started.
            **kwargs: Any additional arguments that are passed to the agent.
        """
        pass

    def make_move(self, game: Game) -> Tuple[int, int, int]:
        """Make a move in the game.
        game: Game: The game instance

        Returns a tuple of the move type, move index, and move state.
        """

        legal_moves = game.get_legal_moves(self.id)

        if not legal_moves or (len(legal_moves) == 1 and legal_moves[0][0] == Game.MoveType.QUIT.value):
            logging.info("No legal moves available")
            return None

        while True:
            move = random.choice(legal_moves)
            if move[0] != Game.MoveType.QUIT.value:
                break

        return move


