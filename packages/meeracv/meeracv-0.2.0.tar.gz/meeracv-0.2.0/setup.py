from setuptools import setup, find_packages

setup(
    name="meeracv",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "pillow>=8.0.0",
        "scipy>=1.6.0",
        "opencv-python-headless>=4.5.0",
        "face-recognition>=1.3.0",
        "pytesseract>=0.3.8",
        "mediapipe>=0.8.0",
        "scikit-learn>=0.24.0",
    ],
    author="Kashyapsinh Gohil",
    description="A computer vision library inspired by OpenCV",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KashyapSinh-Gohil/meeracv",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 