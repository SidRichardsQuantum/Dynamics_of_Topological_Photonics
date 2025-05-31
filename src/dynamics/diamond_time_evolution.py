import numpy as np
import matplotlib.pyplot as plt
from src.models.diamond_lattice import DiamondLatticeSystem
#

def evolve_and_plot(system, dt, total_time, plot_interval=None):
    """
    Evolve the system and plot the wavefunction intensity over time.

    Parameters:
    -----------
    system : DiamondLatticeSystem
        The system to evolve
    dt : float
        Time step
    total_time : float
        Total evolution time
    plot_interval : int, optional
        Plot every nth step (if None, plots based on available colors)
    """
    N = system.N
    x = np.linspace(1, N, N)  # Mimics real-space

    # Color mapping setup
    n_colors = 50
    values = np.linspace(1, n_colors)
    normalized_values = values / n_colors
    colormap = plt.colormaps.get_cmap('cool')  # Light blue to hot pink
    colors = colormap(normalized_values)

    # Initialize wavefunction - starts entirely on the first site
    phi = np.zeros(N, dtype=complex)
    phi[0] = 1.0

    # Time evolution parameters
    n_steps = int(total_time / dt)
    if plot_interval is None:
        plot_interval = max(1, n_steps // n_colors)

    time = 0.0
    color_index = 0

    plt.figure(figsize=(12, 8))

    for step in range(n_steps + 1):
        # Plot at specified intervals
        if step % plot_interval == 0 and color_index < len(colors):
            plt.plot(x, np.abs(phi) ** 2, c=colors[color_index], alpha=0.8)
            color_index += 1

        # Evolve the system (skip on last step)
        if step < n_steps:
            # Get current Hamiltonian with nonlinear terms
            H = system.get_hamiltonian(phi, onsite=0.0)

            # Get time evolution operator
            U_op = system.time_evolution_operator(H, dt)

            # Evolve the wavefunction
            phi = np.dot(U_op, phi)
            time += dt

    # Formatting and legend
    plt.xlabel('Site-Index')
    plt.ylabel('Intensity')
    legend_elements = [
        plt.Line2D([0], [0], color='#00FFFF', label='Start = '+str(round(time - n_steps * dt, 2))+''),
        plt.Line2D([0], [0], color='#FF00FF', label='Finish = '+str(round(time, 2))+'')
    ]
    plt.legend(handles=legend_elements)
    plt.title('2nd-Order Evolution of the Diamond Model')
    plt.grid(True, alpha=0.3)
    plt.show()

    return phi  # Return final wavefunction


def plot_example_evolution(n_cells=40, t1=0.1, t2=0.4, t3=0.7, t4=0.3, gamma1=0.6, gamma2=0.5, S=1.0,
                           dt=0.1, total_time=None, verbose=True):
    """
    Plot an example time evolution of the Diamond system.

    Parameters:
    -----------
    n_cells : int
        Number of unit cells
    t1, t2, t3, t4 : float
        Hopping parameters
    gamma1, gamma2, S : float
        Gain/loss parameters
    dt : float
        Time step
    total_time : float, optional
        Total evolution time (default: 49*dt for 50 colors)
    verbose : bool
        Whether to print system information

    Returns:
    --------
    final_phi : ndarray
        Final wavefunction after evolution
    system : HamiltonianSystem
        The system object used
    """
    # Create the system
    system = DiamondLatticeSystem(
        n_cells=n_cells,
        t1=t1,  # A and B intra-cell hopping strength
        t2=t2,  # A and C intra-cell hopping strength
        t3=t3,  # A and B inter-cell hopping strength
        t4=t4,  # A and C inter-cell hopping strength
        gamma1=gamma1,  # Gain coefficient (0, 1]
        gamma2=gamma2,  # Loss coefficient (0, 1]
        S=S  # Saturation constant (>= 0)
    )

    # Time evolution parameters
    if total_time is None:
        total_time = 49 * dt  # Evolution stops here (50 colors available)

    if verbose:
        # Print system information
        print(f"System parameters:")
        print(f"  n_cells: {system.n_cells}")
        print(f"  Total sites: {system.N}")
        print(f"  t1: {system.t1}")
        print(f"  t2: {system.t2}")
        print(f"  t3: {system.t3}")
        print(f"  t4: {system.t4}")
        print(f"  gamma1 (gain): {system.gamma1}")
        print(f"  gamma2 (loss): {system.gamma2}")
        print(f"  S (saturation): {system.S}")
        print(f"\nEvolution parameters:")
        print(f"  dt: {dt}")
        print(f"  Total time: {total_time}")
        print(f"  Number of steps: {int(total_time / dt)}")

    # Run the evolution and plotting
    final_phi = evolve_and_plot(system, dt, total_time)

    if verbose:
        # Print final state information
        final_norm = np.linalg.norm(final_phi)
        print(f"\nFinal state:")
        print(f"  Norm: {final_norm:.6f}")
        print(f"  Max intensity: {np.max(np.abs(final_phi) ** 2):.6f}")
        print(f"  Site with max intensity: {np.argmax(np.abs(final_phi) ** 2) + 1}")

    return final_phi, system



# import numpy as np
# import matplotlib.pyplot as plt
# from src.models.diamond_lattice import Hamiltonain, H, U
#
#
# n_cells = 33  #Number of cells
# N = 3 * n_cells + 1  #Number of sites. Has to be 1 modulo 3 for the Diamond model.
# x = np.linspace(1, N, N)  #Mimics real-space
#
# #We have to write a "small" time-interval.
# #The smaller dt is, the less the system will evolve.
# #Luckily, because we have set h_bar=1, dt is allowed to "look big" like 0.1 or 0.01:
# dt = 0.1
# T = 49 * dt  #The time for which the evolution stops at (there are only 50 colours available)
#
# #The next four lines are to colour-map the plot
# values = np.linspace(1, 50)  #There are 50 colours in the colour-map
# normalized_values = values / 50
# colormap = plt.colormaps.get_cmap('cool')  #Light blue to hot pink
# colors = colormap(normalized_values)
#
#
# #Function to apply U repeatedly to the wavefunction until time T:
# def Evolve(v, u, r, s, gamma1, gamma2, S, n_cells, dt):
#     M = 0  #Colour-index for the plot
#     time = 0  #Start time
#     phi = np.zeros(N)
#     phi[0] = 1  #Wavefunction starts entirely on the first site.
#     h = Hamiltonain(v, u, r, s, 0, n_cells)
#     h = H(h, phi, gamma1, gamma2, S, n_cells)
#     while time < T:
#         plt.plot(x, np.abs(phi) ** 2, c=colors[M])  #Plots site-intensities in real-space
#         phi = np.dot(U(h, n_cells, dt), phi)
#         time += dt
#         M += 1
#         h = H(h, phi, gamma1, gamma2, S, n_cells)
#     plt.xlabel('Site-Index')
#     plt.ylabel('Intensity')
#     legend_elements = list()
#     legend_elements.append(plt.Line2D([0], [0], color='#00FFFF', label='Start'))
#     legend_elements.append(plt.Line2D([0], [0], color='#FF00FF', label='Finish'))
#     plt.legend(handles=legend_elements)
#     plt.title('2nd-Order Evolution of the Diamond Model')
#     plt.show()
#
# #Gain coefficient gamma1 in the interval (0, 1]
# #Loss coefficient gamma2 in the interval (0, 1]
# #Saturation constant S >= 0
# Evolve(0.1, 0.4, 0.7, 0.6, 0.5, 0.8, 1, n_cells, dt)
