import matplotlib.pyplot as plt
from topological_photonics.models.diamond_lattice import DiamondLatticeSystem
from topological_photonics.phases.common import create_phase_grid
from topological_photonics.phases.common import find_convergence_time
from topological_photonics.phases.common import plot_phase_diagram_base
from topological_photonics.plotting import output_file


def create_phase_diagram(t1=0.5, t2=0.1, t3=0.1, t4=0.5, S=1.0, n_cells=15,
                         points=20, dt=0.1, tolerance=1e-2, max_time=75,
                         plot=True, verbose=True, output_dir="outputs"):
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
    def system_factory(gamma1, gamma2):
        return DiamondLatticeSystem(
            n_cells=n_cells,
            t1=t1,
            t2=t2,
            t3=t3,
            t4=t4,
            gamma1=gamma1,
            gamma2=gamma2,
            S=S
        )

    gamma1_array, gamma2_array, convergence_times, converged_mask = create_phase_grid(
        points=points,
        system_factory=system_factory,
        system_description=f"t1={t1}, t2={t2}, t3={t3}, t4={t4}, S={S}",
        dt=dt,
        tolerance=tolerance,
        max_time=max_time,
        verbose=verbose,
    )
    
    if plot:
        plot_phase_diagram(gamma1_array, gamma2_array, convergence_times,
                            converged_mask, t1, t2, t3, t4, S, dt, tolerance, max_time, n_cells,
                            output_dir=output_dir)

    return gamma1_array, gamma2_array, convergence_times, converged_mask


def plot_phase_diagram(gamma1_array, gamma2_array, convergence_times, converged_mask,
                        t1, t2, t3, t4, S, dt, tolerance, max_time, n_cells, output_dir="outputs"):
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
        f'Diamond Model Phase Diagram\n'
        f'tolerance={tolerance}, S={S}, dt={dt}\n'
        f't1={t1}, t2={t2}, t3={t3}, t4={t4}',
    )

    if t1 == t2 == t3 == t4:
        phase_dir = "equal_hoppings"
    elif t1 == t4 and t2 == t3:
        phase_dir = "facing_dimerization"
    elif t1 == t3 and t2 == t4:
        phase_dir = "neighbouring_dimerization"
    elif t1 == t2 and t3 == t4:
        phase_dir = "intra_vs_inter"
    else:
        phase_dir = "mixed_hoppings"

    filename = output_file(
        output_dir,
        "phases",
        "diamond_phases",
        phase_dir,
        f"N={3 * n_cells + 1}_S={S}_t1={t1}_t2={t2}_t3={t3}_t4={t4}.png",
    )

    # Save the plot
    plt.savefig(filename, dpi=300)
    plt.close()  # Close the plot to free memory


def plot_example_phase_diagram(t1=0.5, t2=0.1, t3=0.1, t4=0.5, S=1.0, points=20, max_time=75,
                               verbose=True, output_dir="outputs"):
    """Plot an example phase diagram with default parameters."""

    return create_phase_diagram(t1=t1, t2=t2, t3=t3, t4=t4, S=S,
                                points=points, max_time=max_time, verbose=verbose,
                                output_dir=output_dir)
