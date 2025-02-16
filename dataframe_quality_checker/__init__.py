"""Schema-driven pandas quality checks; never mutates the input DataFrame."""
__version__ = "1.0.0"
from .schema import Schema
from .validator import validate

__all__ = ['Schema','validate','__version__']
