# MeeraCV

A lightweight, pure Python computer vision library built from scratch with zero external dependencies.

## Features

- **Pure Python Implementation**: No external dependencies required
- **Educational**: Clear, well-documented code for learning computer vision concepts
- **Customizable**: Easy to modify and extend for your specific needs

## Core Modules

### Image Processing
- Custom image format handling (BMP support)
- Basic image operations (read, write, color conversion)
- Pixel-level manipulation
- Convolution operations

### Filters
- Gaussian blur
- Median blur
- Bilateral filter
- Sobel edge detection
- Canny edge detection

### OCR (Optical Character Recognition)
- Custom character recognition engine
- Template-based matching
- Document structure analysis
- Text region detection

### Face Detection
- Custom face detection algorithm
- Facial feature extraction
- Basic face recognition capabilities

### Video Processing
- Basic video capture
- Frame extraction
- Video file handling
- Real-time processing support

### 3D Vision
- Custom stereo vision implementation
- Depth perception algorithms
- 3D reconstruction capabilities

### Gesture Recognition
- Hand landmark detection
- Gesture classification
- Real-time tracking

## Installation

```bash
pip install meeracv
```

## Quick Start

```python
import meeracv as mcv

# Load and process an image
img = mcv.Image.from_file('input.jpg')
gray = img.to_grayscale()

# Apply Gaussian blur
kernel = mcv.gaussian_kernel(5, 1.4)
blurred = gray.apply_kernel(kernel)

# Save the result
blurred.save('output.jpg')
```

## Advanced Examples

### Text Recognition
```python
from meeracv import TextRecognizer

# Initialize recognizer
recognizer = TextRecognizer()

# Load image and extract text
img = mcv.Image.from_file('document.jpg')
text = recognizer.extract_text(img)
print(f"Extracted text: {text}")
```

### Face Detection
```python
from meeracv import FaceDetector

# Initialize detector
detector = FaceDetector()

# Load image and detect faces
img = mcv.Image.from_file('people.jpg')
faces = detector.detect_faces(img)

# Process detected faces
for face in faces:
    print(f"Found face at: {face}")
```

### Video Processing
```python
from meeracv import VideoCapture

# Start video capture
cap = VideoCapture()

# Process frames
while True:
    frame = cap.read()
    if frame is None:
        break
    
    # Process frame here
    processed = frame.to_grayscale()
    
    # Display or save the processed frame
    processed.save('output.jpg')
```

## Performance Considerations

Since MeeraCV is implemented in pure Python without external dependencies:
- Operations may be slower compared to optimized libraries like OpenCV
- Memory usage might be higher for large images
- Best suited for learning and prototyping
- Consider using PyPy for better performance

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 