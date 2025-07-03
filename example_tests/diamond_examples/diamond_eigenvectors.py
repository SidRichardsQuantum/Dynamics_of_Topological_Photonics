import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
    gamma1=0.0,  # No gain
    gamma2=0.0   # No loss
)

# Get the Hamiltonian with onsite energy = 1
H = system.get_hamiltonian(phi=None, onsite=1.0)

# Calculate eigenvalues and eigenvectors
evals, evecs = np.linalg.eigh(H)

# Create real-space array (mimics sites in a straight line)
x = np.linspace(1, 3 * n_cells + 1, 3 * n_cells + 1)

# Index for the localized edge-state
y = n_cells

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Plot the eigenvector intensity
plt.figure(figsize=(10, 6))
plt.plot(x, abs(evecs[:, y]) ** 2, c='red', linewidth=2)
plt.xlabel('Site-index')
plt.ylabel('Intensity')
plt.title('Diamond Hamiltonian Eigenvector')
plt.xlim(1, 3 * n_cells + 1)
plt.grid(True, alpha=0.3)

# Generate filename
filename = (f"images/diamond_eigenvector_N={3 * n_cells + 1}_"
            f"t1={system.t1}_t2={system.t2}_t3={system.t3}_t4={system.t4}.png")
plt.savefig(filename, dpi=300)
plt.close()

print(f"Plot saved to {filename}")

# Optional: Print system and eigenvector information
print(f"System parameters:")
print(f"  n_cells: {system.n_cells}")
print(f"  t1: {system.t1}")
print(f"  t2: {system.t2}")
print(f"  t3: {system.t3}")
print(f"  t4: {system.t4}")
print(f"  Total system size: {system.N} sites")
print(f"\nEigenvector analysis:")
print(f"  Plotting eigenvector index: {y}")
print(f"  Corresponding eigenvalue: {evals[y]:.6f}")
print(f"  Eigenvector norm: {np.linalg.norm(evecs[:, y]):.6f}")
print(f"  Maximum intensity: {np.max(abs(evecs[:, y]) ** 2):.6f}")
print(f"  Site with maximum intensity: {np.argmax(abs(evecs[:, y]) ** 2) + 1}")
