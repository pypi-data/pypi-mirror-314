import psutil
from collections import deque
from datetime import datetime
from typing import List, Tuple

class ResourceHistory:
    def __init__(self, max_points=60):
        self.max_points = max(1, max_points)  # Ensure at least 1 point
        self.cpu_history = deque(maxlen=max_points)
        self.memory_history = deque(maxlen=max_points)
        self.timestamps = deque(maxlen=max_points)
        # Initialize CPU monitoring
        try:
            psutil.cpu_percent(interval=None)
            # Add initial values to prevent empty graphs
            self.cpu_history.append(0)
            self.memory_history.append(0)
            self.timestamps.append(datetime.now())
        except Exception:
            pass
        
    def update(self):
        """Update resource history with current values"""
        try:
            # Get CPU percentage with minimal interval for real-time updates
            cpu = psutil.cpu_percent(interval=0.05)  # Reduced interval for more frequent updates
            memory = psutil.virtual_memory().percent
            timestamp = datetime.now()
            
            # Handle None values and ensure valid ranges
            if cpu is not None and memory is not None:
                # Enhanced smoothing with weighted moving average to reduce spikes
                if len(self.cpu_history) > 0:
                    last_cpu = self.cpu_history[-1]
                    # Weight recent readings more heavily (80% new, 20% old)
                    # This provides more responsive updates while still smoothing spikes
                    cpu = (0.8 * cpu + 0.2 * last_cpu)
                
                # Ensure values are within valid range with float precision
                cpu = round(max(0.0, min(100.0, cpu)), 1)  # Round to 1 decimal place
                memory = round(max(0.0, min(100.0, memory)), 1)
                
                # Update histories with validated values
                self.cpu_history.append(cpu)
                self.memory_history.append(memory)
                self.timestamps.append(timestamp)
                
                # Ensure we don't exceed max points
                while len(self.cpu_history) > self.max_points:
                    self.cpu_history.popleft()
                    self.memory_history.popleft()
                    self.timestamps.popleft()
                
                return True
            return False
        except KeyboardInterrupt:
            # Gracefully handle keyboard interrupts
            return False
        except psutil.Error as e:
            # Handle psutil-specific errors
            print(f"System resource error: {str(e)}")
            return False
        except Exception as e:
            print(f"Resource monitoring error: {str(e)}")
            # Return last known good values if available
            if len(self.cpu_history) > 0 and len(self.memory_history) > 0:
                self.cpu_history.append(self.cpu_history[-1])
                self.memory_history.append(self.memory_history[-1])
                self.timestamps.append(timestamp)
                return True
            return False

    def get_cpu_graph(self, width: int, height: int) -> List[str]:
        """Generate ASCII graph for CPU usage"""
        return self._generate_graph(list(self.cpu_history), width, height, "CPU Usage %")

    def get_memory_graph(self, width: int, height: int) -> List[str]:
        """Generate ASCII graph for memory usage"""
        return self._generate_graph(list(self.memory_history), width, height, "Memory Usage %")

    def _generate_graph(self, data: List[float], width: int, height: int, title: str) -> List[str]:
        """Generate ASCII graph from data points with enhanced visualization"""
        # Ensure positive dimensions with minimums
        width = max(40, width)  # Increased minimum width for better visibility
        height = max(6, height)  # Minimum height for title, axis, and current value
        
        # Handle empty data case with informative message
        if not data:
            empty_graph = [" " * width for _ in range(height)]
            empty_graph[0] = f"{title} (Waiting for data...)".center(width)
            return empty_graph

        try:
            # Calculate graph dimensions with proper spacing
            graph_height = max(3, height - 3)  # Reserve space for title, current value, and labels
            graph_width = max(30, width - 12)  # Reserve more space for y-axis labels
            
            # Dynamic scaling based on actual data range
            actual_max = max(data)
            actual_min = min(data)
            current_value = data[-1] if data else 0
            
            # Use fixed ranges for percentage values
            max_value = 100
            min_value = 0
            value_range = max_value - min_value
            scale = (graph_height - 1) / value_range if value_range > 0 else 1
            
            # Ensure data points are within range with proper rounding
            data = [round(max(min_value, min(max_value, d)), 1) for d in data]

            # Generate graph lines
            lines = []
            
            # Add title with current value
            title_with_value = f"{title} (Current: {current_value:.1f}%)"
            lines.append(f"{title_with_value:^{width}}")

            # Generate graph body with improved scale marks
            for y in range(graph_height):
                # Calculate value for this line with proper spacing
                value = max_value - (y * (value_range / (graph_height - 1)))
                line = f"{value:4.0f}%│"
                
                for x in range(min(len(data), graph_width)):
                    try:
                        data_idx = -(graph_width - x)  # Start from most recent data
                        if abs(data_idx) <= len(data):
                            data_value = data[data_idx]
                            height_at_x = (data_value - min_value) * scale
                            
                            if graph_height - y <= height_at_x:
                                # Enhanced visualization using varied characters
                                if data_value >= 90:
                                    line += "█"  # Critical level
                                elif data_value >= 75:
                                    line += "▓"  # High level
                                elif data_value >= 50:
                                    line += "▒"  # Medium level
                                elif data_value >= 25:
                                    line += "░"  # Low level
                                else:
                                    line += "·"  # Very low level
                            else:
                                line += " "
                        else:
                            line += " "
                    except IndexError:
                        line += " "
                
                lines.append(line)

            # Add x-axis with time indicators
            x_axis = "    └" + "─" * (graph_width - 2) + "┘"
            time_label = "Time →"
            x_axis = x_axis[:-len(time_label)] + time_label
            lines.append(x_axis)

            return lines
            
        except Exception as e:
            # Fallback to empty graph on error
            empty_graph = [" " * width for _ in range(height)]
            empty_graph[0] = f"{title} (Error: {str(e)})".center(width)
            return empty_graph
            
        except Exception:
            # Fallback to empty graph on error
            empty_graph = [" " * width for _ in range(height)]
            empty_graph[0] = f"{title} (Error)".center(width)
            return empty_graph
