"""
Base class for game agents.
Create a subclass of this class to implement a game agent.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple
from tangled_game_engine import Game

from .config_handler import parser, remaining_args

class GameAgentBase(ABC):
    """
    Base class for game agents.
    Create a subclass of this class to implement a game agent.
    """

    __player_id: str

    def __init__(self, player_id: str = None):
        """
        Initializes the game agent with the player id.
        This id must either match an id of the player in a game, or the game must allow all players.
        
        Args:
            player_id (str): The player id for this agent.
        """

        if not player_id:
            # Get the name of the subclass for this class as the player id
            player_id  = self.__class__.__name__
        self.__player_id = player_id
                
        

    @staticmethod
    def add_cli_options(parser):
        """
        Hook for agents to add their CLI options. Override for subclasses that need custom cli options.
        Args:
            parser (ArgumentParser): The argument parser instance to add options to.
        """
        pass

    
    def on_game_start(self, game: Game, **kwargs):
        """
        Called when a game starts. This is a good place to do any setup that is needed for the agent.
        This method can be overridden by a subclass if needed.
        
        Args:
            game (Game): The game object that has started.
            **kwargs: Any additional arguments that are passed to the agent.
        """
        pass
    
    @property
    def id(self) -> str:
        return self.__player_id

    @id.setter
    def id(self, player_id: str):
        self.__player_id = player_id

    @abstractmethod
    def make_move(self, game: Game) -> Tuple[int, int, int]:
        """
        Have the agent make a move in the game. This method should be implemented by a subclass.
        This will be called each time it is the agent's turn to make a move.
        The move must be a valid move for the game and the agent.

        Args:
            game (Game): The game object to make a move in. Use this to get valid moves and the current state of the game.

        Returns:
            Tuple[int, int, int]: A tuple of the move type (see Game.MoveType), move index (vertex or edge), and move state (see Vertex.State and Edge.State).
        """
        pass


__all__ = ["GameAgentBase"]