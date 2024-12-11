"""
MeeraCV - A computer vision library inspired by OpenCV
"""

__version__ = '0.1.0'

from .core.image import imread, imwrite, cvtColor
from .core.filters import GaussianBlur, medianBlur, bilateralFilter
from .core.transforms import resize, rotate, warpAffine
from .core.features import detectKeypoints, computeDescriptors, matchFeatures
from .core.draw import line, rectangle, circle, putText

# Color conversion constants
COLOR_BGR2GRAY = 0
COLOR_BGR2RGB = 1
COLOR_RGB2BGR = 2
COLOR_BGR2HSV = 3
COLOR_HSV2BGR = 4 