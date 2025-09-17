#!/usr/bin/env python3
"""
Port Scanner Entry Point

Simple entry point script for the port scanner tool.
"""
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main CLI
from src.port_scanner.cli import main

if __name__ == "__main__":
    main()
