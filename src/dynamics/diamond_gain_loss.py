import numpy as np
import matplotlib.pyplot as plt
from src.models.diamond_lattice import DiamondLatticeSystem
#

def find_and_plot_final_state(system, dt=0.01, tolerance=1e-3, max_time=50, n_backtrack=50,
                              plot=True, verbose=True):
    """
    Find the final state of the system and plot the evolution leading to it.

    Parameters:
    -----------
    system : DiamondLatticeSystem
        The system to evolve
    dt : float
        Time step
    tolerance : float
        Convergence tolerance for final state
    max_time : float
        Maximum evolution time
    n_backtrack : int
        Number of states to plot by backtracking
    plot : bool
        Whether to create the plot
    verbose : bool
        Whether to print evolution information

    Returns:
    --------
    final_phi : ndarray
        Final converged wavefunction
    final_time : float
        Time at which convergence was reached
    converged : bool
        Whether the system actually converged
    """
    N = system.N
    x = np.linspace(1, N, N)  # Mimics real-space

    # Initialize wavefunction - starts entirely on the first site
    phi = np.zeros(N, dtype=complex)
    phi[0] = 1.0

    time = 0.0
    dif = tolerance + 1
    converged = False

    if verbose:
        print(f"Evolving system to find final state...")
        print(f"  dt: {dt}")
        print(f"  tolerance: {tolerance}")
        print(f"  max_time: {max_time}")

    # Evolve until convergence or max time
    step_count = 0
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
        step_count += 1

        # Print progress occasionally
        if verbose and step_count % 1000 == 0:
            print(f"    Step {step_count}, time = {time:.2f}, diff = {dif:.2e}")

        # Time limit check
        if time >= max_time:
            if verbose:
                print(f"  Reached maximum time {max_time} without convergence")
            break
    else:
        converged = True
        if verbose:
            print(f"  Converged at time = {time:.4f} after {step_count} steps")

    final_phi = phi.copy()
    final_time = time

    if plot:
        # Set up color mapping for backtracking plot
        values = np.linspace(1, n_backtrack)
        normalized_values = values / n_backtrack
        colormap = plt.colormaps.get_cmap('cool')  # Light blue to hot pink
        colors = colormap(normalized_values)

        plt.figure(figsize=(12, 8))

        # Plot the states leading up to the final by evolving backwards
        phi_plot = final_phi.copy()
        for i in range(n_backtrack):
            color_index = n_backtrack - 1 - i
            zorder = n_backtrack - i  # Earlier states in back

            plt.plot(x, np.abs(phi_plot) ** 2, c=colors[color_index],
                     zorder=zorder, alpha=0.8)

            # Evolve backwards (skip on last iteration)
            if i < n_backtrack - 1:
                # Get Hamiltonian for current state
                H = system.get_hamiltonian(phi_plot, onsite=0.0)
                U_op = system.time_evolution_operator(H, dt)

                # Evolve backwards using inverse of U
                try:
                    phi_plot = np.dot(np.linalg.inv(U_op), phi_plot)
                except np.linalg.LinAlgError:
                    if verbose:
                        print(f"Warning: Could not invert U at step {i}, stopping backtrack")
                    break

        # Formatting
        plt.xlabel('Site-Index')
        plt.ylabel('Intensity')
        plt.title('Diamond Model Final States')
        plt.xticks(range(0, N + 1, 5))
        plt.xlim(1, N)
        plt.gca().spines['top'].set_visible(False)
        plt.grid(True, alpha=0.3)

        # Legend
        legend_elements = [
            plt.Line2D([0], [0], color='#FF00FF',
                       label=f'Final time = {round(final_time, 2)}'),
            plt.Line2D([0], [0], color='#00FFFF',
                       label=f'{round(final_time - n_backtrack * dt, 2)}')
        ]
        plt.legend(handles=legend_elements)
        plt.show()

    return final_phi, final_time, converged


def plot_example_final_state(n_cells=40, t1=0.1, t2=0.4, t3=0.7, t4=0.3, gamma1=0.6, gamma2=0.5, S=1.0,
                             dt=0.01, tolerance=1e-4, max_time=50, verbose=True):
    """
    Plot an example final state evolution of the Diamond system.

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
    tolerance : float
        Convergence tolerance
    max_time : float
        Maximum evolution time
    verbose : bool
        Whether to print system information

    Returns:
    --------
    final_phi : ndarray
        Final converged wavefunction
    final_time : float
        Time at convergence
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

    if verbose:
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

    # Find and plot final state
    final_phi, final_time, converged = find_and_plot_final_state(
        system, dt=dt, tolerance=tolerance, max_time=max_time, verbose=verbose
    )

    if verbose:
        print(f"\nFinal state results:")
        print(f"  Converged: {converged}")
        print(f"  Final time: {final_time:.4f}")
        print(f"  Final norm: {np.linalg.norm(final_phi):.6f}")
        print(f"  Max intensity: {np.max(np.abs(final_phi) ** 2):.6f}")
        print(f"  Site with max intensity: {np.argmax(np.abs(final_phi) ** 2) + 1}")

    return final_phi, final_time, system



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
# def Final_state(v, u, r, s, gamma1, gamma2, S):
#     M = 49  #Colour-index for the plot
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
#         if time >= 500:  #Set a time limit
#             break
#     while M >= 0:  #This then plots the 50 states leading up to the final.
#         plt.plot(x, np.abs(phi) ** 2, c=colors[M], zorder = M - 49)
#         phi = np.dot(np.linalg.inv(U(h, n_cells, dt)), phi)  #Regenerates the last states by evolving backwards using the inverse of U(t)
#         h = H(h, phi, gamma1, gamma2, S, n_cells)
#         M -= 1
#     plt.xlabel('Site-Index')
#     plt.ylabel('Intensity')
#     plt.title('Diamond Model Final States')
#     plt.xticks(range(0, 3 * n_cells + 2, 5))
#     plt.xlim(1, 3 * n_cells + 1)
#     plt.gca().spines['top'].set_visible(False)
#     legend_elements = list()
#     legend_elements.append(plt.Line2D([0], [0], color='#FF00FF', label='Final time = '+str(round(time, 2))+''))
#     legend_elements.append(plt.Line2D([0], [0], color='#00FFFF', label = str(round(time - 49 * dt, 2))))
#     plt.legend(handles=legend_elements)
#     plt.show()
#
# #Gain coefficient in the interval (0, 1]
# #Loss coefficient in the interval (0, 1]
# #Saturation constant S >= 0
# Final_state(0.1, 0.4, 0.7, 0.9, 0.6, 0.5, 1)
