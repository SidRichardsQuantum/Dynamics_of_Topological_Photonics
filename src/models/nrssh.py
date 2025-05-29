import numpy as np


#For non-reciprocal intra-cell hopping strengths r and u,
#and reciprocal intrer-cell hoppings s:
def Hamiltonain(r, u, v, onsite, n_cells):
    N = 2 * n_cells
    H = np.zeros((N, N), dtype=complex)
    for i in range(N):
        H[i, i] = onsite
    for i in range(0, N - 1, 2):
        H[i, i + 1] = r
        H[i + 1, i] = u
    for i in range(1, N - 1, 2):
        H[i, i + 1] = v
        H[i + 1, i] = v
    return(H)


#Schrodinger eq: 1j * (d/dt)phi(t) = H(t)phi(t)
#Time-derivative: (d/dt)phi(t) = (phi(t+dt) - phi(t)) / dt
#Combine the above to write phi(t + dt) = U(t)phi(t), where U is of the 1st-order:
#U(t) = 1 - 1j * dt * H(t)
#This is NOT unitary even if H is Hermitian, because dt "isn't infinitesimal".
#So after some illegal maths, we define the 2nd-order time-evolution operator:
def U(h, n_cells, dt):
    U = np.dot((np.identity(2 * n_cells) - 1j * dt * h / 2), np.linalg.inv(np.identity(2 * n_cells) + 1j * dt * h / 2))
    return U


#Write the onsite-potentials as imaginary gain and loss terms.
#Loss and nonlinear saturable gain on every site.
def H(h, phi, gamma1, gamma2, S, n_cells):
    for i in range(2 * n_cells):
        h[i, i] = 1j * (gamma1 / (1 + S * np.abs(phi[i]) ** 2) - gamma2)
    return h
