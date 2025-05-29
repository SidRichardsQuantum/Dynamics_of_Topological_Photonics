import numpy as np
import matplotlib.pyplot as plt
from src.models.diamond_lattice import Hamiltonain, H, U


n_cells = 33  #Number of cells
N = 3 * n_cells + 1  #Number of sites. Has to be 1 modulo 3 for the Diamond model.
x = np.linspace(1, N, N)  #Mimics real-space

#We have to write a "small" time-interval.
#The smaller dt is, the less the system will evolve.
#Luckily, because we have set h_bar=1, dt is allowed to "look big" like 0.1 or 0.01:
dt = 0.1
T = 49 * dt  #The time for which the evolution stops at (there are only 50 colours available)

#The next four lines are to colour-map the plot
values = np.linspace(1, 50)  #There are 50 colours in the colour-map
normalized_values = values / 50
colormap = plt.colormaps.get_cmap('cool')  #Light blue to hot pink
colors = colormap(normalized_values)


#Function to apply U repeatedly to the wavefunction until time T:
def Evolve(v, u, r, s, gamma1, gamma2, S, n_cells, dt):
    M = 0  #Colour-index for the plot
    time = 0  #Start time
    phi = np.zeros(N)
    phi[0] = 1  #Wavefunction starts entirely on the first site.
    h = Hamiltonain(v, u, r, s, 0, n_cells)
    h = H(h, phi, gamma1, gamma2, S, n_cells)
    while time < T:
        plt.plot(x, np.abs(phi) ** 2, c=colors[M])  #Plots site-intensities in real-space
        phi = np.dot(U(h, n_cells, dt), phi)
        time += dt
        M += 1
        h = H(h, phi, gamma1, gamma2, S, n_cells)
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
#Saturation constant S >= 0
Evolve(0.1, 0.4, 0.7, 0.6, 0.5, 0.8, 1, n_cells, dt)
