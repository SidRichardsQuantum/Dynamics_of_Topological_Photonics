import numpy as np
import matplotlib.pyplot as plt


N = 25  #Number of sites
#We have to write a "small" time-interval.
#The smaller dt is, the less the system will evolve.
#Luckily, because we have set h_bar=1, dt is allowed to "look big" like 0.1 or 0.01:
dt = 0.01

x = np.linspace(1, N, N)  #Mimics real-space
tolerance = 10 ** -3  #Small tolerance e.g: 10 ** -3

#The next four lines are to colour-map the plot
values = np.linspace(1, 50)  #There are 50 colours in the colour-map
normalized_values = values / 50
colormap = plt.colormaps.get_cmap('cool')  #Light blue to hot pink
colors = colormap(normalized_values)


#Hamiltonian for the NRSSH model:
def Hamiltonain(r, u, v):
    H = np.zeros((N, N), dtype=complex)
    for i in range(0, N - 1, 2):
        H[i, i + 1] = r
        H[i + 1, i] = u
    for i in range(1, N - 1, 2):
        H[i, i + 1] = v
        H[i + 1, i] = v
    return(H)


#Write the onsite-potentials as imaginary gain and loss terms
def H(phi, r, u, v, gamma1, gamma2, S):
    H = Hamiltonain(r, u, v)
    for i in range(0, N):
        H[i, i] = 1j * (gamma1 / (1 + S * np.abs(phi[i]) ** 2) - gamma2)
    return H


def U(phi, r, u, v, gamma1, gamma2, S):
    U = np.dot((np.identity(N) - 1j * dt * H(phi, r, u, v, gamma1, gamma2, S) / 2), np.linalg.inv(np.identity(N) + 1j * dt * H(phi, r, u, v, gamma1, gamma2, S) / 2))
    return U


def Final_state(r, u, v, gamma1, gamma2, S):
    M = 49  #Colour-index for the plot
    time = 0  #Start time
    phi = np.zeros(N)
    phi[0] = 1  #Wavefunction starts entirely on the first site.
    dif = tolerance + 1
    while dif >= tolerance:  #This is to evolve the system until a final state is reached.
        phinew = np.dot(U(phi, r, u, v, gamma1, gamma2, S), phi)
        dif = abs(sum(np.abs(phinew) ** 2) - sum(np.abs(phi) ** 2))
        phi = phinew
        time += dt
        if time >= 500:  #Set a time limit.
            break
    while M >= 0:  #This then plots the 50 states leading up to the final.
        plt.plot(x, np.abs(phi) ** 2, c=colors[M], zorder = M - 49)
        phi = np.dot(np.linalg.inv(U(phi, r, u, v, gamma1, gamma2, S)), phi)  #Regenerates the last states by evolving backwards using the inverse of U(t)
        M -= 1
    plt.xlabel('Site-Index')
    plt.ylabel('Intensity')
    plt.title('NRSSH Model Final States')
    plt.xticks(range(0, N + 1, 5))
    plt.xlim(1, N)
    plt.gca().spines['top'].set_visible(False)
    legend_elements = list()
    legend_elements.append(plt.Line2D([0], [0], color='#FF00FF', label='Final time = '+str(round(time, 2))+''))
    legend_elements.append(plt.Line2D([0], [0], color='#00FFFF', label = str(round(time - 49 * dt, 2))))
    plt.legend(handles=legend_elements)
    plt.show()

#Gain coefficient in the interval (0, 1]
#Loss coefficient in the interval (0, 1]
#Saturation constant S >= 0
Final_state(0.1, 0.4, 0.7, 0.6, 0.5, 1)
