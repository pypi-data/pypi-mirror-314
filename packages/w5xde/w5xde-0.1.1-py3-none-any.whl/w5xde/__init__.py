"""
W5xDE: A Python package for distributed machine learning.
"""

__version__ = "0.1.1"
__author__ = "Mikus Sturmanis, Jordan Legg"
__email__ = "ilovevisualstudiocode@gmail.com"

from .w5xde import CentralServer, TrainingNode

__all__ = [
    'CentralServer',
    'TrainingNode'
]