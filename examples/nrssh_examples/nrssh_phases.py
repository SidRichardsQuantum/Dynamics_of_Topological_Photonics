import os
from topological_photonics.phases.nrssh_phase_diagrams import plot_example_phase_diagram

OUTPUT_DIR = os.environ.get("TOPOPHOTONICS_OUTPUT_DIR", "outputs")

if __name__ == "__main__":
    gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram(output_dir=OUTPUT_DIR)

    # You can also run with custom parameters:
    # gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram(
    #     v=0.3, u=0.5, r=0.7, S=1.0, points=30, max_time=175, verbose=True)
