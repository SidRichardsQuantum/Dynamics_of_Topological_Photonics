import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.phases.diamond_phase_diagrams import plot_example_phase_diagram


if __name__ == "__main__":
    # gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram()

    gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram(
        t1=0.7, t2=0.3, t3=0.3, t4=0.7, S=1.0, points=30, max_time=63.9, verbose=True)
