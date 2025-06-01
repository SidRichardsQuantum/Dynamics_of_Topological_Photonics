# Dynamics of Topological Photonics with Nonlinear Saturable Gain and Loss

This repository contains a revised version of the code from my dissertation at Lancaster University, developed under the supervision of Dr. Henning Schomerus. The project explores the fascinating intersection of **topological laser phases**, **nonlinear optics**, and **quantum physics** by studying how edge modes and nonlinear dynamics behave in photonic lattices through comprehensive phase diagram analysis.

## Table of Contents
- [Quick Start](#quick-start)⚡
- [Why This Work Matters](#why-this-work-matters)
- [Overview](#overview)🧠
- [Methodology](#methodology)🔬
- [Project Structure](#project-structure)
- [Results](#results)📊

## Quick Start

```bash
# Clone the repository
git clone https://github.com/SidRichardsQuantum/Dynamics_of_Topological_Photonics.git
cd Dynamics_of_Topological_Photonics

# Install dependencies
pip install -r requirements.txt

# Run the default example NRSSH model phase diagram
python example_tests/nrssh_examples/nrssh_phases.py
```

```python
'''example_tests.nrssh_examples.nrssh_phases.py

Generate a NRSSH model phase diagram with your chosen parameters'''

from src.phases.nrssh_phase_diagrams import plot_example_phase_diagram

# v, u, r in (0, 1]
# S >= 0
# Recommended that points are between 15 and 25 for quick generation
if __name__ == "__main__":
         gamma1_arr, gamma2_arr, conv_times, conv_mask = plot_example_phase_diagram(
         v=0.3, u=0.2, r=0.9, S=1.0, points=20, verbose=True)
```

## Why This Work Matters

### 🔴 **Advanced Laser Physics**
Understanding how nonlinear gain saturation and loss effects interact in topological lattice systems provides crucial insights for developing next-generation laser technologies. The phase diagrams reveal optimal operating conditions for various laser applications, from high-power semiconductor lasers to exotic chaotic mode-locked systems.

### 🌟 **Novel Optical Phenomena**
The research uncovers complex phase behaviors including:
- **Chaotic lasing regimes** with potential applications in short-pulsed, high peak-power lasers
- **First and second-order phase transitions** that could enable new types of optical switching
- **Critical points** where systems exhibit extreme sensitivity, useful for precision sensing applications

### 🔮 **Quantum Computing Potential**
The lattice models show promising connections to quantum computing architectures:
- **Quantum Annealing**: Phase diagrams could potentially map computational complexity regimes and help optimize quantum algorithms
- **Nonlinear Operations**: Nonlinear gain saturation might represent nonlinear quantum operators that enhance readout signals
- **Decoherence Modeling**: Loss parameters could model environmental decoherence, noise, and quantum errors
- **Topological Connections**: The exchange matrices studied relate to mathematical structures used in topological error correction codes like the toric code

### 🎯 **Real-World Impact**
This research bridges fundamental physics with practical applications:
- **Materials Science**: Understanding dimerization effects in atoms and molecules for developing new optical materials
- **Fiber Optics**: If one were to adapt this code to include nonlinear **loss**, then insights into soliton dynamics and nonlinear wave propagation are possible
- **Quantum Technologies**: Framework for analyzing types of decoherence and error rates in quantum systems

By studying these topological phase diagrams, we gain powerful insights into how complex systems behave under competing effects of gain and loss—knowledge that's essential for advancing both fundamental physics and cutting-edge technologies.

## Overview
We study two main lattice models:

1. **Non-reciprocal SSH (NRSSH) Model** 🔴=🔵-🔴=🔵 A variation of the Su–Schrieffer–Heeger model with unequal (non-reciprocal) intra-cell hopping in opposite directions.

2. **Diamond (Rhombic) Model** 💎 A lattice with three sites per unit cell (A, B, C). Hoppings occur between A-B and A-C but not between B and C. Different hopping configurations lead to various "dimerizations" and exotic laser phases.

## Methodology

### 1. **Hamiltonian Construction**
Hamiltonians are defined by populating the matrix entry $[i, j]$ with the hopping strength from site $j$ to $i$.  
We compute and visualize:
- **Band structure** in momentum ($k$)-space
- **Edge states** in real space (finding topologically protected modes)

### 2. **Inclusion of Gain and Loss**
- Introduced as imaginary onsite potential terms.
- Gain features **nonlinear saturation** controlled by intensity and a saturation parameter $S$.
- $\gamma_1$ (gain) and $\gamma_2$ (loss) are tunable parameters.
- For the NRSSH model: all sites have both gain and loss terms.
- For the diamond model: A sites have gain, B and C sites have loss.

### 3. **Time Evolution**
We evolve the system:
- Using a **2nd-order time evolution operator** $U(t)$ to generate $\phi(t + dt)$ from $\phi(t)$.
- Evolution is repeated for 50 steps (the number of colours in the colour-map).

### 4. **Steady-State Detection**
The system is evolved until the change in total intensity between time steps falls below a chosen **tolerance** parameter.
The site intensities moments before reaching this final state are visualized.

### 5. **Phase Diagram Generation**
Simulations are ran over 100s of parameter combinations to create **phase diagrams**. These help analyze:
- Phases that host topologically-protected edge modes
- Stability vs chaos
- Loss-dominated and hybrid lasing modes

## Project Structure

```
Dynamics_of_Topological_Photonics/
├── README.md                             # This file
├── THEORY.md                             # File explaining the physics behind this project
├── src/                                  # Source code
│   ├── models/
│   │   ├── __init__/
│   │   ├── nrssh_lattice/                # Builds the operators for the NRSSH model
│   │   └── diamond_lattice/              # Builds the operators for the Diamond model
│   ├── dynamics/
│   │   ├── __init__/
│   │   ├── nrssh_time_evolution/         # Evolves the NRSSH model
│   │   ├── nrssh_gain_loss/              # Generates the NRSSH model's final states
│   │   ├── diamond_time_evolution/       # Evolves the Diamond model
│   │   └── diamond_gain_loss/            # Generates the Diamond model's final states
│   └── phases/
│       ├── __init__/
│       ├── nrssh_phase_diagrams/         # Plots the NRSSH model's phase diagram
│       └── diamond_phase_diagrams/       # Plots the Diamond model's phase diagram
└── example_tests/                        # Examples
    ├── nrssh_examples/
    │   ├── nrssh_eigenenergies/          # Plots eigenenergies
    │   ├── nrssh_eigenvectors/           # Plots eigenvectors
    │   ├── nrssh_first_moments/          # Plots first states
    │   ├── nrssh_last_moments/           # Plots final states
    │   └── nrssh_phases/                 # Plots phase diagrams
    └── diamond_examples/
        ├── diamond_eigenenergies/        # Plots eigenenergies
        ├── diamond_eigenvectors/         # Plots eigenvectors
        ├── diamond_first_moments/        # Plots first states
        ├── diamond_last_moments/         # Plots final states
        └── diamond_phases/               # Plots phase diagrams
```

## Results

### **NRSSH Findings**

**Phase Behavior Discovery**
- Discovered first-order phase transitions leading to chaotic regimes when gain saturation mediates prominent nonlinearities
- Mapped lasing threshold discontinuities influenced by system parameters

**Temporal Dynamics**
- Revealed irregular chaotic behavior with hyper-sensitivity to initial conditions
- Demonstrated that chaotic phases correspond to oscillating phases

### **Diamond Findings**

**Complex Phase Structure**
- Uncovered additional phase types beyond the NRSSH model, including mixed phases
- Identified exclusive stable phases in face-dimerized systems with higher final times compared to lossy stable regions
- Found that only saturated systems without neighboring-dimerization can enter chaotic phases

**Critical Phase Transitions**
- Documented both 1st-order and 2nd-order phase transitions between stable and chaotic phases
- Discovered non-linear phase transition curves (unlike the linear NRSSH case)
- Identified critical points where phase transition curves gradually shift from 1st-order to 2nd-order behavior

### 🔑 **Key Technical Achievements**

**Temporal Criterion Development**
- Established robust temporal evolution criteria for phase classification
- Validated phase diagram generation methodology across different lattice geometries
- Demonstrated scalability of the approach to complex multi-parameter spaces

**Stability Analysis**
- Successfully prevented unstable phases in systems with non-zero gain saturation and appropriate dimerization
- Characterized conditions where systems reach stable final states versus continuous evolution
- Mapped parameter spaces that avoid optical damage thresholds

**Physical Correspondence**
- Established clear connections between phase behaviors and real laser dynamics
- Demonstrated relevance to semiconductor laser saturation effects and high-power applications
- Confirmed applicability to quantum walks, annealing and topological quantum computing scenarios

These results provide a comprehensive framework for understanding and predicting the behavior of complex topological systems under competing gain and loss effects, with immediate applications in laser design and nonlinear optics research, and potentially in (topological) quantum computing and annealing.

---

📘 Author: [Sid Richards]

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="20" /> LinkedIn: [https://www.linkedin.com/in/sid-richards-21374b30b/]
