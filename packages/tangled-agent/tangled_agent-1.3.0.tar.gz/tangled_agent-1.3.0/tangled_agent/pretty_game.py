import os
import time
import shutil
from typing import Dict, Any, List, Tuple
from enum import IntEnum
from tangled_game_engine import Vertex, Edge, Game

class GameDisplay:
    def __init__(self):
        self.update_terminal_size()
        
    def update_terminal_size(self) -> None:
        """Update the terminal dimensions safely across platforms."""
        try:
            self.terminal_width, self.terminal_height = shutil.get_terminal_size()
        except Exception:
            self.terminal_width, self.terminal_height = 80, 24

    def clear_screen(self) -> None:
        """Clear the screen in a cross-platform way."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def count_edge_states(self, edges: List[Tuple[int, int, int]]) -> Dict[Edge.State, int]:
        """Count the number of edges in each state."""
        counts = {state: 0 for state in Edge.State}
        for _, _, state in edges:
            counts[Edge.State(state)] += 1
        return counts

    def create_box(self, text: str, padding: int = 1) -> str:
        """Create a box around text with specified padding."""
        lines = text.split('\n')
        max_length = max(len(line) for line in lines)
        
        horizontal = '-'
        vertical = '|'
        corner = '+'
        
        box = [corner + horizontal * (max_length + padding * 2) + corner]
        box.append(vertical + ' ' * (max_length + padding * 2) + vertical)
        
        for line in lines:
            padded_line = line.ljust(max_length)
            box.append(vertical + ' ' * padding + padded_line + ' ' * padding + vertical)
        
        box.append(vertical + ' ' * (max_length + padding * 2) + vertical)
        box.append(corner + horizontal * (max_length + padding * 2) + corner)
        
        return '\n'.join(box)

    def center_text(self, text: str) -> str:
        """Center text in the terminal."""
        lines = text.split('\n')
        centered_lines = []
        
        for line in lines:
            padding = (self.terminal_width - len(line)) // 2
            centered_lines.append(' ' * max(0, padding) + line)
            
        return '\n'.join(centered_lines)

    def display_status(self, game_state: Dict[str, Any]) -> None:
        """Display the game status in a formatted box."""
        self.update_terminal_size()
        self.clear_screen()
        
        # Count edges in each state
        edge_counts = self.count_edge_states(game_state['edges'])
        
        # Format player nodes for display
        p1_node = str(game_state['player1_node']) if game_state['player1_node'] >= 0 else 'None'
        p2_node = str(game_state['player2_node']) if game_state['player2_node'] >= 0 else 'None'
        
        status_lines = [
            f"Graph Game Status - Turn {game_state['turn_count']}",
            f"{'=' * 40}",
            f"Current Player: Player {game_state['current_player_index']}",
            "",
            f"Graph ID: {game_state.get('graph_id', '')}",
            f"Total Vertices: {game_state['num_nodes']}",
            f"Total Edges: {len(game_state['edges'])}",
            "",
            "Player Information:",
            f"Player 1 ({game_state.get('player1_id', '-')}):",
            f"  Claimed Node: {p1_node}",
            f"Player 2 ({game_state.get('player2_id', '-')}):",
            f"  Claimed Node: {p2_node}",
            "",
            "Edge States:",
            f"  UNSET: {edge_counts[Edge.State.NONE]}",
            f"  FM:    {edge_counts[Edge.State.FM]}",
            f"  AFM:   {edge_counts[Edge.State.AFM]}",
            f"  NP:    {edge_counts[Edge.State.NEITHER]}"
        ]
        
        status_box = self.create_box('\n'.join(status_lines))
        centered_box = self.center_text(status_box)
        print(centered_box)
        # Wait for a moment before returning
        time.sleep(0.1)

def main():
    """Example usage with sample game state."""
    display = GameDisplay()
    
    # Sample game state
    game_state = {
        "num_nodes": 6,
        "edges": [
            (0, 1, Edge.State.NONE.value),  # UNSET
            (1, 2, Edge.State.FM.value),  # FM
            (2, 3, Edge.State.AFM.value),  # AFM
            (3, 4, Edge.State.NEITHER.value),  # NP
            (4, 5, Edge.State.NONE.value),  # UNSET
        ],
        "graph_id": "test_graph_01",
        "player1_id": "Alice",
        "player2_id": "Bob",
        "turn_count": 3,
        "current_player_index": 1,
        "player1_node": 2,
        "player2_node": -1,
    }
    
    display.display_status(game_state)

if __name__ == "__main__":
    main()