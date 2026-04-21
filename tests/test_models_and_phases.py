import tempfile
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

from src.models.diamond_lattice import DiamondLatticeSystem
from src.models.nrssh_lattice import NRSSHLatticeSystem
from src.dynamics import diamond_gain_loss, diamond_time_evolution, nrssh_gain_loss, nrssh_time_evolution
from src.phases import diamond_phase_diagrams, nrssh_phase_diagrams
from src.plotting import output_file


class LatticeShapeTests(unittest.TestCase):
    def test_nrssh_hamiltonian_shape_and_hoppings(self):
        system = NRSSHLatticeSystem(n_cells=3, v=0.2, u=0.5, r=0.9)

        self.assertEqual(system.N, 6)
        self.assertEqual(system.H_base.shape, (6, 6))
        self.assertEqual(system.H_base[0, 1], 0.2)
        self.assertEqual(system.H_base[1, 0], 0.5)
        self.assertEqual(system.H_base[1, 2], 0.9)
        self.assertEqual(system.H_base[2, 1], 0.9)

        phi = np.ones(system.N, dtype=complex)
        self.assertEqual(system.get_hamiltonian(phi).shape, (6, 6))

    def test_diamond_hamiltonian_shape_and_hoppings(self):
        system = DiamondLatticeSystem(
            n_cells=2,
            t1=0.1,
            t2=0.2,
            t3=0.3,
            t4=0.4,
        )

        self.assertEqual(system.N, 7)
        self.assertEqual(system.H_base.shape, (7, 7))
        self.assertEqual(system.H_base[0, 1], 0.1)
        self.assertEqual(system.H_base[0, 2], 0.2)
        self.assertEqual(system.H_base[1, 3], 0.3)
        self.assertEqual(system.H_base[2, 3], 0.4)

        phi = np.ones(system.N, dtype=complex)
        self.assertEqual(system.get_hamiltonian(phi).shape, (7, 7))


class NumericalBehaviorTests(unittest.TestCase):
    def test_nrssh_hamiltonian_has_expected_nonreciprocity_and_gain_loss(self):
        system = NRSSHLatticeSystem(
            n_cells=2,
            v=0.2,
            u=0.5,
            r=0.9,
            gamma1=0.6,
            gamma2=0.2,
            S=1.0,
        )
        phi = np.ones(system.N, dtype=complex)
        H = system.get_hamiltonian(phi)

        self.assertNotEqual(system.H_base[0, 1], system.H_base[1, 0])
        self.assertTrue(np.all(np.isfinite(H)))
        np.testing.assert_allclose(np.diag(H).imag, np.full(system.N, 0.1))

    def test_diamond_hamiltonian_has_expected_symmetry_and_gain_loss(self):
        system = DiamondLatticeSystem(
            n_cells=2,
            t1=0.1,
            t2=0.2,
            t3=0.3,
            t4=0.4,
            gamma1=0.6,
            gamma2=0.2,
            S=1.0,
        )
        phi = np.ones(system.N, dtype=complex)
        H = system.get_hamiltonian(phi)

        np.testing.assert_allclose(system.H_base, system.H_base.T.conj())
        self.assertTrue(np.all(np.isfinite(H)))
        np.testing.assert_allclose(np.diag(H)[0::3].imag, np.full(3, 0.3))
        np.testing.assert_allclose(np.diag(H)[1::3].imag, np.full(2, -0.2))
        np.testing.assert_allclose(np.diag(H)[2::3].imag, np.full(2, -0.2))

    def test_time_evolution_operators_are_finite(self):
        nrssh_system = NRSSHLatticeSystem(n_cells=2, v=0.2, u=0.5, r=0.9)
        nrssh_U = nrssh_system.time_evolution_operator(nrssh_system.get_hamiltonian(), 0.05)

        diamond_system = DiamondLatticeSystem(n_cells=1, t1=0.1, t2=0.2, t3=0.3, t4=0.4)
        diamond_U = diamond_system.time_evolution_operator(diamond_system.get_hamiltonian(), 0.05)

        self.assertEqual(nrssh_U.shape, (nrssh_system.N, nrssh_system.N))
        self.assertEqual(diamond_U.shape, (diamond_system.N, diamond_system.N))
        self.assertTrue(np.all(np.isfinite(nrssh_U)))
        self.assertTrue(np.all(np.isfinite(diamond_U)))

    def test_short_time_evolution_returns_finite_wavefunctions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            nrssh_phi, nrssh_system = nrssh_time_evolution.plot_example_evolution(
                n_cells=2,
                total_time=0.1,
                verbose=False,
                output_dir=tmpdir,
            )
            diamond_phi, diamond_system = diamond_time_evolution.plot_example_evolution(
                n_cells=1,
                total_time=0.1,
                verbose=False,
                output_dir=tmpdir,
            )

            self.assertEqual(nrssh_phi.shape, (nrssh_system.N,))
            self.assertEqual(diamond_phi.shape, (diamond_system.N,))
            self.assertTrue(np.all(np.isfinite(nrssh_phi)))
            self.assertTrue(np.all(np.isfinite(diamond_phi)))

    def test_final_state_search_returns_finite_values_without_plotting(self):
        nrssh_system = NRSSHLatticeSystem(n_cells=2, v=0.2, u=0.5, r=0.9)
        nrssh_phi, nrssh_time, nrssh_converged = nrssh_gain_loss.find_and_plot_final_state(
            nrssh_system,
            v=0.2,
            u=0.5,
            r=0.9,
            max_time=0.1,
            plot=False,
            verbose=False,
        )

        diamond_system = DiamondLatticeSystem(n_cells=1, t1=0.1, t2=0.2, t3=0.3, t4=0.4)
        diamond_phi, diamond_time, diamond_converged = diamond_gain_loss.find_and_plot_final_state(
            diamond_system,
            t1=0.1,
            t2=0.2,
            t3=0.3,
            t4=0.4,
            gamma1=0.5,
            gamma2=0.2,
            max_time=0.1,
            plot=False,
            verbose=False,
        )

        self.assertTrue(np.all(np.isfinite(nrssh_phi)))
        self.assertTrue(np.all(np.isfinite(diamond_phi)))
        self.assertTrue(np.isfinite(nrssh_time))
        self.assertTrue(np.isfinite(diamond_time))
        self.assertIsInstance(nrssh_converged, bool)
        self.assertIsInstance(diamond_converged, bool)


