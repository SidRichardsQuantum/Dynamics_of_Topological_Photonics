import numpy as np
from .nrssh_lattice import LatticeModel


class DiamondModel(LatticeModel):
    """Diamond lattice model with three sites per unit cell."""

    def __init__(self,
                 unit_cells: int,
                 t_intra_ab: float = 1.0,
                 t_intra_ac: float = 1.0,
                 t_inter_ab: float = 1.0,
                 t_inter_ac: float = 1.0,
                 dimerization: str = '',
                 **kwargs):
        """
        Initialize Diamond model.

        Args:
            unit_cells: Number of unit cells
            t_intra_ab: Between A and B sites in the same cell
            t_intra_ac: Between A and C sites in the same cell
            t_inter_ab: Between A and B sites between different cells
            t_inter_ac: Between A and C sites between different cells
            dimerization: Type of dimerization ('face', 'neighboring')

            face: t_intra_ab = t_inter_ac and t_inter_ab = t_intra_ac
            neighbouring: t_intra_ab = t_inter_ab and t_intra_ac = t_inter_ac
        """
        sites = 3 * unit_cells + 1  # Ends with an extra A site
        super().__init__(sites, **kwargs)
        self.unit_cells = unit_cells
        self.t_intra_ab = t_intra_ab
        self.t_intra_ac = t_intra_ac
        self.t_inter_ab = t_inter_ab
        self.t_inter_ac = t_inter_ac
        self.dimerization = dimerization

    def build_hamiltonian(self) -> np.ndarray:
        """Build Diamond Hamiltonian matrix."""
        if self._hamiltonian is None:
            self._hamiltonian = self._construct_matrix()
        return self._hamiltonian

    def _construct_matrix(self) -> np.ndarray:
        """Construct the Hamiltonian matrix for Diamond model."""
        n_cells = (self.sites - 1) // 3
        N = 3 * n_cells + 1
        H = np.zeros((N, N), dtype=complex)

        # Intra-cell hopping
        for i in range(0, N - 1, 3):
            H[i, i + 1] = self.t_intra_ab
            H[i + 1, i] = self.t_intra_ab
        for i in range(0, N - 2, 3):
            H[i, i + 2] = self.t_intra_ac
            H[i + 2, i] = self.t_intra_ac

        # Inter-cell hopping
        for i in range(2, N - 1, 3):
            H[i, i + 1] = self.t_inter_ab
            H[i + 1, i] = self.t_inter_ab
        for i in range(1, N - 2, 3):
            H[i, i + 2] = self.t_inter_ac
            H[i + 2, i] = self.t_inter_ac

        return H



# def Hamiltonain(v, u, r, s, onsite, n_cells):
#     N = 3 * n_cells + 1  #Number of sites. Has to be 1 mod 3 for the Diamond model
#     H = np.zeros((N, N), dtype=complex)
#     for i in range(N):
#         H[i, i] = onsite
#     for i in range(0, N - 1, 3):
#         H[i, i + 1] = u
#         H[i + 1, i] = u
#     for i in range(0, N - 2, 3):
#         H[i, i + 2] = s
#         H[i + 2, i] = s
#     for i in range(2, N - 1, 3):
#         H[i, i + 1] = r
#         H[i + 1, i] = r
#     for i in range(1, N - 2, 3):
#         H[i, i + 2] = v
#         H[i + 2, i] = v
#     return(H)
#
#
# #Schrodinger eq: 1j * (d/dt)phi(t) = H(t)phi(t)
# #Time-derivative: (d/dt)phi(t) = (phi(t+dt) - phi(t)) / dt
# #Combine the above to write phi(t + dt) = U(t)phi(t), where U is of the 1st-order:
# #U(t) = 1 - 1j * dt * H(t)
# #This is NOT unitary even if H is Hermitian, because dt "isn't infinitesimal".
# #So after some illegal maths, we define the 2nd-order time-evolution operator:
# def U(h, n_cells, dt):
#     U = np.dot((np.identity(3 * n_cells + 1) - 1j * dt * h / 2), np.linalg.inv(np.identity(3 * n_cells + 1) + 1j * dt * h / 2))
#     return U
#
#
# #Write the onsite-potentials as imaginary gain and loss terms.
# #Nonlinear saturable gain on the A-sites.
# #Loss on the B- and C-sites.
# def H(h, phi, gamma1, gamma2, S, n_cells):
#     for i in range(0, 3 * n_cells + 1, 3):
#         h[i, i] = 1j * gamma1 / (1 + S * np.abs(phi[i]) ** 2)
#     for i in range(1, 3 * n_cells + 1, 3):
#         h[i, i] = -1j * gamma2
#     for i in range(2, 3 * n_cells + 1, 3):
#         h[i, i] = -1j * gamma2
#     return h
