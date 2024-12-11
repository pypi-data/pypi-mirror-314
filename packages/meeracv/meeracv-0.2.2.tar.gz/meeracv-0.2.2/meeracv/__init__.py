"""
MeeraCV - A computer vision library inspired by OpenCV
"""

__version__ = '0.2.0'

from .core.image import imread, imwrite, cvtColor
from .core.filters import GaussianBlur, medianBlur, bilateralFilter
from .core.transform import resize, rotate, warpAffine
from .core.features import detectKeypoints, computeDescriptors, matchFeatures
from .core.draw import line, rectangle, circle, putText
from .core.video import VideoCapture, start_webcam
from .core.face import FaceDetector
from .core.ocr import TextRecognizer, DocumentAnalyzer
from .core.vision3d import StereoVision
from .core.gesture import HandGestureRecognizer
from .core.tracking import MultiObjectTracker
from .core.segmentation import ImageSegmentation
from .core.enhancement import ImageEnhancement

# Color conversion constants
COLOR_BGR2GRAY = 0
COLOR_BGR2RGB = 1
COLOR_RGB2BGR = 2
COLOR_BGR2HSV = 3
COLOR_HSV2BGR = 4 