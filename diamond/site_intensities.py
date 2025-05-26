import numpy as np
import matplotlib.pyplot as plt


n_cells = 33  #Number of cells
N = 3 * n_cells + 1  #Number of sites. Has to be 1 mod 3 for the Diamond model
x = np.linspace(1, N, N)  #Mimics real-space (picture the sites in a straight line)

from Diamond Model.py import Hamiltonian
H = Hamiltonain(v, u, r, s, onsite)
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

evals, evecs = np.linalg.eigh(Hamiltonain(0.2, 0.5, 0.9, 0.4, 1))
y = N//3  #Look at 2*N//3 and N//2 too!

plt.plot(x, abs(evecs[:, y]) ** 2, c='red')  #See what happens if N is odd vs even
plt.xlabel('Site-index')
plt.ylabel('Intensity')
plt.title('H Eigenvectors')
plt.xlim(1, N)
plt.show()
