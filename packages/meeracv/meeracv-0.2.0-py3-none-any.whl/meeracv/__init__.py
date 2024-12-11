"""
MeeraCV - A computer vision library inspired by OpenCV
"""

__version__ = '0.1.0'

from .core.image import imread, imwrite, cvtColor
from .core.filters import GaussianBlur, medianBlur, bilateralFilter
from .core.transforms import resize, rotate, warpAffine
from .core.features import detectKeypoints, computeDescriptors, matchFeatures
from .core.draw import line, rectangle, circle, putText
from .core.video import start_webcam, read_video_file, write_video, extract_frames
from .core.face import FaceDetector
from .core.ocr import TextRecognizer, DocumentAnalyzer
from .core.vision3d import StereoVision, StructureFromMotion, DepthCamera, PointCloudProcessor
from .core.gesture import HandGestureRecognizer, PoseEstimator, GestureController
from .core.tracking import ObjectTracker, DeepObjectTracker, MultiObjectTrackingSystem

# Color conversion constants
COLOR_BGR2GRAY = 0
COLOR_BGR2RGB = 1
COLOR_RGB2BGR = 2
COLOR_BGR2HSV = 3
COLOR_HSV2BGR = 4 