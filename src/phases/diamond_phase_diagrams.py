import numpy as np
import matplotlib.pyplot as plt
from src.models.diamond_lattice import DiamondLatticeSystem
#

def find_convergence_time(system, dt=0.015, tolerance=1e-4, max_time=10, verbose=False):
    """
    Find the time it takes for the system to converge to a final state.

    Parameters:
    -----------
    system : DiamondLatticeSystem
        The system to evolve
    dt : float
        Time step for evolution
    tolerance : float
        Convergence tolerance
    max_time : float
        Maximum time limit to prevent infinite loops
    verbose : bool
        Whether to print evolution information

    Returns:
    --------
    convergence_time : float
        Time at which the system converged (max_time if no convergence)
    converged : bool
        Whether the system actually converged within the time limit
    """
    N = system.N
    time = 0.0

    # Initialize wavefunction - starts entirely on the first site
    phi = np.zeros(N, dtype=complex)
    phi[0] = 1.0

    dif = tolerance + 1
    converged = False

    if verbose:
        print(f"Finding convergence time for gamma1={system.gamma1:.3f}, gamma2={system.gamma2:.3f}")

    while dif >= tolerance:
        # Get current Hamiltonian with nonlinear terms
        H = system.get_hamiltonian(phi, onsite=0.0)

        # Get time evolution operator
        U_op = system.time_evolution_operator(H, dt)

        # Evolve the wavefunction
        phi_new = np.dot(U_op, phi)

        # Check convergence (difference in intensity)
        dif = abs(sum(np.abs(phi_new) ** 2) - sum(np.abs(phi) ** 2))

        phi = phi_new
        time += dt

        # Time limit check
        if time >= max_time:
            if verbose:
                print(f"  Reached time limit {max_time} without convergence")
            break
    else:
        converged = True
        if verbose:
            print(f"  Converged at time = {time:.4f}")

    return time, converged


