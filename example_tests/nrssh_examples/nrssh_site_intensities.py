import numpy as np
import matplotlib.pyplot as plt
from src.models.nrssh_lattice import HamiltonianSystem

# Create the system with the same parameters
n_cells = 50
system = HamiltonianSystem(
    n_cells=n_cells,
    v=0.1,      # Previously first argument
    u=0.5,      # Previously second argument
    r=0.9,      # Previously third argument
    gamma1=0.0, # No gain
    gamma2=0.0  # No loss
)

# Get the Hamiltonian with onsite energy = 1
H = system.get_hamiltonian(phi=None, onsite=1.0)

# Calculate eigenvalues and eigenvectors
evals, evecs = np.linalg.eigh(H)

# Create real-space array (mimics sites in a straight line)
x = np.linspace(1, 2 * n_cells, 2 * n_cells)

# Index for the localized edge-state (center of the bands)
y = n_cells

# Plot the eigenvector intensity
plt.figure(figsize=(10, 6))
plt.plot(x, abs(evecs[:, y]) ** 2, c='red', linewidth=2)
plt.xlabel('Site-index')
plt.ylabel('Intensity')
plt.title('NRSSH Hamiltonian Eigenvectors')
plt.xlim(1, 2 * n_cells)
plt.grid(True, alpha=0.3)
plt.show()

# Optional: Print some information about the eigenvector
print(f"System parameters:")
print(f"  n_cells: {system.n_cells}")
print(f"  r (forward hopping): {system.r}")
print(f"  u (backward hopping): {system.u}")
print(f"  v (inter-cell hopping): {system.v}")
print(f"  Total system size: {system.N} sites")
print(f"\nEigenvector analysis:")
print(f"  Plotting eigenvector index: {y}")
print(f"  Corresponding eigenvalue: {evals[y]:.6f}")
print(f"  Eigenvector norm: {np.linalg.norm(evecs[:, y]):.6f}")
print(f"  Maximum intensity: {np.max(abs(evecs[:, y]) ** 2):.6f}")
print(f"  Site with maximum intensity: {np.argmax(abs(evecs[:, y]) ** 2) + 1}")
