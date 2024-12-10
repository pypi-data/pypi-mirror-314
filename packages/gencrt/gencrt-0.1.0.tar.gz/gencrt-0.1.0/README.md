# gencrt

**`gencrt`** is a Python library that implements the **Generalized Chinese Remainder Theorem (CRT)** algorithm. It enables solving systems of modular equations efficiently and robustly, making it a valuable tool for applications in number theory, cryptography, and computational mathematics.

## Features

- Solve modular equations using the **generalized CRT** algorithm.
- Support for multiple congruences of the form `x ≡ a_i (mod n_i)`.
- Includes utility functions for:
  - Extended Euclidean Algorithm to compute the greatest common divisor (GCD) and Bézout coefficients.
  - Validation of moduli and congruences for correctness.

## Installation

To use `gencrt` in your project, you can install it via pip:

```bash
pip install gencrt
```

## Usage

### Importing the Library

```python
from gencrt import crt, extended_gcd
```

### Solving Modular Equations with generalized CRT
To solve a system of modular equations:
```
x ≡ a1 (mod n1)
x ≡ a2 (mod n2)
x ≡ a3 (mod n3)
```

```python
from gencrt import crt

# Define the congruences as a list of (a_i, n_i)
congruences = [(2, 3), (3, 4), (1, 5)]

# Solve using the generalized CRT
solution = crt(congruences)

print(f"The solution is x ≡ {solution} (mod product of moduli)")
```

### Extended Euclidean Algorithm
Compute the GCD and Bézout coefficients:

```python
from gencrt import extended_gcd

a, b = 56, 15
gcd, x, y = extended_gcd(a, b)

print(f"GCD: {gcd}, x: {x}, y: {y} (Bézout coefficients)")
```

## API Reference

### `crt(congruences: Iterable)`
- **Description**: Solves a system of modular equations using the generalized CRT.
- **Parameters**:
  - `congruences`: An iterable of tuples `(a_i, n_i)`.
- **Returns**: Integer solution ` x ` modulo the product of moduli, or `None` if no solution exists.

### `extended_gcd(a: int, b: int)`
- **Description**: Computes the GCD of two integers and Bézout coefficients.
- **Parameters**:
  - `a, b`: Integers.
- **Returns**: A tuple `(GCD, x, y)`.

## License

This library is licensed under the MIT License. See [LICENSE](LICENSE) for more details.

---

**Author**: Simon Ljungbeck
**Date**: December 2024

For issues or contributions, visit the [GitHub repository](https://github.com/SimonLjungbeck/gencrt).
