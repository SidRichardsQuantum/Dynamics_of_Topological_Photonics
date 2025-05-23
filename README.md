# Dynamics of Topological Photonics with Nonlinear Saturable Gain and Loss

This is a revamped version of my dissertation code at Lancaster University, where i worked with Dr Henning Schomerus on topological laser phases, edge modes and numerical simulations.

### In this repo, we study two main lattices:
- The non-reciprocal Su–Schrieffer–Heeger (NRSSH) model with alternating inter and intra-cell hopping strengths, where the left and right intra-cell hoppings are unequal.
- Diamond (Rhombic) model with three sites A, B, C per cell.
There are no hoppings between sites B and C, hence this model may be referred to as the "ladder lattice" or something similar.
Different combinations of which hoppings are equal form different "dimerizations" - leading to exotic laser phases.

First, we work on defining the Hamiltonians by writing its entries [i, j] equal to the hopping strength from site j to site i.
The Hamiltonian's eigenvalues (eigenenergies) are then calculated and plotted against momentum(k)-space, to see the lattice's band (gap) structure in the first Brillouin zone.
We refer to the momentum as 'k', following the Planck relation p = h_bar * k and setting Planck's reduced constant h_bar = 1.
(This formulism will actually prove useful when considering an infinitesimal time interval dt.)

Next, we plot the same Hamiltonian's eigenvectors real-space, to visualize localized edge-states.
These edge-modes are only present in topologically insulating phases, and are akin to eigenenergies within the band gap.

We then toggle the Hamiltonian's onsite energies to become imaginary terms corresponding to gain and loss.
The gain term has a saturation S that limits gain nonlinearly - depending on the site's intensity.
Loss is given as a constant term gamma2. Similarly, there is a gain constant gamma1.

We combine the Schrödinger equation and definition of a time-derivative to write phi(t + dt) as a function of H(t) and phi(t), such that phi(t + dt) = U(t) • phi(t).
Here, U(t) is the 1st-order time-evolution operator which evolves phi by time increment dt, and depends on time itself.
However, this operator is NOT unitary, even if the Hamiltonian is Hermitian.
Therefore, we upgrade U to the 2nd-order using some technical mathematics, assuring unitarity.
(Note that if dt was infinitesimally small, then there would be no system evolution - boring!)
The system is then evolved 50 times and the site-intensities are plotted to display how the wavefuntion evolves into the lattice.
(50 because there are 50 colours in our colour-map.)

The previous step is then modified such that we see the final iterations before the state reaches a final state.
A final state is defined such that the difference in successive (time dt apart) total intensities falls below a specific 'tolerance' threshold.
Tolerance and increment dt have a close relationship in terms of runtime - for which we discuss some work-arounds.
Times to reach final states are different depending on gain, loss, saturation and hopping strengths.
Therefore, this is why it's possible to create temporal phase diagrams of gain against loss coefficients!

Finally, the above code is ran over 100s of combinations of gain vs loss, to form entire phase diagrams.
In these diagrams, with help of the file for plotting intensities in real space, we will be able to analse properties of different laser phases.
These phases govern whether edge modes can exist, chaotic lasing behaviour, stability, lossy phases, and apparent blended/combined phases of the forementioned.


## Main results: