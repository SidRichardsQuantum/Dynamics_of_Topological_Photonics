import numpy as np
import matplotlib.pyplot as plt
from src.models.diamond import Hamiltonain


#n_cells is the number of unit cells in the lattice chain
n_cells = 33
evals = np.linalg.eigvalsh(Hamiltonain(0.2, 0.5, 0.9, 0.4, 1, n_cells))
k = np.linspace(-np.pi, np.pi, 3 * n_cells + 1)  #Momentum("k")-space points

plt.scatter(k, evals, c='red', marker=('.'))
plt.scatter(-k, evals, c='red', marker=('.'))
plt.title('Diamond Model Eigenenergies')
plt.xlabel('k-space')
plt.ylabel('Eigenvalues')
plt.show()
