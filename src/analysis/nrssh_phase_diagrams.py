import numpy as np
import matplotlib.pyplot as plt
from src.models.nrssh import Hamiltonain, H, U


n_cells = 40  #Number of cells
N = 2 * n_cells  #Number of sites. Has to be 1 modulo 3 for the Diamond model.

#We have to write a "small" time-interval.
#The smaller dt is, the less the system will evolve.
#Luckily, because we have set h_bar=1, dt is allowed to "look big" like 0.1 or 0.01:
dt = 0.015

tolerance = 10 ** -4  #Small tolerance e.g: 10 ** -3

#The next four lines are to colour-map the plot:
values = np.linspace(1, 50)  #There are 50 colours in the colour-map
normalized_values = values / 50
colormap = plt.colormaps.get_cmap('cool')  #Light blue to hot pink
colors = colormap(normalized_values)


limit = 10  #Set a time limit to stop certain points from being plotted
def Final_time(r, u, v, gamma1, gamma2, S):
    time = 0  #Start time
    phi = np.zeros(N)
    phi[0] = 1  #Wavefunction starts entirely on the first site.
    h = Hamiltonain(r, u, v, 0, n_cells)
    h = H(h, phi, gamma1, gamma2, S, n_cells)
    dif = tolerance + 1
    while dif >= tolerance:  #This is to evolve the system until a final state is reached.
        phinew = np.dot(U(h, n_cells, dt), phi)
        dif = abs(sum(np.abs(phinew) ** 2) - sum(np.abs(phi) ** 2))
        phi = phinew
        time += dt
        h = H(h, phi, gamma1, gamma2, S, n_cells)
        if time >= limit:  #Set a time limit
            break
    return time


def phase_diagram(r, u, v, S, points):
    p = 0
    gam2 = np.linspace(0, 1, points)  #List of gain values to plot
    gam1 = np.linspace(0, 1, points)  #List of loss values
    for i in range(len(gam1)):
        for k in range(len(gam2)):
            col = Final_time(r, u, v, gam1[i], gam2[k], S)
            if col < limit:
                n = 50 / limit  #Normalisation constant to fit the colours in the map
                plt.scatter(gam1[i], gam2[k], marker='s', c=colors[int(n * col)])
                if col >= p:
                    p = col
    if p < limit - dt:
        print(round(p, 2))
    x = [0, 1]
    y = [0, 1]
    b = [0, 1 / (1 + S)]
    plt.plot(x, y, c='black', label=u'\u03B3$_1=$'u'\u03B3$_2$', linestyle='dashed')
    plt.plot(x, b, c='grey', label=u'\u03B3$_1=(1+S)$'u'\u03B3$_2$', linestyle='dashed')
    plt.ylabel('Loss 'u'\u03B3$_2$')
    plt.xlabel('Gain 'u'\u03B3$_1$')
    plt.title('NRSSH model phase diagram with \n tolerance=' +str(tolerance)+ ', S=' +str(S)+ ', dt=' +str(dt)+ ', \n u=' +str(u)+ ', r=' +str(r)+ '')
    legend_elements = list()
    legend_elements.append(plt.Line2D([0], [0], color='black', label=u'\u03B3$_1=$'u'\u03B3$_2$', linestyle='dashed'))
    legend_elements.append(plt.Line2D([0], [0], color='grey', label=u'\u03B3$_1=(1+S)$'u'\u03B3$_2$', linestyle='dashed'))
    legend_elements.append(plt.Line2D([0], [0], color=colors[0], label='' +str(round(1 / n, 2))+ ''))
    legend_elements.append(plt.Line2D([0], [0], color=colors[-1], label='' +str(round(50 / n, 2))+ ''))
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.legend(handles=legend_elements, loc='upper right')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()

phase_diagram(0.5, 0.5, 0.5, 5, 10)
