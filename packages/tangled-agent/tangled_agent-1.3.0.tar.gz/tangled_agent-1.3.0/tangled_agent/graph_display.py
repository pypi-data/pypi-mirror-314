import tkinter as tk
from tkinter import ttk
import math
from typing import Dict, List, Tuple, Any

class GraphGameGUI:
    def __init__(self, resolution: Tuple[int, int] = (800, 600)):
        """
        Initialize the GUI window with the given resolution.
        
        Args:
            resolution (Tuple[int, int]): Width and height of the window (default: 800x600)
        """
        self.window = tk.Tk()
        self.window.title("Graph Game Visualization")
        
        # Set window size
        self.width, self.height = resolution
        self.window.geometry(f"{self.width}x{self.height}")
        
        # Create canvas for graph drawing
        self.canvas = tk.Canvas(self.window, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status bar for game information
        self.status_frame = ttk.Frame(self.window)
        self.status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Labels for game status
        self.turn_label = ttk.Label(self.status_frame, text="Turn: 0")
        self.turn_label.pack(side=tk.LEFT, padx=5)
        
        self.player_label = ttk.Label(self.status_frame, text="Current Player: 1")
        self.player_label.pack(side=tk.LEFT, padx=5)
        
        # Edge state colors
        self.edge_colors = {
            0: 'gray',    # UNSET
            1: 'blue',    # FM
            2: 'red',     # NFM
            3: 'black'    # NP
        }
        
        # Node colors
        self.player_colors = {
            1: '#FFB6C1',  # Light pink for player 1
            2: '#ADD8E6'   # Light blue for player 2
        }
        
        # Bind resize event
        self.canvas.bind('<Configure>', self.on_resize)
        
        # Initialize game state as None
        self.game_state = None
        self.node_positions = {}
        
        # Flag to track if we've done initial setup
        self.is_initialized = False

        # Wait for the window to be ready
        self.window.update()
    
    def __del__(self):
        """Destructor to ensure the window is closed when the instance is destroyed."""
        if hasattr(self, 'window'):
            self.window.destroy()
    
    def on_resize(self, event):
        """Handle window resize by redrawing the graph."""
        if self.is_initialized and self.game_state is not None:
            self.node_positions = self.calculate_node_positions(self.game_state['num_nodes'])
            self.update(self.game_state)
    
    def calculate_node_positions(self, num_nodes: int) -> Dict[int, Tuple[int, int]]:
        """Calculate positions for nodes in a circular layout."""
        positions = {}
        
        # Get actual canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Calculate padding as a percentage of the smaller dimension
        padding = min(width, height) * 0.15
        
        # Calculate center and radius
        center_x = width / 2
        center_y = height / 2
        radius = min(width - padding*2, height - padding*2) / 2
        
        # Calculate positions with offset from center
        for i in range(num_nodes):
            angle = 2 * math.pi * i / num_nodes - math.pi / 2  # Start from top
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions[i] = (x, y)
        
        return positions
    
    def draw_node(self, canvas: tk.Canvas, x: int, y: int, node_id: int, 
                  player1_node: int, player2_node: int) -> None:
        """Draw a node with appropriate color based on player ownership."""
        # Calculate radius based on canvas size
        radius = min(self.canvas.winfo_width(), self.canvas.winfo_height()) * 0.04
        color = 'white'
        
        if node_id == player1_node:
            color = self.player_colors[1]
        elif node_id == player2_node:
            color = self.player_colors[2]
            
        # Create node circle
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                         fill=color, outline='black', width=2)
        
        # Add node ID text
        font_size = int(radius * 0.8)
        canvas.create_text(x, y, text=str(node_id), 
                         font=('Arial', font_size, 'bold'))
    
    def draw_edge(self, canvas: tk.Canvas, start_pos: Tuple[int, int], 
                  end_pos: Tuple[int, int], state: int) -> None:
        """Draw an edge with appropriate color based on its state."""
        color = self.edge_colors[state]
        # Calculate line width based on canvas size
        line_width = min(self.canvas.winfo_width(), self.canvas.winfo_height()) * 0.004
        canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1],
                         fill=color, width=max(1, int(line_width)))
    
    def draw_legend(self) -> None:
        """Draw a legend showing edge state colors."""
        legend_items = [
            ("UNSET", 0),
            ("FM", 1),
            ("NFM", 2),
            ("NP", 3)
        ]
        
        # Scale legend size based on canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        start_x = canvas_width * 0.02  # 2% from left
        start_y = canvas_height * 0.02  # 2% from top
        line_length = canvas_width * 0.04  # 4% of width
        spacing = canvas_height * 0.04  # 4% of height
        
        # Calculate text size based on canvas dimensions
        font_size = int(min(canvas_width, canvas_height) * 0.02)
        
        for i, (label, state) in enumerate(legend_items):
            y = start_y + i * spacing
            # Draw line sample
            self.canvas.create_line(start_x, y, start_x + line_length, y,
                                  fill=self.edge_colors[state], 
                                  width=max(1, int(canvas_width * 0.003)))
            # Draw label
            self.canvas.create_text(start_x + line_length + 10, y,
                                  text=label, anchor='w',
                                  font=('Arial', font_size))
    
    def update(self, game_state: Dict[str, Any]) -> None:
        """
        Update the display with new game state.
        This method should be called whenever the game state changes.
        
        Args:
            game_state (Dict[str, Any]): Current game state
        """
        self.game_state = game_state
        
        # Initialize node positions if this is the first update
        if not self.is_initialized:
            self.node_positions = self.calculate_node_positions(game_state['num_nodes'])
            self.is_initialized = True
        
        # Clear and redraw
        self.canvas.delete("all")
        
        # Update status labels
        self.turn_label.config(text=f"Turn: {game_state['turn_count']}/{len(game_state['edges'])+2}")
        self.player_label.config(text=f"Current Player: {game_state['current_player_index']}")
        
        # Draw edges first (so they appear behind nodes)
        for edge in game_state['edges']:
            start_node, end_node, state = edge
            start_pos = self.node_positions[start_node]
            end_pos = self.node_positions[end_node]
            self.draw_edge(self.canvas, start_pos, end_pos, state)
        
        # Draw nodes
        for node_id, pos in self.node_positions.items():
            self.draw_node(self.canvas, pos[0], pos[1], node_id,
                         game_state['player1_node'], game_state['player2_node'])
        
        # Add legend
        self.draw_legend()
        
        # Process any pending events
        self.window.update()
        
    def display_status(self, game_state: Dict[str, Any], delay: float = 0.5) -> None:
        """
        Update the display with new game state and enforce a minimum delay between updates.
        
        Args:
            game_state (Dict[str, Any]): Current game state
            delay (float): Minimum time in seconds that should elapse between display updates
        """
        import time
        current_time = time.time()
        
        # Initialize last_update_time if it doesn't exist
        if not hasattr(self, 'last_update_time'):
            self.last_update_time = current_time
        
        # Calculate time elapsed since last update
        elapsed = current_time - self.last_update_time
        
        # Update the display
        self.update(game_state)
        
        # If we haven't waited long enough, sleep for the remaining time
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        # Update the last update time to the current time plus any sleep
        self.last_update_time = time.time()