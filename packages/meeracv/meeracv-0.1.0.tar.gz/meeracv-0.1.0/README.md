# MeeraCV

MeeraCV is a computer vision library inspired by OpenCV, designed to provide essential image processing and computer vision functionality.

## Features

- Image I/O operations
- Basic image processing (filters, transformations)
- Color space conversions
- Edge detection
- Contour detection
- Feature detection and matching
- Image segmentation

## Installation

```bash
pip install meeracv
```

## Quick Start

```python
import meeracv as mcv

# Read an image
img = mcv.imread('image.jpg')

# Convert to grayscale
gray = mcv.cvtColor(img, mcv.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = mcv.GaussianBlur(gray, kernel_size=(5,5), sigma=1.0)

# Save the result
mcv.imwrite('result.jpg', blurred)
```

## Requirements

- Python 3.7+
- NumPy
- Pillow
- SciPy

## License

This project is licensed under the MIT License - see the LICENSE file for details. 