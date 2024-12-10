from __future__ import annotations
import random
import logging

from typing import Tuple

from tangled_game_engine import GameAgentBase

def get_builtin_agents():
    """
    Find all implementations of the GameAgentBase class in the tangled_agent module and return their names.
    """

    subclasses = GameAgentBase.__subclasses__()
    # print(f"subclasses: {subclasses}")
    result = [cls.__name__ for cls in subclasses]
    # print(f"result: {result}")
    return result

def create_agent(agent_class_name: str, agent_id: str) -> GameAgentBase:
    """
    Create an agent by name.
    """
    subclasses = GameAgentBase.__subclasses__()
    for cls in subclasses:
        if cls.__name__ == agent_class_name:
            return cls(agent_id)
    raise ValueError(f"Agent {agent_class_name} not found")
