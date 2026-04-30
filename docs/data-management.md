# Data Management

## Dataset

The research uses MNIST digits 0 and 1. The notebook downloads MNIST through
TensorFlow/Keras and balances the binary classes for fair comparison.

## Storage Policy

The repository does not commit raw or processed dataset files. This keeps the
repository small and avoids ambiguity about dataset redistribution.

## Derived Data

If derived arrays are saved, record:

- Source dataset and version
- Filtered classes
- Normalization range
- Class balancing method
- Random seed
- Script or notebook cell used to create the data

Place local derived files in `data/processed/`.
