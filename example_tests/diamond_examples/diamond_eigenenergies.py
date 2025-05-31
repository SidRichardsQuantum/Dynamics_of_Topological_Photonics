import numpy as np
import matplotlib.pyplot as plt
from src.models.diamond_lattice import DiamondLatticeSystem


# Create the system with the same parameters
n_cells = 33
system = DiamondLatticeSystem(
    n_cells=n_cells,
    t1=0.2,
    t2=0.4,
    t3=0.6,
    t4=0.8,
    gamma1=0.0, # No gain (was handled by onsite=1 previously)
    gamma2=0.0  # No loss (was handled by onsite=1 previously)
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
plt.title('Diamond Model eigenenergies')
plt.xlabel('k-space')
plt.xlim(-np.pi, np.pi)
plt.ylabel('H Eigenvalues')
plt.grid(True, alpha=0.3)
plt.show()
