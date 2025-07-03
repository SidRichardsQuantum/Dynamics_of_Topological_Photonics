import numpy as np
import matplotlib.pyplot as plt
from src.models.nrssh_lattice import NRSSHLatticeSystem
import os


def evolve_and_plot(system, dt, total_time, plot_interval=None, verbose=True):
    """
    Evolve the system and save the wavefunction intensity plot over time.

    Parameters:
    -----------
    system : HamiltonianSystem
        The system to evolve
    dt : float
        Time step
    total_time : float
        Total evolution time
    plot_interval : int, optional
        Plot every nth step (if None, plots based on available colors)
    verbose : bool
        Whether to print save path
    """
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)

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
            H = system.get_hamiltonian(phi, onsite=0.0)
            U_op = system.time_evolution_operator(H, dt)
            phi = np.dot(U_op, phi)
            time += dt

    # Formatting and legend
    plt.xlabel('Site-Index')
    plt.ylabel('Intensity')
    legend_elements = [
        plt.Line2D([0], [0], color='#00FFFF', label='Start = ' + str(round(time - n_steps * dt, 2))),
        plt.Line2D([0], [0], color='#FF00FF', label='Finish = ' + str(round(time, 2)))
    ]
    plt.legend(handles=legend_elements)
    plt.title('2nd-Order Evolution of the NRSSH Model')
    plt.grid(True, alpha=0.3)

    # Generate filename
    filename = (f"images/nrssh_first_moments_n_cells={system.n_cells}_v={system.v}_u={system.u}_"
                f"r={system.r}_gamma1={system.gamma1}_gamma2={system.gamma2}_S={system.S}.png")
    plt.savefig(filename, dpi=300)
    plt.close()

    if verbose:
        print(f"Plot saved to {filename}")

    return phi  # Return final wavefunction


def plot_example_evolution(n_cells=40, v=0.1, u=0.4, r=0.7, gamma1=0.6, gamma2=0.5, S=1.0,
                           dt=0.1, total_time=None, verbose=True):
    """
    Plot an example time evolution of the NRSSH system.

    Returns:
    --------
    final_phi : ndarray
        Final wavefunction after evolution
    system : HamiltonianSystem
        The system object used
    """
    # Create the system
    system = NRSSHLatticeSystem(
        n_cells=n_cells,
        v=v,  # Non-reciprocal forward hopping
        u=u,  # Non-reciprocal backward hopping
        r=r,  # Reciprocal inter-cell hopping
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
        print(f"  v (forward hopping): {system.v}")
        print(f"  u (backward hopping): {system.u}")
        print(f"  r (inter-cell hopping): {system.r}")
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
