from __future__ import annotations

import configargparse

def setup_args() -> configargparse.ArgParser:
    """
    Set up handling of command-line arguments.
    """

    description = """
Play a game of Tangled with one or two custom agents, either for local testing
 or for online play."""
    
    epilog = """
Run this program with the --help flag to see the full list of options.
"""

    usage = """
Local game: 
    python -m tangled-agent --agent your_agent.YourAgentClass
Remote game: 
    python -m tangled-agent --game-id <game-id> --agent your_agent.YourAgentClass [--player-index 1] [--new-credentials]

Or you can use a configuration file (e.g. config.ini) with the following format:

```config.ini
[DEFAULT]
agent = your_agent.YourAgentClass
agent_2 = your_agent.OtherAgentClass
vertex_count = 5
game-id = <game-id>
host = <game-host>
new-credentials = False
```

or a combination of both:

    python -m tangled_agent --config config.ini --game_id <game-id> --host <game-host> --new-credentials

If a game-id is provided, the script will connect to the remote game server and join the game as either player 1 or 2 using the specified GameAgent subclass.
"""

    parser = configargparse.ArgParser(description=description,
                                        epilog=epilog,
                                        usage=usage,
                                        default_config_files=['config.ini'])

    

    parser.add('--config', is_config_file=True, help='Path to the configuration file.')
    parser.add_argument('--game-id', type=str, default=None, help='The ID of the game to connect to for a remote game.')
    parser.add_argument('--host', type=str, default='https://game-service-fastapi-blue-pond-7261.fly.dev', help='The host URL for the remote game server.')
    parser.add_argument('--new-credentials', action='store_true', help='Force new credentials.')
    parser.add_argument('--agent', type=str, default="tangled_agent.RandomRandyAgent", help='The qualified name of the game agent class (module.ClassName) to use.')
    parser.add_argument('--agent-2', type=str, default=None, help='The qualified name of the game agent class (module.ClassName) to use for player 2.')
    parser.add_argument('--agent-name', type=str, default="default", help='The name of the player agent to use for record keeping (online games).')
    parser.add_argument('--player-index', type=int, default=0, help='The index of the player to be in the game (0=no preference, 1 or 2).')
    parser.add_argument('--graph-id', type=str, default="k_3", help='The graph ID to use for the game.')
    valid_log_levels = ['PRETTY', 'GRAPH', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    parser.add_argument('--log-level', type=str, default='PRETTY', choices=valid_log_levels, help=f'The logging level to use ({", ".join(valid_log_levels)}).')
    parser.add_argument('--sample', action='store_true', help='Generate a sample agent.')
    return parser


parser = setup_args()
args, remaining_args = parser.parse_known_args()

hooks: list[callable[None, [configargparse.ArgParser]]] = []

def add_custom_args(hook: callable[None, [configargparse.ArgParser]]) -> None:
    """
    Add a hook to add custom arguments to the argument parser.
    
    Args:
        hook (callable): A function that accepts an ArgumentParser instance. This should add any arguments needed by the agent.
    """
    hooks.append(hook)
    
def parse_custom_args() -> None:
    """
    Run all hooks to add custom arguments to the argument parser.
    
    Args:
        parser (ArgumentParser): The argument parser to add arguments to.
    """
    global parser, args, remaining_args
    
    for hook in hooks:
        hook(parser)
    args = parser.parse_args(remaining_args, args)
