"""
Port Scanner Package

A simple network port scanner that can scan single ports on target IP addresses or domain names.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .cli import main
from .core.scanner import scan_port
from .core.utils import is_ip, resolve_domain, validate_port

__all__ = [
    "main",
    "scan_port", 
    "is_ip",
    "resolve_domain",
    "validate_port"
]