def create_phase_diagram(t1=0.5, t2=0.5, t3=0.5, t4=0.5, S=1.0, n_cells=33,
                         points=10, dt=0.015, tolerance=1e-4, max_time=10,
                         plot=True, verbose=True):
    """
    Create a phase diagram showing convergence times across gamma1-gamma2 parameter space.

    Parameters:
    -----------
    t1, t2, t3, t4: float
        Hopping parameters for the Diamond system
    S : float
        Saturation constant
    n_cells : int
        Number of unit cells
    points : int
        Number of points along each axis of the phase diagram
    dt : float
        Time step for evolution
    tolerance : float
        Convergence tolerance
    max_time : float
        Maximum evolution time
    plot : bool
        Whether to create and show the plot
    verbose : bool
        Whether to print progress information

    Returns:
    --------
    gamma1_array : ndarray
        Array of gamma1 values
    gamma2_array : ndarray
        Array of gamma2 values
    convergence_times : ndarray
        2D array of convergence times
    converged_mask : ndarray
        2D boolean array indicating which points converged
    """
    # Create parameter arrays
    gamma1_array = np.linspace(0, 1, points)
    gamma2_array = np.linspace(0, 1, points)

    # Initialize results arrays
    convergence_times = np.zeros((points, points))
    converged_mask = np.zeros((points, points), dtype=bool)

    if verbose:
        print(f"Creating phase diagram...")
        print(f"  Parameter ranges: gamma1=[0,1], gamma2=[0,1]")
        print(f"  Grid size: {points}x{points}")
        print(f"  System parameters: t1={t1}, t2={t2}, t3={t3}, t4={t4}, S={S}")
        print(f"  Evolution parameters: dt={dt}, tolerance={tolerance}, max_time={max_time}")

    # Calculate convergence times for each parameter combination
    max_converged_time = 0
    total_points = points * points
    completed_points = 0

    for i, gamma1 in enumerate(gamma1_array):
        for j, gamma2 in enumerate(gamma2_array):
            # Create system with current parameters
            system = DiamondLatticeSystem(
                n_cells=n_cells,
                t1=t1,  # A and B intra-cell hopping strength
                t2=t2,  # A and C intra-cell hopping strength
                t3=t3,  # A and B inter-cell hopping strength
                t4=t4,  # A and C inter-cell hopping strength
                gamma1=gamma1,
                gamma2=gamma2,
                S=S
            )

            # Find convergence time
            conv_time, converged = find_convergence_time(
                system, dt=dt, tolerance=tolerance, max_time=max_time
            )

            convergence_times[i, j] = conv_time
            converged_mask[i, j] = converged

            if converged and conv_time > max_converged_time:
                max_converged_time = conv_time

            completed_points += 1
            if verbose and completed_points % (total_points // 10) == 0:
                progress = (completed_points / total_points) * 100
                print(f"  Progress: {progress:.0f}%")

    if verbose:
        converged_count = np.sum(converged_mask)
        print(f"  Completed! {converged_count}/{total_points} points converged")
        if max_converged_time > 0:
            print(f"  Maximum convergence time: {max_converged_time:.4f}")

    if plot:
        _plot_phase_diagram(gamma1_array, gamma2_array, convergence_times,
                            converged_mask, t1, t2, t3, t4, S, dt, tolerance, max_time)

    return gamma1_array, gamma2_array, convergence_times, converged_mask


def _plot_phase_diagram(gamma1_array, gamma2_array, convergence_times, converged_mask,
                        t1, t2, t3, t4, S, dt, tolerance, max_time):
    """
    Internal function to create the phase diagram plot.
    """
    # Set up color mapping
    n_colors = 50
    values = np.linspace(1, n_colors)
    normalized_values = values / n_colors
    colormap = plt.colormaps.get_cmap('cool')  # Light blue to hot pink
    colors = colormap(normalized_values)

    plt.figure(figsize=(10, 8))

    # Plot points that converged within time limit
    normalization_factor = n_colors / max_time

    for i, gamma1 in enumerate(gamma1_array):
        for j, gamma2 in enumerate(gamma2_array):
            if converged_mask[i, j]:
                conv_time = convergence_times[i, j]
                color_index = int(normalization_factor * conv_time)
                color_index = min(color_index, n_colors - 1)  # Ensure within bounds

                plt.scatter(gamma1, gamma2, marker='s', c=[colors[color_index]], s=50)

    # Add theoretical lines
    x_line = [0, 1]
    y_line = [0, 1]
    saturation_line = [0, 1 / (1 + S)]

    plt.plot(x_line, y_line, c='black',
             label=r'$\gamma_1 = \gamma_2$', linestyle='dashed', linewidth=2)
    plt.plot(x_line, saturation_line, c='grey',
             label=r'$\gamma_1 = (1+S)\gamma_2$', linestyle='dashed', linewidth=2)

    # Formatting
    plt.xlabel(r'Gain $\gamma_1$', fontsize=12)
    plt.ylabel(r'Loss $\gamma_2$', fontsize=12)
    plt.title(f'Diamond Model Phase Diagram\n'
              f'tolerance={tolerance}, S={S}, dt={dt}\n'
              f't1={t1}, t2={t2}, t3={t3}, t4={t4}', fontsize=11)

    # Create legend
    legend_elements = [
        plt.Line2D([0], [0], color='black',
                   label=r'$\gamma_1 = \gamma_2$', linestyle='dashed'),
        plt.Line2D([0], [0], color='grey',
                   label=r'$\gamma_1 = (1+S)\gamma_2$', linestyle='dashed'),
        plt.Line2D([0], [0], color=colors[0], marker='s', linestyle='None',
                   label=f'{1 / normalization_factor:.2f}'),
        plt.Line2D([0], [0], color=colors[-1], marker='s', linestyle='None',
                   label=f'{n_colors / normalization_factor:.2f}')
    ]

    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.legend(handles=legend_elements, loc='upper right')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)

    # Remove top and right spines for cleaner look
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()


def plot_example_phase_diagram(t1=0.5, t2=0.5, t3=0.5, t4=0.5, S=1.0, points=10, verbose=True):
    """
    Plot an example phase diagram with default parameters.

    Parameters:
    -----------
    t1, t2, t3, t4 : float
        Hopping parameters
    S : float
        Saturation constant
    points : int
        Number of points along each axis
    verbose : bool
        Whether to print information

    Returns:
    --------
    gamma1_array, gamma2_array : ndarray
        Parameter arrays
    convergence_times : ndarray
        2D array of convergence times
    converged_mask : ndarray
        2D boolean array indicating convergence
    """
    return create_phase_diagram(
        t1=t1, t2=t2, t3=t3, t4=t4, S=S, points=points, verbose=verbose
    )



