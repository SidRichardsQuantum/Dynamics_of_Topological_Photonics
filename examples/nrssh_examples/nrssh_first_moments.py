import os
from topological_photonics.dynamics.nrssh_time_evolution import plot_example_evolution

OUTPUT_DIR = os.environ.get("TOPOPHOTONICS_OUTPUT_DIR", "outputs")

plot_example_evolution(output_dir=OUTPUT_DIR)  # Run default example
