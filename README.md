# Hybrid Quantum–Classical GANs (HQCGAN) Research

## Overview
This repository contains the research work and implementation for **"Quantum-Enhanced Generative Adversarial Networks: Comparative Analysis of Classical and Hybrid Quantum–Classical Generative Adversarial Networks"**. The study explores how quantum computing can enhance generative modelling by integrating parameterised quantum circuits into GAN architectures.

We evaluate multiple HQCGAN configurations alongside a baseline classical GAN, focusing on image generation performance for binary MNIST digits (0 and 1).

---

## Key Features
- **Classical GAN** baseline for direct performance comparison.
- **Quantum Generator** implemented using **Qiskit** parameterised quantum circuits.
- Multiple HQCGAN variants with **3, 5, and 7 qubits**.
- Realistic **noise models** for near-term quantum device simulation.
- Training and evaluation on **binary MNIST dataset**.
- Quantitative evaluation using:
  - Fréchet Inception Distance (FID)
  - Kernel Inception Distance (KID)

---

## Methodology
1. **Data Preparation**
   - Binary subset of MNIST dataset containing digits **0** and **1**.
   - Normalisation and reshaping for GAN training.

2. **Model Architectures**
   - **Classical GAN**: Fully-connected generator and discriminator.
   - **HQCGAN**: Quantum generator + classical discriminator.
   - Quantum circuits parameterised with trainable weights.

3. **Training**
   - Trained for **150 epochs** with **Adam optimiser**.
   - Learning rate = `0.0002`, β₁ = `0.5`, batch size = `64`.

4. **Evaluation**
   - FID and KID metrics to assess image fidelity and diversity.

---

## Results Summary
- HQCGAN variants with **5 qubits** showed the most promising improvement over classical GANs.
- Performance varied with qubit count; higher qubit numbers increased representational capacity but also training instability.
- Quantum-enhanced models exhibited competitive FID/KID scores under realistic noise conditions.

---

## Tech Stack
- **Python 3**
- **Qiskit**
- **TensorFlow / Keras**
- **NumPy**, **Pandas**
- **Matplotlib**, **Seaborn**
