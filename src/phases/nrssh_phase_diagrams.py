import numpy as np
import matplotlib.pyplot as plt
from src.models.nrssh_lattice import NRSSHLatticeSystem


def find_convergence_time(system, dt=0.015, tolerance=1e-4, max_time=10, verbose=False):
    """
    Find the time it takes for the system to converge to a final state.

    Parameters:
    -----------
    system : HamiltonianSystem
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


def create_phase_diagram(v=0.5, u=0.5, r=0.5, S=5.0, n_cells=40,
                         points=10, dt=0.015, tolerance=1e-4, max_time=10,
                         plot=True, verbose=True):
    """
    Create a phase diagram showing convergence times across gamma1-gamma2 parameter space.

    Parameters:
    -----------
    v, u, r : float
        Hopping parameters for the NRSSH system
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
        print(f"  System parameters: v={v}, u={u}, r={r}, S={S}")
        print(f"  Evolution parameters: dt={dt}, tolerance={tolerance}, max_time={max_time}")

    # Calculate convergence times for each parameter combination
    max_converged_time = 0
    total_points = points * points
    completed_points = 0

    for i, gamma1 in enumerate(gamma1_array):
        for j, gamma2 in enumerate(gamma2_array):
            # Create system with current parameters
            system = NRSSHLatticeSystem(
                n_cells=n_cells,
                v=v,
                u=u,
                r=r,
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
                            converged_mask, v, u, r, S, dt, tolerance, max_time)

    return gamma1_array, gamma2_array, convergence_times, converged_mask


def _plot_phase_diagram(gamma1_array, gamma2_array, convergence_times, converged_mask,
                        v, u, r, S, dt, tolerance, max_time):
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
    plt.title(f'NRSSH Model Phase Diagram\n'
              f'tolerance={tolerance}, S={S}, dt={dt}\n'
              f'v={v}, u={u}, r={r}', fontsize=11)

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


def plot_example_phase_diagram(v=0.5, u=0.5, r=0.5, S=1.0, points=10, verbose=True):
    """
    Plot an example phase diagram with default parameters.

    Parameters:
    -----------
    v, u, r : float
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
        v=v, u=u, r=r, S=S, points=points, verbose=verbose
    )
