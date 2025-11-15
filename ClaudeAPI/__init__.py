# claude_api/__init__.py

"""
Public interface for the claude_api package.

This module exposes a minimal, clean API surface so that other parts
of the application can interact with Claude through simple functions
without needing to know the internal structure of the package.
"""

from .client import ask_raw

__all__ = ["ask_raw"]