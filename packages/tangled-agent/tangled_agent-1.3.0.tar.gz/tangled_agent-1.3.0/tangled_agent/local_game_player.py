"""
LocalGamePlayer class for playing a game locally.

This class is used to play a game locally between two agents. Use this to test your 
agents against each other without incurring server costs.
"""

from __future__ import annotations

import time
from typing import Dict, Optional, Type, Any, Tuple, List
from tangled_game_engine import Game

from .base_game_player import GamePlayerBase
from .base_agent import GameAgentBase

class LocalGamePlayer(GamePlayerBase):
    """
    LocalGamePlayer class for playing a game locally between two agents.
    Instantiate it with references to the two agents and the game to play.
    Call play_game() to play the game until it is over. Calls will be made by
    play_game to the agents to select moves for their turn until the game is over.
    """

    player1: GameAgentBase
    player2: GameAgentBase
    game: Game
    update_display: Optional[callable]

    def __init__(self, player1: GameAgentBase, player2: GameAgentBase, game: Game, update_display: Optional[callable] = None):
        """
        Initializes the LocalGamePlayer with the two agents and the game to play.
        
        Args:
            player1 (GameAgentBase): The first player agent.
            player2 (GameAgentBase): The second player agent.
            game (Game): The game to play.
        """

        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.game.join_game(self.player1.id, 1)
        self.game.join_game(self.player2.id, 2)
        self.update_display = update_display

    def play_game(self) -> dict:
        """
        Play the game until it is over. Calls will be made by play_game to the agents
        to select moves for their turn until the game is over.

        Returns:
            dict: The final state of the game.
        """
        
        self.player1.on_game_start(self.game)
        self.player2.on_game_start(self.game)

        while not self.game.is_game_over():
            player = self.player1 if self.game.is_my_turn(player_id=self.player1.id) else self.player2
            move = player.make_move(self.game)
            if move:
                type, index, state = move
                if type == Game.MoveType.QUIT.value:
                    print(f"{player.id()} quit the game.")
                    break
                self.game.make_move(player.id, type, index, state)
                if self.update_display:
                    self.update_display(self.game.get_game_state())
            else:
                print("No moves available. Ending game.")
                break
                
        final_state = self.game.get_game_state()
        return final_state

__all__ = ["LocalGamePlayer"]
