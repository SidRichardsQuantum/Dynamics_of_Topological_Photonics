import os
from topological_photonics.dynamics.nrssh_gain_loss import plot_example_final_state

OUTPUT_DIR = os.environ.get("TOPOPHOTONICS_OUTPUT_DIR", "outputs")

plot_example_final_state(v=0.3, u=0.5, r=0.7, gamma1=0.9, gamma2=0.15, S=1.0, 
                         max_time=175, verbose=True, output_dir=OUTPUT_DIR)
