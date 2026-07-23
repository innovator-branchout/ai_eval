"""
AI Evaluation System - Backend Scripts Package

This package contains all the necessary scripts for:
- Data processing and embedding computation
- Model training and evaluation
- Prediction and classification
- Analysis and reporting
"""

__version__ = "1.0.0"
__author__ = "Sumer Chaudhary"

# Import core components (avoid importing training/prediction modules at package import time)
from .database import *
from .dataset import *
from .embeddings import *
