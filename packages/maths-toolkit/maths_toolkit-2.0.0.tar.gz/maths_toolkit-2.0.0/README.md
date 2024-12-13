# Maths Toolkit
# Author : N V R K SAI KAMESH SHARMA
---
Maths Toolkit is a Python library designed to simplify intermediate-level mathematics calculations for both Maths A (Algebra) and Maths B (Trigonometry, Calculus, and more). It provides easy-to-use functions for common operations, making it ideal for students, educators, and developers.

## Features

### Algebra (Maths A)
- Solve quadratic equations.
- Matrix operations (addition, multiplication, transpose).

### Trigonometry (Maths B)
- Sine, cosine, and other trigonometric functions (in degrees).

### Calculus (Maths B)
- Differentiate polynomials.
- Integrate polynomials.

### Statistics
- Calculate mean, variance, and standard deviation.

## Installation

Install Maths Toolkit using pip:

```bash
pip install maths-toolkit
```

## Usage

Here's how to use Maths Toolkit:

### Example: Solving Quadratic Equations
```python
from maths_toolkit import MathsToolkit

# Solve x^2 - 5x + 6 = 0
roots = MathsToolkit.solve_quadratic(1, -5, 6)
print("Roots:", roots)
```

### Example: Trigonometry
```python
# Calculate sin(30 degrees)
sine = MathsToolkit.sin_deg(30)
print("Sin 30°:", sine)
```

### Example: Calculus
```python
# Differentiate 3x^2 + 2x + 1
derivative = MathsToolkit.differentiate([3, 2, 1])
print("Derivative:", derivative)

# Integrate 3x^2 + 2x + 1
integral = MathsToolkit.integrate([3, 2, 1])
print("Integral:", integral)
```

### Example: Statistics
```python
# Data set
data = [1, 2, 3, 4, 5]

# Calculate mean, variance, and standard deviation
mean = MathsToolkit.mean(data)
variance = MathsToolkit.variance(data)
std_dev = MathsToolkit.standard_deviation(data)

print("Mean:", mean)
print("Variance:", variance)
print("Standard Deviation:", std_dev)
```

### Example: Matrix Operations
```python
# Matrices
a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]

# Matrix addition
addition = MathsToolkit.matrix_add(a, b)
print("Matrix Addition:", addition)

# Matrix multiplication
multiplication = MathsToolkit.matrix_multiply(a, b)
print("Matrix Multiplication:", multiplication)

# Matrix transpose
transpose = MathsToolkit.matrix_transpose(a)
print("Matrix Transpose:", transpose)
```

## Future Plans
- Expand support for advanced calculus.
- Include graphical visualizations.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

N V R K Sai Kamesh Sharma

For questions or feedback, feel free to reach out at [your-email@example.com].

