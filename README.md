# Dynamics of Topological Photonics with Nonlinear Saturable Gain and Loss

This repository contains a revised version of the code from my dissertation at Lancaster University, developed under the supervision of Dr. Henning Schomerus. The project explores **topological laser phases, edge modes**, and **nonlinear dynamics** in photonic lattices.

## 🧠 Overview

We study two main lattice models:

1. **Non-reciprocal SSH (NRSSH) Model**  
   A variation of the Su–Schrieffer–Heeger model with unequal (non-reciprocal) intra-cell hopping in opposite directions.

2. **Diamond (Rhombic) Model**  
   A lattice with three sites per unit cell (A, B, C). Hoppings occur between A-B and A-C but not between B and C. Different hopping configurations lead to various "dimerizations" and exotic laser phases.

## 🔬 Methodology

### 1. **Hamiltonian Construction**
Hamiltonians are defined by populating the matrix entry `[i, j]` with the hopping strength from site `j` to `i`.  
We compute and visualize:
- **Band structure** in momentum ($k$)-space (First Brillouin zone)
- **Edge states** in real space (topologically protected modes)

### 2. **Inclusion of Gain and Loss**
- Introduced as imaginary onsite potential terms.
- Gain features **nonlinear saturation** controlled by intensity and a saturation parameter `S`.
- `γ₁` (gain) and `γ₂` (loss) are tunable parameters.

### 3. **Time Evolution**
We evolve the system:
- Use a **2nd-order time evolution operator** `U(t)` to generate $\phi(t + dt)$ from $\phi(t)$.
- Evolution is repeated for 50 steps (the number of colours in the colour-map).

### 4. **Steady-State Detection**
The system is evolved until the change in total intensity between time steps falls below a defined **tolerance**.
The site intensities moments before reaching this final state are visualized.

### 5. **Phase Diagram Generation**
Simulations are run over 100s of parameter combinations to create **phase diagrams**. These help analyze:
- Existence of edge modes
- Stability vs chaos
- Loss-dominated and hybrid laser phases

## 📈 Main Results