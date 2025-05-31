# Theoretical Framework

This document provides the mathematical and physical foundations underlying the dynamics of topological photonic systems studied in this project.

## Table of Contents
- [Introduction](#introduction)
- [Lattice Models](#lattice-models)
- [Hamiltonian Construction](#hamiltonian-construction)
- [Gain and Loss Mechanisms](#gain-and-loss-mechanisms)
- [Time Evolution](#time-evolution)
- [Phase Classification](#phase-classification)
- [Topological Properties](#topological-properties)
- [Physical Interpretation](#physical-interpretation)
- [References](#references)

## Introduction

Topological photonics combines the robust properties of topological insulators with the rich physics of optical systems.
This project focuses on the behaviour of:

- **Topological protection**: Edge states immune to disorder.
- **Non-Hermitian dynamics**: Systems with imaginary gain and loss terms.
- **Nonlinear gain saturation**: Amplification mechanism dependent on site-intensity.
- **Phases**: Competition between these effects leads regions of stable lasing, chaotic dynamics, and topologically protected modes.

## Lattice Models

### Non-Reciprocal SSH (NRSSH) Model

The classic Su-Schrieffer-Heeger (SSH) model is adapted by introducing hoppings:

- **Intra-cell hoppings**: $v$ and $u$, where $u \neq v$
- **Inter-cell hopping**: $r$
- **Onsite potential**: $\epsilon$

**NRSSH Hamiltonian:**

Hamiltonians are constructed by populating matrix entry $[i, j]$ with the hopping strength **from site $j$ to site $i$**:

$H = \Sigma_i (v|2i⟩⟨2i+1| + u|2i+1⟩⟨2i| + r(|2i+1⟩⟨2i+2| + |2i+2⟩⟨2i+1|))$

### Diamond (Rhombic) Model

- **Intra-cell A-B hopping**: $t_1$
- **Intra-cell A-C hopping**: $t_2$
- **Inter-cell A-B hopping**: $t_3$
- **Inter-cell A-C hopping**: $t_4$

**Diamond Hamiltonian:**

$H = \Sigma_i(t_1(|3i⟩⟨3i+1| + |3i+1⟩⟨3i|) + t_2(|3i⟩⟨3i+2| + |3i+2⟩⟨3i|) + t_3(|3i+1⟩⟨3i+3| + |3i+3⟩⟨3i+1|) + t_4(|3i+2⟩⟨3i+3| + |3i+3⟩⟨3i+2|))$

**Dimerizations:**
- Facing: $t_1=t_4$ and $t_2=t_3$
- Neighbouring: $t_1=t_3$ and $t_2=t_4$
- Intra $\neq$ inter: $t_1=t_2$ and $t_3=t_4$

**Physical Significance:**
- More complicated band structure than the NRSSH's
- Multiple topological phases exist
- Richer phase transition behavior

## Gain and Loss Mechanisms

### Nonlinear Saturable Gain (NSG) and Contant Loss

- **$\gamma_1 \in (0,1]$**: Gain parameter
- **$\gamma_2 \in (0,1]$**: Loss parameter
- **$S \geq 0$**: Saturation parameter

The NSG term is:

$i\gamma_1 / (1 + S|\varphi|^2)$

where $\varphi$ is the site's amplitude.

### Site-Specific Assignment

**NRSSH Model**: All sites have both gain and loss.
**Diamond Model**: NSG on the A sites. Constant loss $\gamma_2$ on the B and C sites.

## Time-Evolution Operator

### Derivation

We set $\hbar=1$.
The Schrödinger equation $i∂_t\varphi = H\varphi$ can be combined with the definition of the time-derivative $∂_t\varphi = (\varphi(t + dt) - \varphi(t)) / dt$ to derive the 1st-order time-evolution operator:

$U(t) = I - idtH(t)$.

But this operator is not unitary even if $H$ is Hermitian. So we upgrade this to the 2nd-order by considering $\pm dt / 2$:

$\varphi(t + dt/2) = (I - idtH / 2)\varphi(t)$

and

$\varphi(t + dt/2) = (I + idtH / 2)\varphi(t + dt)$

we derive the unitary 2nd-order time-evolution operator:

$U(t) = (I - idtH / 2) / (I + idtH / 2)$.

A final state is determined by when the difference in total intensities between successive time-increments dt drops below a certain "tolerance" parameter.

## Phase Classification

**Lossy Phase**:
- The system is dominated by loss
- Intensities diminish and energy dissipates

**Stable Phase**:
- Intensities converge smoothly between points in the diagram
- Can host edge modes and skin-effects
- Diamond models can have stable regions with relatively high final times

**Unstable Phase**:
- NSG dominates and intensities grow indefinitely
- Realistically would lead to optical damage

**Chaotic Phase**:
- Irregular times to reach final states
- Extreme sensitivity to initial parameters

**Blended Phase**:
- Neighbouring points are chaotic, stable or lossy
- 2nd-order (continuous) phase transitions between neighbouring phases

### Phase Boundaries

**1st-Order Transitions**: Discontinuous jumps in final times.
**2nd-Order Transitions**: Continuous / smooth changes.
**Critical Points**: Where transitions change from the 1st to 2nd-order.

### Laser Realisation

**Gain Saturation**: Prominent in laser gain media, and could parameterise high signal inputs because a medium's available energy is finite.
**Loss Mechanisms**: General energy dissipation and other lossy effects such as scattering.
**Lossy Phase**: No lasing achived and the system is below the lasing threshold.
**Stable Phase**: Regular laser behaviour, steady output and NSG/loss balance.
**Unstable Phase**: Leads to optical damage.
**Chaotic Phase**: Output flickers unpredictably, can be used to make short-pulsed lasers.
**Blended Phase**: For spatially-incoherent lasing - some sites want to laser and others don't.

### Quantum Computing Applications

**Quantum Annealing**: Phase diagrams map computational complexity landscapes when sites represent qubits.
**Decoherence Modeling**: Loss parameters represent environmental noise, decoherence and errors.

---
