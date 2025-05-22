import numpy as np
import matplotlib.pyplot as plt


N = 100  #Number of sites
x = np.linspace(1, N, N)  #Mimics real-space (picture the sites in a straight line)


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
