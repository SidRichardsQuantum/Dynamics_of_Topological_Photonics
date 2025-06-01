import numpy as np


class NRSSHLatticeSystem:
    """
    A class for simulating a Hamiltonian for the NRSSH model
    with nonlinear saturable gain and constant loss dynamics.
    """

    def __init__(self, n_cells, v=1.0, u=1.0, r=1.0, gamma1=1.0, gamma2=0.5, S=1.0):
        """
        Initialize the Hamiltonian system.

        Parameters:
        -----------
        n_cells : int
            Number of unit cells in the system
        v : float
            Non-reciprocal intra-cell hopping strength (forward)
        u : float
            Non-reciprocal intra-cell hopping strength (backward)
        r : float
            Reciprocal inter-cell hopping strength
        gamma1 : float
            Gain parameter
        gamma2 : float
            Loss parameter
        S : float
            Saturation parameter for nonlinear gain
        """
        self.n_cells = n_cells
        self.N = 2 * n_cells  # Total number of sites
        self.r = r
        self.u = u
        self.v = v
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

        # Intra-cell hopping (non-reciprocal)
        for i in range(0, self.N - 1, 2):
            H[i, i + 1] = self.v
            H[i + 1, i] = self.u

        # Inter-cell hopping (reciprocal)
        for i in range(1, self.N - 1, 2):
            H[i, i + 1] = self.r
            H[i + 1, i] = self.r

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
        for i in range(self.N):
            intensity = np.abs(phi[i]) ** 2
            gain_loss = 1j * (self.gamma1 / (1 + self.S * intensity) - self.gamma2)
            H[i, i] += gain_loss

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
