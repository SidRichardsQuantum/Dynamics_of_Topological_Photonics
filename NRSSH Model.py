import matplotlib.pyplot as plt
import numpy as np


N = 250  #Number of sites
k = np.linspace(-np.pi, np.pi, N)  #Momentum("k")-space points

#For non-reciprocal intra-cell hopping strengths r and u,
#and reciprocal intrer-cell hoppings s:
def Hamiltonain(r, u, s, onsite):
    H = np.zeros((N, N), dtype=complex)
    for i in range(N):
        H[i, i] = onsite
    for i in range(0, N - 1, 2):
        H[i, i + 1] = r
        H[i + 1, i] = u
    for i in range(1, N - 1, 2):
        H[i, i + 1] = s
        H[i + 1, i] = s
    return(H)

evals = np.linalg.eigvalsh(Hamiltonain(0.2, 0.5, 0.9, 1))

plt.scatter(k, evals, c='red', marker=('.'))
plt.scatter(-k, evals, c='red', marker=('.'))
plt.title('NRSSH Model eigenenergies')
plt.xlabel('k-space')
plt.ylabel('H Eigenvalues')
plt.show()
