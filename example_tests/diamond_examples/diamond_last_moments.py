import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.dynamics.diamond_gain_loss import plot_example_final_state


plot_example_final_state(t1=0.5, t2=0.5, t3=0.9, t4=0.9, gamma1=0.9, gamma2=0.15, S=1.0, 
                         max_time=75, verbose=True)
