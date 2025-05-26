import numpy as np


def Hamiltonain(v, u, r, s, onsite, n_cells):
    N = 3 * n_cells + 1  #Number of sites. Has to be 1 mod 3 for the Diamond model
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


#Schrodinger eq: 1j * (d/dt)phi(t) = H(t)phi(t)
#Time-derivative: (d/dt)phi(t) = (phi(t+dt) - phi(t)) / dt
#Combine the above to write phi(t + dt) = U(t)phi(t), where U is of the 1st-order:
#U(t) = 1 - 1j * dt * H(t)
#This is NOT unitary even if H is Hermitian, because dt "isn't infinitesimal".
#So after some illegal maths, we define the 2nd-order time-evolution operator:
def U(h, n_cells, dt):
    U = np.dot((np.identity(3 * n_cells + 1) - 1j * dt * h / 2), np.linalg.inv(np.identity(3 * n_cells + 1) + 1j * dt * h / 2))
    return U


#Write the onsite-potentials as imaginary gain and loss terms
def H(h, phi, gamma1, gamma2, S, n_cells):
    for i in range(0, n_cells):
        h[i, i] = 1j * (gamma1 / (1 + S * np.abs(phi[i]) ** 2) - gamma2)
    return h
