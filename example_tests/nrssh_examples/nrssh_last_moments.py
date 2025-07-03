import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.dynamics.nrssh_gain_loss import plot_example_final_state


plot_example_final_state()  # Run default example
