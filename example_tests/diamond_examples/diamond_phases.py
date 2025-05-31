from src.phases.diamond_phase_diagrams import plot_example_phase_diagram


if __name__ == "__main__":
    # Run default example (matches your original parameters)
    gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram()

    # You can also run with custom parameters:
    # gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram(
    #     t1=0.9, t2=0.7, t3=0.4, t4=0.1, S=1.0, points=10, verbose=True
    # )
#