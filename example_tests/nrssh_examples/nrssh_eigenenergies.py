import numpy as np
import matplotlib.pyplot as plt
from src.models.nrssh_lattice import NRSSHLatticeSystem


# Create the system with the same parameters
n_cells = 50
system = NRSSHLatticeSystem(
    n_cells=n_cells,
    v=0.2,
    u=0.5,
    r=0.9,
    gamma1=0.0, # No gain
    gamma2=0.0  # No loss
)

# Get the Hamiltonian with real onsite energy = 1 (no nonlinear effects)
H = system.get_hamiltonian(phi=None, onsite=1.0)

# Calculate eigenvalues
evals = np.linalg.eigvalsh(H)

# Create k-space array for plotting
k = np.linspace(-np.pi, np.pi, 2 * n_cells)

# Plot the results
plt.figure(figsize=(8, 6))
plt.scatter(k, evals, c='red', marker='.')
plt.scatter(-k, evals, c='blue', marker='.')  # Flip the k-values to simulate the true band-structure
plt.title('NRSSH Model eigenenergies')
plt.xlabel('k-space')
plt.ylabel('H Eigenvalues')
plt.grid(True, alpha=0.3)
plt.show()
