import matplotlib.pyplot as plt
from topological_photonics.models.nrssh_lattice import NRSSHLatticeSystem
from topological_photonics.phases.common import create_phase_grid
from topological_photonics.phases.common import find_convergence_time
from topological_photonics.phases.common import plot_phase_diagram_base
from topological_photonics.plotting import output_file


def create_phase_diagram(v=0.5, u=0.5, r=0.5, S=5.0, n_cells=40,
                         points=10, dt=0.1, tolerance=1e-2, max_time=50,
                         plot=True, verbose=True, output_dir="outputs"):
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
    def system_factory(gamma1, gamma2):
        return NRSSHLatticeSystem(
            n_cells=n_cells,
            v=v,
            u=u,
            r=r,
            gamma1=gamma1,
            gamma2=gamma2,
            S=S
        )

    gamma1_array, gamma2_array, convergence_times, converged_mask = create_phase_grid(
        points=points,
        system_factory=system_factory,
        system_description=f"v={v}, u={u}, r={r}, S={S}",
        dt=dt,
        tolerance=tolerance,
        max_time=max_time,
        verbose=verbose,
    )

    if plot:
        plot_phase_diagram(gamma1_array, gamma2_array, convergence_times,
                           converged_mask, v, u, r, S, dt, tolerance, max_time, n_cells,
                           output_dir=output_dir)


    return gamma1_array, gamma2_array, convergence_times, converged_mask


def plot_phase_diagram(gamma1_array, gamma2_array, convergence_times, converged_mask,
                        v, u, r, S, dt, tolerance, max_time, n_cells, output_dir="outputs"):
    """
    Internal function to create and save the phase diagram plot.
    """
    plot_phase_diagram_base(
        gamma1_array,
        gamma2_array,
        convergence_times,
        converged_mask,
        S,
        dt,
        tolerance,
        max_time,
        f'NRSSH Model Phase Diagram\n'
        f'tolerance={tolerance}, S={S}, dt={dt}\n'
        f'v={v}, u={u}, r={r}',
    )

    if v == u == r:
        phase_dir = "tb_model"
    elif v == u:
        phase_dir = "ssh_model"
    else:
        phase_dir = "nrssh_model"

    filename = output_file(
        output_dir,
        "phases",
        "nrssh_phases",
        phase_dir,
        f"N={n_cells}_S={S}_v={v}_u={u}_r={r}.png",
    )

    # Save the plot
    plt.savefig(filename, dpi=300)
    plt.close()  # Close the plot to free memory


def plot_example_phase_diagram(v=0.5, u=0.5, r=0.5, S=1.0, points=10, max_time=50, verbose=True,
                               output_dir="outputs"):
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
        v=v, u=u, r=r, S=S, points=points, max_time=max_time, verbose=verbose,
        output_dir=output_dir
    )
