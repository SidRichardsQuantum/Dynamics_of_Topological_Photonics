# Theoretical Framework

This document provides the mathematical and physical foundations underlying the dynamics of topological photonic systems studied in this project.

## Table of Contents
- [Introduction](#introduction)
- [Lattice Models](#lattice-models)
- [Gain and Loss Mechanisms](#gain-and-loss-mechanisms)
- [Time-Evolution Operator](#time-evolution-operator)
- [Eigenvalues and Eigenvectors](#eigenvalues-and-eigenvectors)
- [Phase Classification](#phase-classification)
- [Phase Boundaries](#phase-boundaries)
- [Realisations](#realisations)

## Introduction

Topological photonics combines the robust properties of topological insulators with the rich physics of optical systems.
This project focuses on the behaviour of:

- **Topological protection**: Edge states immune to disorder.
- **Non-Hermitian dynamics**: Systems with imaginary gain and loss terms.
- **Nonlinear gain saturation**: Amplification mechanism dependent on site-intensity.
- **Phases**: Competition between these effects leads regions of stable lasing, chaotic dynamics, and topologically protected modes.

## Lattice Models

1. ### Non-Reciprocal SSH (NRSSH) Model

The classic Su-Schrieffer-Heeger (SSH) model is adapted by introducing hoppings:

- **Intra-cell hoppings**: $v$ and $u$, where $u \neq v$
- **Inter-cell hopping**: $r$
- **Onsite potential**: $\epsilon$

(Setting $v=u$ reduces the system to the SSH Model, and similarly $v=u=r$ forms the trivial tight-binding model.)

![NRSSH Model](images/NRSSH%20Model.png)

#### **NRSSH Hamiltonian:**

Hamiltonians are constructed by populating matrix entry $[i, j]$ with the hopping strength **from site $j$ to site $i$**:

$H = \Sigma_i (v|2i⟩⟨2i+1| + u|2i+1⟩⟨2i| + r(|2i+1⟩⟨2i+2| + |2i+2⟩⟨2i+1|)) + \epsilon I$

2. ### Diamond (Rhombic) Model

- **Intra-cell A-B hopping**: $t_1$
- **Intra-cell A-C hopping**: $t_2$
- **Inter-cell A-B hopping**: $t_3$
- **Inter-cell A-C hopping**: $t_4$
- **Onsite potential**: $\epsilon$

![Diamond Model](images/Diamond%20Model.png)

#### **Dimerizations:**
- Facing: $t_1=t_4$ and $t_2=t_3$
- Neighbouring: $t_1=t_3$ and $t_2=t_4$
- Intra $\neq$ inter: $t_1=t_2$ and $t_3=t_4$

#### **Diamond Hamiltonian:**

$H = \Sigma_i(t_1(|3i⟩⟨3i+1| + |3i+1⟩⟨3i|) + t_2(|3i⟩⟨3i+2| + |3i+2⟩⟨3i|) + t_3(|3i+1⟩⟨3i+3| + |3i+3⟩⟨3i+1|) + t_4(|3i+2⟩⟨3i+3| + |3i+3⟩⟨3i+2|)) + \epsilon I$

## Gain and Loss Mechanisms

### Nonlinear Saturable Gain (NSG) and Contant Loss:

- **$\gamma_1 \in (0,1]$**: Gain parameter
- **$\gamma_2 \in (0,1]$**: Loss parameter
- **$S \geq 0$**: Saturation parameter

The NSG term is $i\gamma_1 / (1 + S|\varphi_m|^2)$, where $|\varphi_m|^2$ is site m's intensity.

**NRSSH Model**: All sites have both gain and loss.

**Diamond Model**: NSG on the A sites. Constant loss $\gamma_2$ on the B and C sites.

## Time-Evolution Operator

We use "natural units" and set $\hbar = 1$.
This is what quantum physicists use (along with setting the speed of light $c = 1$) to avoid writing constants and make the maths easier.
(Natural units allows us to refer to the $k$-space, where $p=\hbar k$ is the wave number, as the "momentum-space".)
Computationally, using natural units benefits us; because omitting $\hbar \approx 10^{-34}$, makes our chosen values for $dt$ extremely smaller when physically-realized.
Therefore, we can set $dt$ to float values that "look big", such as $0.1$.

### Derivation

The Schrödinger equation $i d\varphi / dt = H \varphi$ can be combined with the definition of the time-derivative $d\varphi / dt = (\varphi(t + dt) - \varphi(t)) / dt$ to derive the 1st-order time-evolution operator:

$U(t) = I - i dt H(t)$.

But this operator is **not** unitary even if $H$ is Hermitian.
So we upgrade this to the 2nd-order by considering $\pm dt / 2$:

$\varphi(t + dt/2) = (I - idtH / 2)\varphi(t)$

and

$\varphi(t + dt/2) = (I + idtH / 2)\varphi(t + dt)$

we derive the unitary 2nd-order time-evolution operator:

$U(t) = (I - idtH / 2)(I + idtH / 2)^{-1}$.

A final state is determined by when the difference in total intensities between successive time-increments $dt$ drops below a certain "tolerance" parameter.

## Eigenvalues and Eigenvectors

Eigenvalues of the Hamiltonian (eigenenergies), when plotted in $k$-space, form the band structure for the lattice.
In some phases, there is a gap in the bands such that particles require excitation to jump across the gap.
Insulators have large band gaps that electrons can't easily jump across.
Metals have no band gap, so electrons can freely move between the eigenenergy states.

Other phases host localised edge states, which have eigenenergies within the band gap; where the ends of the lattice are highly conducting and the bulk is insulating - forming a **topological insulator**.

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

## Phase Boundaries

**1st-Order Transitions**: Discontinuous jumps in final times.
**2nd-Order Transitions**: Continuous / smooth changes.
**Critical Points**: Where transitions change from the 1st to 2nd-order.

## Realisations

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

📘 Author: [Sid Richards]

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="20" /> LinkedIn: [https://www.linkedin.com/in/sid-richards-21374b30b/]
