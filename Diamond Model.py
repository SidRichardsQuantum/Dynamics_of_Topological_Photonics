import matplotlib.pyplot as plt
import numpy as np


N = 100  #Number of sites
k = np.linspace(-np.pi, np.pi, N)  #Momentum("k")-space points


def Hamiltonain(v, u, r, s, onsite):
    H = np.zeros((N, N), dtype=complex)
    for i in range(N):
        H[i, i] = onsite
    for i in range(0, N - 1, 3):
        H[i, i + 1] = u
        H[i + 1, i] = u
    for i in range(0, N - 2, 3):
        H[i, i + 2] = s
        H[i + 2, i] = s
    for i in range(2, N - 1, 3):
        H[i, i + 1] = r
        H[i + 1, i] = r
    for i in range(1, N - 2, 3):
        H[i, i + 2] = v
        H[i + 2, i] = v
    return(H)

evals = np.linalg.eigvalsh(Hamiltonain(0.2, 0.5, 0.9, 0.4, 1))

plt.scatter(k, evals, c='red', marker=('.'))
plt.scatter(-k, evals, c='red', marker=('.'))
plt.title('Diamond Model eigenenergies')
plt.xlabel('k-space')
plt.ylabel('H Eigenvalues')
plt.show()