class PhaseGridTests(unittest.TestCase):
    def test_nrssh_phase_grid_supports_small_point_counts(self):
        gamma1, gamma2, convergence_times, converged = nrssh_phase_diagrams.create_phase_diagram(
            points=3,
            n_cells=2,
            max_time=0.1,
            plot=False,
            verbose=False,
        )

        self.assertEqual(gamma1.shape, (3,))
        self.assertEqual(gamma2.shape, (3,))
        self.assertEqual(convergence_times.shape, (3, 3))
        self.assertEqual(converged.shape, (3, 3))
        self.assertTrue(np.all(np.isfinite(convergence_times)))
        self.assertTrue(np.all(convergence_times <= 0.1))

    def test_diamond_phase_grid_supports_small_point_counts(self):
        gamma1, gamma2, convergence_times, converged = diamond_phase_diagrams.create_phase_diagram(
            points=3,
            n_cells=1,
            max_time=0.1,
            plot=False,
            verbose=False,
        )

        self.assertEqual(gamma1.shape, (3,))
        self.assertEqual(gamma2.shape, (3,))
        self.assertEqual(convergence_times.shape, (3, 3))
        self.assertEqual(converged.shape, (3, 3))
        self.assertTrue(np.all(np.isfinite(convergence_times)))
        self.assertTrue(np.all(convergence_times <= 0.1))

    def test_phase_grid_rejects_zero_points(self):
        with self.assertRaises(ValueError):
            nrssh_phase_diagrams.create_phase_diagram(points=0, plot=False, verbose=False)

        with self.assertRaises(ValueError):
            diamond_phase_diagrams.create_phase_diagram(points=0, plot=False, verbose=False)


class PlotPathTests(unittest.TestCase):
    def test_output_file_creates_parent_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = output_file(tmpdir, "nested", "path", "plot.png")

            self.assertEqual(filename, str(Path(tmpdir, "nested", "path", "plot.png")))
            self.assertTrue(Path(filename).parent.exists())

    def test_diamond_mixed_hopping_plot_creates_output_directory(self):
        gamma_values = np.array([0.0])
        convergence_times = np.array([[0.1]])
        converged_mask = np.array([[True]])

        with tempfile.TemporaryDirectory() as tmpdir:
            diamond_phase_diagrams.plot_phase_diagram(
                gamma_values,
                gamma_values,
                convergence_times,
                converged_mask,
                0.1,
                0.2,
                0.3,
                0.4,
                1.0,
                0.1,
                1e-2,
                1.0,
                1,
                output_dir=tmpdir,
            )

            expected_file = Path(
                tmpdir,
                "phases/diamond_phases/mixed_hoppings/"
                "N=4_S=1.0_t1=0.1_t2=0.2_t3=0.3_t4=0.4.png",
            )
            self.assertTrue(expected_file.exists())

    def test_nrssh_equal_hopping_plot_creates_output_directory(self):
        gamma_values = np.array([0.0])
        convergence_times = np.array([[0.1]])
        converged_mask = np.array([[True]])

        with tempfile.TemporaryDirectory() as tmpdir:
            nrssh_phase_diagrams.plot_phase_diagram(
                gamma_values,
                gamma_values,
                convergence_times,
                converged_mask,
                0.5,
                0.5,
                0.5,
                1.0,
                0.1,
                1e-2,
                1.0,
                2,
                output_dir=tmpdir,
            )

            expected_file = Path(
                tmpdir,
                "phases/nrssh_phases/tb_model/N=2_S=1.0_v=0.5_u=0.5_r=0.5.png",
            )
            self.assertTrue(expected_file.exists())


if __name__ == "__main__":
    unittest.main()
