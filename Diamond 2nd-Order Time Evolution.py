import numpy as np
import matplotlib.pyplot as plt


N = 50  #Number of sites
#We have to write a "small" time-interval.
#The smaller dt is, the less the system will evolve.
#Luckily, because we have set h_bar=1, dt is allowed to "look big" like 0.1 or 0.01:
dt = 0.1

T = 49 * dt  #The time for which the evolution stops at (there are only 50 colours available)
x = np.linspace(1, N, N)  #Mimics real-space

#The next four lines are to colour-map the plot
values = np.linspace(1, 50)  #There are 50 colours in the colour-map
normalized_values = values / 50
colormap = plt.colormaps.get_cmap('cool')  #Light blue to hot pink
colors = colormap(normalized_values)

#Hamiltonian for the NRSSH model:
def Hamiltonain(v, u, r, s):
    H = np.zeros((N, N), dtype=complex)
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

#Write the onsite-potentials as imaginary gain and loss terms
def H(phi, v, u, r, s, gamma1, gamma2, S):
    H = Hamiltonain(v, u, r, s)
    for i in range(0, N):
        H[i, i] = 1j * (gamma1 / (1 + S * np.abs(phi[i]) ** 2) - gamma2)
    return H

#Schrodinger eq: 1j * (d/dt)phi(t) = H(t)phi(t)
#Time-derivative: (d/dt)phi(t) = (phi(t+dt) - phi(t)) / dt
#Combine the above to write phi(t + dt) = U(t)phi(t), where U is of the 1st-order:
#U(t) = 1 - 1j * dt * H(t)
#This is NOT unitary even if H is Hermitian, because dt "isn't infinitesimal".
#So after some illegal maths, we define the 2nd-order time-evolution operator:
def U(phi, v, u, r, s, gamma1, gamma2, S):
    U = np.dot((np.identity(N) - 1j * dt * H(phi, v, u, r, s, gamma1, gamma2, S) / 2), np.linalg.inv(np.identity(N) + 1j * dt * H(phi, v, u, r, s, gamma1, gamma2, S) / 2))
    return U

#Function to apply U repeatedly to the wavefunction until time T:
def Evolve(v, u, r, s, gamma1, gamma2, S):
    M = 0  #Colour-index for the plot
    time = 0  #Start time
    phi = np.zeros(N)
    phi[0] = 1  #Wavefunction starts entirely on the first site.
    while time < T:
        plt.plot(x, np.abs(phi) ** 2, c=colors[M])  #Plots site-intensities in real-space
        phi = np.dot(U(phi, v, u, r, s, gamma1, gamma2, S), phi)
        time += dt
        M += 1
    plt.xlabel('Site-Index')
    plt.ylabel('Intensity')
    legend_elements = list()
    legend_elements.append(plt.Line2D([0], [0], color='#00FFFF', label='Start'))
    legend_elements.append(plt.Line2D([0], [0], color='#FF00FF', label='Finish'))
    plt.legend(handles=legend_elements)
    plt.title('2nd-Order Evolution of the Diamond Model')
    plt.show()

#Gain coefficient gamma1 in the interval (0, 1]
#Loss coefficient gamma2 in the interval (0, 1]
#Saturation constant S
Evolve(0.1, 0.4, 0.7, 0.6, 0.5, 0.8, 1)
