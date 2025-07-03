import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.phases.diamond_phase_diagrams import plot_example_phase_diagram


if __name__ == "__main__":
    gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram()

    # gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram(
    #     t1=0.9, t2=0.7, t3=0.4, t4=0.1, S=1.0, points=20, verbose=True
    # )
