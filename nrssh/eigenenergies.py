import numpy as np
import matplotlib.pyplot as plt
from nrssh.model import Hamiltonain


n_cells = 50
k = np.linspace(-np.pi, np.pi, 2 * n_cells)
evals = np.linalg.eigvalsh(Hamiltonain(0.2, 0.5, 0.9, 1, n_cells))

plt.scatter(k, evals, c='red', marker=('.'))
plt.scatter(-k, evals, c='red', marker=('.'))
plt.title('NRSSH Model eigenenergies')
plt.xlabel('k-space')
plt.ylabel('H Eigenvalues')
plt.show()
