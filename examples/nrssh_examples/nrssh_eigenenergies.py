import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np
import matplotlib.pyplot as plt
from src.models.nrssh_lattice import NRSSHLatticeSystem
from src.plotting import output_file

OUTPUT_DIR = os.environ.get("TOPOPHOTONICS_OUTPUT_DIR", "outputs")

# Create the system with the same parameters
n_cells = 50
v = 0.2
u = 0.5
r = 0.9
onsite = 1.0

system = NRSSHLatticeSystem(
    n_cells=n_cells,
    v=v,
    u=u,
    r=r,
    onsite=onsite,
    gamma1=0.0,  # No gain
    gamma2=0.0   # No loss
)

# Get the Hamiltonian with real onsite energy = 1 (no nonlinear effects)
H = system.get_hamiltonian(phi=None, onsite=onsite)

# Calculate eigenvalues
evals = np.linalg.eigvalsh(H)

# Create k-space array for plotting
k = np.linspace(-np.pi, np.pi, 2 * n_cells)

# Generated plots go under outputs/ so tracked documentation figures stay stable.

# Plot the results
plt.figure(figsize=(8, 6))
plt.scatter(k, evals, c='red', marker='.')
plt.scatter(-k, evals, c='blue', marker='.')  # Flip the k-values to simulate the true band-structure
plt.title(f'NRSSH Model Eigenenergies\n'
          f'v={v}, u={u}, r={r}, onsite={onsite}', fontsize=11)
plt.xlabel('k-space')
plt.ylabel('H Eigenvalues')
plt.grid(True, alpha=0.3)

# Generate filename
filename = output_file(OUTPUT_DIR, "eigensolutions", f"nrssh_eigenenergies_N={2 * n_cells}_v={v}_u={u}_r={r}.png")
plt.savefig(filename, dpi=300)
plt.close()

print(f"Plot saved to {filename}")
