import os
from topological_photonics.phases.diamond_phase_diagrams import plot_example_phase_diagram

OUTPUT_DIR = os.environ.get("TOPOPHOTONICS_OUTPUT_DIR", "outputs")

if __name__ == "__main__":
    # Run with default parameters
    gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram()

    # Run with custom parameters
    # gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram(
    #     t1=0.7, t2=0.3, t3=0.3, t4=0.7, S=1.0, points=30, max_time=63.9,
    #     verbose=True, output_dir=OUTPUT_DIR)
