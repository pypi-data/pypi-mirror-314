"""
Main entry point for the Tangled agent game playing tools.
"""

from __future__ import annotations

import importlib
import os
import sys
import configargparse
from tangled_game_engine import Game
from .basic_game import play_local_game, play_remote_game
from .base_agent import GameAgentBase

from .config_handler import args, add_custom_args, parse_custom_args, parser

import logging
from .pretty_game import GameDisplay
from .graph_display import GraphGameGUI
from functools import partial

def import_agent(agent_name: str) -> GameAgentBase:
    """
    Dynamically import a class from a string specification in the format 'module_name.ClassName'.
    
    Args:
        agent_name (str): The module and class name as a single string.
    
    Returns:
        type: The class type that was dynamically imported.
    """
    try:
        # Split the input into module and class
        module_name, class_name = agent_name.rsplit('.', 1)
        logging.debug(f"Importing module {module_name} and class {class_name}")
        
        # Import the module
        module = importlib.import_module(module_name)

        # Get the class from the module
        clazz = getattr(module, class_name)
        if not issubclass(clazz, GameAgentBase):
            raise ValueError(f"Class '{class_name}' is not a subclass of GameAgentBase.")
        
        return clazz
    except (ImportError, AttributeError, ValueError) as e:
        raise ImportError(f"Could not import class {agent_name}. Ensure it exists and is correctly specified (e.g. module_name.ClassName).") from e
    

def generate_sample_agent(agent_name: str) -> str:
    """
    Generate a sample agent class with the given name.
    """
    from importlib import resources
    import tangled_agent
        
    # Validate that the agent name is a valid Python identifier in CamelCase
    if not agent_name.isidentifier() or not agent_name[0].isupper():
        raise ValueError("Agent name must be a valid Python identifier in CamelCase (e.g. MyAgent).")
    
    # Convert camel case agent_name to snake case for file
    file_name = agent_name[0].lower() + ''.join([f"_{c.lower()}" if c.isupper() else c for c in agent_name[1:]]) + ".py"

    # Check if local file_name already exists and ask to overwrite before doing so.
    if os.path.exists(file_name):
        overwrite = input(f"File {file_name} already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Exiting without overwriting file.")
            sys.exit(0)
    
    # Read the random agent template
    with resources.open_text(tangled_agent, "sample_agent.py") as infile:
        sample_text = infile.read()
        # Rename the RandomRandyAgent class to the given name
        sample_text = sample_text.replace("SampleAgent", agent_name)
        
        # Write the file
        with open(file_name, "w") as outfile:
            outfile.write(sample_text)        

def main():
    """
    Main entry point for the script.
    Get the command-line arguments and start the game.
    """
    if args.sample:
        print("Generating sample agent SampleAgent in file sample_agent.py")
        generate_sample_agent("SampleAgent")
        sys.exit(0)

    # Create an agent from the class from a string
    agent_class = import_agent(args.agent)

    # Create an agent from the class from a string
    agent_class2 = import_agent(args.agent_2) if args.agent_2 else None

    if not agent_class2:
        agent_class2 = agent_class

    # Add custom arguments to the parser for the agents
    agent_class.add_cli_options(parser)
    if agent_class2 != agent_class:
        agent_class2.add_cli_options(parser)
        
    # Parse the command line arguments
    parse_custom_args()

    game_display = None
    callback = None
    if args.log_level:
        if args.log_level == 'PRETTY':
            logging.basicConfig(level=logging.INFO)
            game_display = GameDisplay()
            callback = game_display.display_status
        elif args.log_level == 'GRAPH':
            logging.basicConfig(level=logging.INFO)
            game_display = GraphGameGUI()
            callback = partial(game_display.display_status, delay=0.1)
        else:
            logging.basicConfig(level=args.log_level)
            

    if args.game_id is not None:

        # Create the agent to play the game. The player ID should match one of the players in the game.
        player = agent_class()
        
        logging.info(f"Game ID: {args.game_id}")
        logging.info(f"Host: {args.host}")
        logging.info(f"Force New Credentials: {args.new_credentials}")
        logging.info(f"Player Index: {args.player_index}")
        logging.info(f"Agent Name: {args.agent_name}")
        
        play_remote_game(args.game_id, 
                         args.host, 
                         player, 
                         force_new_credentials=args.new_credentials, 
                         player_index=args.player_index, 
                         agent_name=args.agent_name, 
                         update_display=callback)
    else:
        # Create two agents with names (e.g. RandomRandyAgent("player1"))
            
        player1 = agent_class(f'{agent_class.__name__}')
        player2 = agent_class2(f'{agent_class2.__name__}') if agent_class2 else agent_class(f'{agent_class.__name__}')

        # Use a predefined graph if supplied
        graph_id = args.graph_id

        logging.info(f"Game graph: {graph_id}")
        game = Game()
        game.create_game(graph_id=graph_id)

        # Play a local game with the two agents
        play_local_game(player1, player2, game, update_display=callback)


if __name__ == "__main__":
    main()