# import numpy as np
# import matplotlib.pyplot as plt
# from src.models.diamond_lattice import Hamiltonain, H, U
#
#
# n_cells = 33  #Number of cells
# N = 3 * n_cells + 1  #Number of sites. Has to be 1 modulo 3 for the Diamond model.
#
# #We have to write a "small" time-interval.
# #The smaller dt is, the less the system will evolve.
# #Luckily, because we have set h_bar=1, dt is allowed to "look big" like 0.1 or 0.01:
# dt = 0.01
#
# tolerance = 10 ** -3  #Small tolerance e.g: 10 ** -3
#
# #The next four lines are to colour-map the plot:
# values = np.linspace(1, 50)  #There are 50 colours in the colour-map
# normalized_values = values / 50
# colormap = plt.colormaps.get_cmap('cool')  #Light blue to hot pink
# colors = colormap(normalized_values)
#
#
# limit = 10  #Set a time limit to stop certain points from being plotted
# def Final_time(v, u, r, s, gamma1, gamma2, S):
#     time = 0  #Start time
#     phi = np.zeros(N)
#     phi[0] = 1  #Wavefunction starts entirely on the first site.
#     h = Hamiltonain(v, u, r, s, 0, n_cells)
#     h = H(h, phi, gamma1, gamma2, S, n_cells)
#     dif = tolerance + 1
#     while dif >= tolerance:  #This is to evolve the system until a final state is reached.
#         phinew = np.dot(U(h, n_cells, dt), phi)
#         dif = abs(sum(np.abs(phinew) ** 2) - sum(np.abs(phi) ** 2))
#         phi = phinew
#         time += dt
#         h = H(h, phi, gamma1, gamma2, S, n_cells)
#         if time >= limit:  #Set a time limit
#             break
#     return time
#
#
# def phase_diagram(v, u, r, s, S, points):
#     p = 0
#     gam2 = np.linspace(0, 1, points)  #List of gain values to plot
#     gam1 = np.linspace(0, 1, points)  #List of loss values
#     for i in range(len(gam1)):
#         for k in range(len(gam2)):
#             col = Final_time(v, u, r, s, gam1[i], gam2[k], S)
#             if col < limit:
#                 n = 50 / limit  #Normalisation constant to fit the colours in the map
#                 plt.scatter(gam1[i], gam2[k], marker='s', c=colors[int(n * col)])
#                 if col >= p:
#                     p = col
#     if p < limit - dt:
#         print(round(p, 2))
#     x = [0, 1]
#     y = [0, 1]
#     b = [0, 1 / (1 + S)]
#     plt.plot(x, y, c='black', label=u'\u03B3$_1=$'u'\u03B3$_2$', linestyle='dashed')
#     plt.plot(x, b, c='grey', label=u'\u03B3$_1=(1+S)$'u'\u03B3$_2$', linestyle='dashed')
#     plt.ylabel('Loss 'u'\u03B3$_2$')
#     plt.xlabel('Gain 'u'\u03B3$_1$')
#     plt.title('Diamond model phase diagram with \n tolerance=' +str(tolerance)+ ', S=' +str(S)+ ', dt=' +str(dt)+ ', \n u=' +str(u)+ ', s=' +str(s)+ ', r=' +str(r)+ '')
#     legend_elements = list()
#     legend_elements.append(plt.Line2D([0], [0], color='black', label=u'\u03B3$_1=$'u'\u03B3$_2$', linestyle='dashed'))
#     legend_elements.append(plt.Line2D([0], [0], color='grey', label=u'\u03B3$_1=(1+S)$'u'\u03B3$_2$', linestyle='dashed'))
#     legend_elements.append(plt.Line2D([0], [0], color=colors[0], label='' +str(round(1 / n, 2))+ ''))
#     legend_elements.append(plt.Line2D([0], [0], color=colors[-1], label='' +str(round(50 / n, 2))+ ''))
#     plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
#     plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
#     plt.legend(handles=legend_elements, loc='upper right')
#     plt.xlim(0, 1)
#     plt.ylim(0, 1)
#     plt.show()
#
# phase_diagram(0.1, 0.3, 0.6, 0.9, 1, 10)
