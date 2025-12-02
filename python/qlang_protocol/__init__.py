"""
Q-Lang Protocol: Quantized Language for Edge AI Communication

A high-performance, context-aware communication protocol for Edge AI devices.
"""

__version__ = "0.1.0"
__author__ = "Q-Lang Team"
__license__ = "MIT OR Apache-2.0"

# Import core classes for easy access
from .instruction import QLangInstruction, QLangMetadata
from .response import QLangResponse, QLangBatch, QLangBatchResponse

__all__ = [
    "QLangInstruction",
    "QLangMetadata",
    "QLangResponse",
    "QLangBatch",
    "QLangBatchResponse",
]
