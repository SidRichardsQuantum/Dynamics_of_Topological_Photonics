import numpy as np


class DiamondLatticeSystem:
    """
    A class for simulating a Hamiltonian for the Diamond lattice model
    with nonlinear saturable gain on A-sites and constant loss on B- and C-sites.
    """

    def __init__(self, n_cells, t1=1.0, t2=1.0, t3=1.0, t4=1.0, gamma1=1.0, gamma2=0.5, S=1.0):
        """
        Initialize the Diamond lattice system.

        Parameters:
        -----------
        n_cells : int
            Number of unit cells in the system
        t1 : float
            Hopping parameter t1
        t2 : float
            Hopping parameter t2
        t3 : float
            Hopping parameter t3
        t4 : float
            Hopping parameter t4
        gamma1 : float
            Gain parameter on A-sites
        gamma2 : float
            Loss parameter on B- and C-sites
        S : float
            Saturation parameter for nonlinear gain
        """
        self.n_cells = n_cells
        self.N = 3 * n_cells + 1  # Total number of sites (must be 1 mod 3 for Diamond model)
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.gamma1 = gamma1
        self.gamma2 = gamma2
        self.S = S

        # Initialize base Hamiltonian
        self.H_base = self._build_base_hamiltonian()

    def _build_base_hamiltonian(self):
        """
        Build the base Hamiltonian with hopping terms (without onsite potentials).
        """
        H = np.zeros((self.N, self.N), dtype=complex)

        for i in range(0, self.N - 1, 3):
            H[i, i + 1] = self.t1
            H[i + 1, i] = self.t1

        for i in range(0, self.N - 2, 3):
            H[i, i + 2] = self.t2
            H[i + 2, i] = self.t2

        for i in range(1, self.N - 2, 3):
            H[i, i + 2] = self.t3
            H[i + 2, i] = self.t3

        for i in range(2, self.N - 1, 3):
            H[i, i + 1] = self.t4
            H[i + 1, i] = self.t4


        return H

    def get_hamiltonian(self, phi=None, onsite=0.0):
        """
        Get the full Hamiltonian including onsite terms.

        Parameters:
        -----------
        phi : array_like, optional
            Wave function for nonlinear onsite potentials
        onsite : float
            Linear onsite potential (default: 0.0)

        Returns:
        --------
        H : ndarray
            Full Hamiltonian matrix
        """
        H = self.H_base.copy()

        # Add linear onsite terms
        for i in range(self.N):
            H[i, i] += onsite

        # Add nonlinear gain/loss terms if phi is provided
        if phi is not None:
            H = self._add_nonlinear_terms(H, phi)

        return H

    def _add_nonlinear_terms(self, H, phi):
        """
        Add nonlinear gain and loss terms to the Hamiltonian.
        - A-sites (i = 0, 3, 6, ...): nonlinear saturable gain
        - B-sites (i = 1, 4, 7, ...): constant loss
        - C-sites (i = 2, 5, 8, ...): constant loss

        Parameters:
        -----------
        H : ndarray
            Hamiltonian matrix to modify
        phi : array_like
            Wave function

        Returns:
        --------
        H : ndarray
            Modified Hamiltonian with nonlinear terms
        """
        # A-sites: nonlinear saturable gain
        for i in range(0, self.N, 3):
            intensity = np.abs(phi[i]) ** 2
            gain = 1j * self.gamma1 / (1 + self.S * intensity)
            H[i, i] += gain

        # B-sites: constant loss
        for i in range(1, self.N, 3):
            loss = -1j * self.gamma2
            H[i, i] += loss

        # C-sites: constant loss
        for i in range(2, self.N, 3):
            loss = -1j * self.gamma2
            H[i, i] += loss

        return H

    def time_evolution_operator(self, H, dt):
        """
        Calculate the second-order time evolution operator.

        U(t) = (I - iH*dt/2) * (I + iH*dt/2)^(-1)

        Parameters:
        -----------
        H : ndarray
            Hamiltonian matrix
        dt : float
            Time step

        Returns:
        --------
        U : ndarray
            Time evolution operator
        """
        I = np.identity(self.N)
        U = np.dot(I - 1j * dt * H / 2, np.linalg.inv(I + 1j * dt * H / 2))
        return U
