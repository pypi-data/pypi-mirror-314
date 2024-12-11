# Abhi5511 Hashing Library

This library provides a quantum-resistant hashing mechanism that uses multiple cryptographic techniques like SHA-256, SHA-3, BLAKE2, and AES encryption.

## Features
- Salt generation for added randomness
- Iterative hashing with SHA-256 and SHA-3
- BLAKE2 hashing for extra security
- AES encryption layer for quantum resistance
- High-entropy randomization

## Installation
Clone this repository and use it in your Python project.

## Usage
```python
from abhi5511_hashing import abhi5511_hash

data = "Your input data"
secure_hash = abhi5511_hash(data)
print(secure_hash)
