import numpy as np
import matplotlib.pyplot as plt
from src.models.nrssh_lattice import HamiltonianSystem


def find_and_plot_final_state(system, dt=0.01, tolerance=1e-3, max_time=500, n_backtrack=50,
                              plot=True, verbose=True):
    """
    Find the final state of the system and plot the evolution leading to it.

    Parameters:
    -----------
    system : HamiltonianSystem
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
        plt.title('NRSSH Model Final States')
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


def plot_example_final_state(n_cells=40, v=0.1, u=0.4, r=0.7, gamma1=0.6, gamma2=0.5, S=1.0,
                             dt=0.01, tolerance=1e-4, max_time=500, verbose=True):
    """
    Plot an example final state evolution of the NRSSH system.

    Parameters:
    -----------
    n_cells : int
        Number of unit cells
    v, u, r : float
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
    system = HamiltonianSystem(
        n_cells=n_cells,
        v=v,  # Non-reciprocal forward hopping
        u=u,  # Non-reciprocal backward hopping
        r=r,  # Reciprocal inter-cell hopping
        gamma1=gamma1,  # Gain coefficient (0, 1]
        gamma2=gamma2,  # Loss coefficient (0, 1]
        S=S  # Saturation constant (>= 0)
    )

    if verbose:
        print(f"System parameters:")
        print(f"  n_cells: {system.n_cells}")
        print(f"  Total sites: {system.N}")
        print(f"  v (forward hopping): {system.v}")
        print(f"  u (backward hopping): {system.u}")
        print(f"  r (inter-cell hopping): {system.r}")
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
