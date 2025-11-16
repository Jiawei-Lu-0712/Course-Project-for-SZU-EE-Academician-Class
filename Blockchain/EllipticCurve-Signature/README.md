# EllipticCurve-Signature

A lightweight educational implementation of **Elliptic Curve Cryptography (ECC)**, including finite field arithmetic, elliptic curve point operations, scalar multiplication, and a simplified digital signature scheme.

This project is designed for **learning and demonstration**, *not for production cryptographic use*.

## Project Structure

```
EllipticCurve-Signature/
│
├── FieldElement.py            # Finite field arithmetic
├── EllipticCurves.py          # Elliptic curve point operations & signatures
├── EllipticCurveswindow.py    # Simple demo window (if applicable)
├── TestReptiles.py            # Test script 1
├── TestReptiles_1.py          # Test script 2
└── README.md                  # Documentation
```

## Features

### **1. Finite Field Implementation**

* Arithmetic mod prime ( p )
* Supports:

  * **Addition**
  * **Subtraction**
  * **Multiplication**
  * **Modular inverse**
  * **Equality checks**

### **2. Elliptic Curve Arithmetic**

Implements points on curves of the form:

[
y^2 = x^3 + ax + b
]

Supports:

* **Point addition**
* **Point doubling**
* **Scalar multiplication**
* **Infinity point** handling

### **3. Hashing**

* Uses **SHA-256** for generating message digests.

### **4. Digital Signatures**

Simplified ECDSA-like functionality:

* **Generate keypair**
* **Sign message**
* **Verify signature**

## Getting Started

### **Prerequisites**

* Python **3.7+**
* No external dependencies required

### **Run Tests**

```bash
python TestReptiles.py
python TestReptiles_1.py
```

## Example Usage

### **Finite Field**

```python
from FieldElement import FieldElemet

a = FieldElemet(17, 223)
b = FieldElemet(64, 223)

print(a + b)
print(a * b)
```

### **Elliptic Curve Point**

```python
from FieldElement import FieldElemet
from EllipticCurves import EllipticPoint

a = FieldElemet(0, 223)
b = FieldElemet(7, 223)
x = FieldElemet(47, 223)
y = FieldElemet(71, 223)

P = EllipticPoint(x, y, a, b)
print(2 * P)
```

### **Signature Demo**

```python
from EllipticCurves import generate_keypair, sign, verify

priv, pub = generate_keypair()
msg = b"Hello ECC"
sig = sign(priv, msg)

print("Valid:", verify(pub, msg, sig))
```

## Testing

Run all test scripts:

```bash
python TestReptiles.py
python TestReptiles_1.py
```

Tests include:

* Field arithmetic validation
* Point addition & multiplication
* Curve behavior testing
* Signature correctness

## Disclaimer

This project is for **educational purposes only**
and should **not** be used for real-world cryptographic or security applications.

