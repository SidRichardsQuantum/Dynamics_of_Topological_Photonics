import numpy as np
import matplotlib.pyplot as plt
from diamond.model import Hamiltonain, H, U


n_cells = 33  #Number of cells
N = 3 * n_cells + 1  #Number of sites. Has to be 1 modulo 3 for the Diamond model.
x = np.linspace(1, N, N)  #Mimics real-space

#We have to write a "small" time-interval.
#The smaller dt is, the less the system will evolve.
#Luckily, because we have set h_bar=1, dt is allowed to "look big" like 0.1 or 0.01:
dt = 0.01

tolerance = 10 ** -3  #Small tolerance e.g: 10 ** -3

#The next four lines are to colour-map the plot:
values = np.linspace(1, 50)  #There are 50 colours in the colour-map
normalized_values = values / 50
colormap = plt.colormaps.get_cmap('cool')  #Light blue to hot pink
colors = colormap(normalized_values)


def Final_state(v, u, r, s, gamma1, gamma2, S):
    M = 49  #Colour-index for the plot
    time = 0  #Start time
    phi = np.zeros(N)
    phi[0] = 1  #Wavefunction starts entirely on the first site.
    h = Hamiltonain(v, u, r, s, 0, n_cells)
    h = H(h, phi, gamma1, gamma2, S, n_cells)
    dif = tolerance + 1
    while dif >= tolerance:  #This is to evolve the system until a final state is reached.
        phinew = np.dot(U(h, n_cells, dt), phi)
        dif = abs(sum(np.abs(phinew) ** 2) - sum(np.abs(phi) ** 2))
        phi = phinew
        time += dt
        h = H(h, phi, gamma1, gamma2, S, n_cells)
        if time >= 500:  #Set a time limit.
            break
    while M >= 0:  #This then plots the 50 states leading up to the final.
        plt.plot(x, np.abs(phi) ** 2, c=colors[M], zorder = M - 49)
        phi = np.dot(np.linalg.inv(U(h, n_cells, dt)), phi)  #Regenerates the last states by evolving backwards using the inverse of U(t)
        h = H(h, phi, gamma1, gamma2, S, n_cells)
        M -= 1
    plt.xlabel('Site-Index')
    plt.ylabel('Intensity')
    plt.title('Diamond Model Final States')
    plt.xticks(range(0, 3 * n_cells + 2, 5))
    plt.xlim(1, 3 * n_cells + 1)
    plt.gca().spines['top'].set_visible(False)
    legend_elements = list()
    legend_elements.append(plt.Line2D([0], [0], color='#FF00FF', label='Final time = '+str(round(time, 2))+''))
    legend_elements.append(plt.Line2D([0], [0], color='#00FFFF', label = str(round(time - 49 * dt, 2))))
    plt.legend(handles=legend_elements)
    plt.show()

#Gain coefficient in the interval (0, 1]
#Loss coefficient in the interval (0, 1]
#Saturation constant S >= 0
Final_state(0.1, 0.4, 0.7, 0.9, 0.6, 0.5, 1)
