# Port Scanner

A small educational port-scanning tool written in Python. It can scan a single TCP and/or UDP port on an IPv4 address or a resolved domain name. The project is a work-in-progress.

## Features

- Command-line interface with comprehensive argument parsing
- TCP and UDP single-port scanning capabilities
- Support for both IP addresses and domain name resolution
- Configurable scan protocols (TCP, UDP, or both)
- Adjustable timeout settings for scan operations
- Verbose logging mode for detailed scan information
- Retrieves common service names for open ports using the system service database
- Small, dependency-free codebase (standard library only)

## Usage

Run the scanner script with command-line arguments:

```bash
python3 scanner.py -t <target> -p <port> [options]
```

### Required Arguments:
- `-t, --target`: IPv4 address or domain name to scan
- `-p, --port`: Port number to scan (1-65535)

### Optional Arguments:
- `-P, --protocol`: Protocol to scan - `tcp`, `udp`, or `both` (default: both)
- `-v, --verbose`: Enable verbose output with debug information
- `-T, --timeout`: Timeout in seconds for each port scan (default: 10)

### Examples:

```bash
# Basic scan of port 80 on a target
python3 scanner.py -t example.com -p 80

# TCP-only scan with verbose output
python3 scanner.py -t 192.168.1.1 -p 22 -P tcp -v

# UDP scan with custom timeout
python3 scanner.py -t 10.0.0.1 -p 53 -P udp -T 5

# Scan both protocols with verbose logging
python3 scanner.py -t google.com -p 443 -P both -v -T 15
```

You can also import the scanner module to other Python projects:

```python
from src.port_scanner import scan_port
# ....
result = scan_port(target, port, "both", 10, logger)
print(f"Scan {target}:{port} -> {result}")
```

## Requirements

No external packages are required. If any third-party dependencies are added, they will be listed in `requirements.txt`.

This project uses only Python standard-library modules (tested on Python 3.10+):
- `socket` - Network communication and port scanning
- `ipaddress` - IP address validation and parsing
- `argparse` - Command-line argument parsing
- `datetime` - Timestamp generation and scan duration tracking
- `logging` - Structured output and debug information
- `sys` - System-specific parameters and exit handling

## Development / TODO

- Add support for scanning port ranges and concurrency to speed up scans
- Improve UDP scanning heuristics and ICMP handling
- Add unit tests and example usage
- Implement configuration file support for common scan profiles
- Add output formatting options (JSON, CSV, XML)
- Implement basic stealth scanning techniques