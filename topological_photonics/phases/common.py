import numpy as np
import matplotlib.pyplot as plt


def find_convergence_time(system, dt=0.1, tolerance=1e-2, max_time=50, verbose=False):
    """
    Find the time it takes for a lattice system to converge to a final state.
    """
    N = system.N
    time = 0.0

    phi = np.zeros(N, dtype=complex)
    phi[0] = 1.0

    dif = tolerance + 1
    converged = False

    if verbose:
        print(f"Finding convergence time for gamma1={system.gamma1:.3f}, gamma2={system.gamma2:.3f}")

    while dif >= tolerance:
        H = system.get_hamiltonian(phi, onsite=0.0)
        U_op = system.time_evolution_operator(H, dt)
        phi_new = np.dot(U_op, phi)

        dif = abs(sum(np.abs(phi_new) ** 2) - sum(np.abs(phi) ** 2))

        phi = phi_new
        time += dt

        if time >= max_time:
            if verbose:
                print(f"  Reached time limit {max_time} without convergence")
            break
    else:
        converged = True
        if verbose:
            print(f"  Converged at time = {time:.4f}")

    return time, converged


def create_phase_grid(points, system_factory, system_description, dt, tolerance, max_time, verbose):
    """
    Evaluate convergence times over a gamma1-gamma2 parameter grid.
    """
    if points < 1:
        raise ValueError("points must be at least 1")

    gamma1_array = np.linspace(0, 1, points)
    gamma2_array = np.linspace(0, 1, points)
    convergence_times = np.zeros((points, points))
    converged_mask = np.zeros((points, points), dtype=bool)

    if verbose:
        print("Creating phase diagram...")
        print("  Parameter ranges: gamma1=[0,1], gamma2=[0,1]")
        print(f"  Grid size: {points}x{points}")
        print(f"  System parameters: {system_description}")
        print(f"  Evolution parameters: dt={dt}, tolerance={tolerance}, max_time={max_time}")

    max_converged_time = 0
    total_points = points * points
    completed_points = 0
    progress_interval = max(1, total_points // 10)

    for i, gamma1 in enumerate(gamma1_array):
        for j, gamma2 in enumerate(gamma2_array):
            system = system_factory(gamma1, gamma2)
            conv_time, converged = find_convergence_time(
                system, dt=dt, tolerance=tolerance, max_time=max_time
            )

            convergence_times[i, j] = conv_time
            converged_mask[i, j] = converged

            if converged and conv_time > max_converged_time:
                max_converged_time = conv_time

            completed_points += 1
            if verbose and completed_points % progress_interval == 0:
                progress = (completed_points / total_points) * 100
                print(f"  Progress: {progress:.0f}%")

    if verbose:
        converged_count = np.sum(converged_mask)
        print(f"  Completed! {converged_count}/{total_points} points converged")
        if max_converged_time > 0:
            print(f"  Maximum convergence time: {max_converged_time:.4f}")

    return gamma1_array, gamma2_array, convergence_times, converged_mask


def plot_phase_diagram_base(gamma1_array, gamma2_array, convergence_times, converged_mask,
                            S, dt, tolerance, max_time, title):
    """
    Plot the shared phase diagram scaffolding and return the color map used.
    """
    n_colors = 50
    values = np.linspace(1, n_colors)
    normalized_values = values / n_colors
    colormap = plt.colormaps.get_cmap('cool')
    colors = colormap(normalized_values)

    plt.figure(figsize=(10, 8))

    normalization_factor = n_colors / max_time

    for i, gamma1 in enumerate(gamma1_array):
        for j, gamma2 in enumerate(gamma2_array):
            if converged_mask[i, j]:
                conv_time = convergence_times[i, j]
                color_index = int(normalization_factor * conv_time)
                color_index = min(color_index, n_colors - 1)
                plt.scatter(gamma1, gamma2, marker='s', c=[colors[color_index]], s=50)

    x_line = [0, 1]
    y_line = [0, 1]
    saturation_line = [0, 1 / (1 + S)]

    plt.plot(x_line, y_line, c='black',
             label=r'$\gamma_1 = \gamma_2$', linestyle='dashed', linewidth=2)
    plt.plot(x_line, saturation_line, c='grey',
             label=r'$\gamma_1 = (1+S)\gamma_2$', linestyle='dashed', linewidth=2)

    plt.xlabel(r'Gain $\gamma_1$', fontsize=12)
    plt.ylabel(r'Loss $\gamma_2$', fontsize=12)
    plt.title(title, fontsize=11)

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
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
