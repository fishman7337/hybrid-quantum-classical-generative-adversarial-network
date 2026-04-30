# Research Context

## Academic Context

This research was completed under Singapore Polytechnic, School of Computing,
Diploma in Applied AI and Analytics, for the Deep Learning module `ST1504`,
CA2 Part C, AY25/26 Year 2 Semester 1.

Author: Goh Kun Ming, DAAA student,
https://orcid.org/0009-0008-7666-781X

Supervising lecturer: Lecturer Gerald Chua Deng Xiang

## Research Question

The study investigates whether noisy parameterised quantum circuits can act as
latent priors for GANs and produce competitive image generation quality under
near-term quantum constraints.

## Experimental Scope

- Dataset: binary MNIST digits 0 and 1.
- Baseline: classical GAN with Gaussian latent noise.
- Quantum variants: HQCGANs using 3, 5, and 7 qubits.
- Simulator: Qiskit AerSimulator with realistic noise models.
- Metrics: Frechet Inception Distance (FID) and Kernel Inception Distance
  (KID).
- Training horizon reported in the paper: 150 epochs.

## Paper Versions

The school-submission paper package and the arXiv paper package are both kept
under `papers/`. The school submission documents the module assessment context,
while the arXiv source corresponds to the public research paper
`arXiv:2508.09209`.
