import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.phases.nrssh_phase_diagrams import plot_example_phase_diagram


if __name__ == "__main__":
    gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram()

    # You can also run with custom parameters:
    # gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram(
    #     v=0.9, u=0.7, r=0.4, S=1.0, points=20, verbose=True
    # )
