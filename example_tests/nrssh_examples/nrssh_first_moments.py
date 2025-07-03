import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.dynamics.nrssh_time_evolution import plot_example_evolution


plot_example_evolution()  # Run default example
