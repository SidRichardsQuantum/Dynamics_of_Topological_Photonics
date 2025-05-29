import numpy as np
import matplotlib.pyplot as plt
from src.models.diamond import Hamiltonain


n_cells = 33
N = 3 * n_cells + 1
x = np.linspace(1, N, N)  #Mimics real-space (picture the sites in a straight line)

evals, evecs = np.linalg.eigh(Hamiltonain(0.1, 0.2, 0.7, 0.9, 1, n_cells))
y = n_cells  #Look at 2*N//3 and N//2 too!

plt.plot(x, abs(evecs[:, y]) ** 2, c='red')  #See what happens if N is odd vs even
plt.xlabel('Site-index')
plt.ylabel('Intensity')
plt.title('Diamond Hamiltonian Eigenvectors')
plt.xlim(1, N)
plt.show()
