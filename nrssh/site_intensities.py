import numpy as np
import matplotlib.pyplot as plt


N = 100  #Number of sites
x = np.linspace(1, N, N)  #Mimics real-space (picture the sites in a straight line)


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

evals, evecs = np.linalg.eigh(Hamiltonain(0.1, 0.5, 0.9, 1))
y = N // 2  #Remember that the localized edge-state eigenenergies were in the center of the bands? y is the index for this.

plt.plot(x, abs(evecs[:, y]) ** 2, c='red')  #See what happens if N is odd vs even!
plt.xlabel('Site-index')
plt.ylabel('Intensity')
plt.title('NRSSH Hamiltonian Eigenvectors')  #Eigenenergy plots
plt.xlim(1, N)
plt.show()
