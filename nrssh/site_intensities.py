import numpy as np
import matplotlib.pyplot as plt
from nrssh.model import Hamiltonain


n_cells = 50
x = np.linspace(1, 2 * n_cells, 2 * n_cells)  #Mimics real-space (picture the sites in a straight line)
evals, evecs = np.linalg.eigh(Hamiltonain(0.1, 0.5, 0.9, 1, n_cells))
y = n_cells  #Remember that the localized edge-state eigenenergies were in the center of the bands? y is the index for this.

plt.plot(x, abs(evecs[:, y]) ** 2, c='red')  #See what happens if N is odd vs even!
plt.xlabel('Site-index')
plt.ylabel('Intensity')
plt.title('NRSSH Hamiltonian Eigenvectors')  #Eigenenergy plots
plt.xlim(1, 2 * n_cells)
plt.show()
