import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np
import matplotlib.pyplot as plt
from src.models.diamond_lattice import DiamondLatticeSystem

# Create the images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# System parameters
n_cells = 33
t1 = 0.2
t2 = 0.4
t3 = 0.6
t4 = 0.8

# Create the system
system = DiamondLatticeSystem(
    n_cells=n_cells,
    t1=t1,
    t2=t2,
    t3=t3,
    t4=t4,
    gamma1=0.0,  # No gain
    gamma2=0.0   # No loss
)

# Get the Hamiltonian with real onsite energy = 1 (no nonlinear effects)
H = system.get_hamiltonian(phi=None, onsite=1.0)

# Calculate eigenvalues
evals = np.linalg.eigvalsh(H)

# Create k-space array for plotting
k = np.linspace(-np.pi, np.pi, 3 * n_cells + 1)

# Plot the results
plt.figure(figsize=(8, 6))
plt.scatter(1.5 * k + 0.5 * np.pi, evals, c='red', marker='.')
plt.scatter(-(1.5 * k + 0.5 * np.pi), evals, c='blue', marker='.')
plt.scatter(1.5 * k - 0.5 * np.pi, evals, c='red', marker='.')
plt.scatter(-(1.5 * k - 0.5 * np.pi), evals, c='blue', marker='.')
plt.title('Diamond Model Eigenenergies')
plt.xlabel('k-space')
plt.xlim(-np.pi, np.pi)
plt.ylabel('H Eigenvalues')
plt.grid(True, alpha=0.3)

# Save the plot
filename = f"images/diamond_eigenenergies_N={3 * n_cells + 1}_t1={t1}_t2={t2}_t3={t3}_t4={t4}.png"
plt.savefig(filename, dpi=300)
plt.close()

print(f"Plot saved to {filename}")
