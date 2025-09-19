# Port Scanner

A simple CLI tool that scans a targeted IPv4 address / domain name on a given port.

## Features

- CLI interface with argument parsing
- Scanning a single TCP and/or UDP port
- Target can be either an IPv4 address or a domain name
- Optional verbose log output
- Prints name of the service, if possible

## Usage

Run the scanner script with command line arguments:

```bash
python3 scanner.py -t <target> -p <port> [options]
```

### Required Arguments:
- `-t, --target`: IPv4 address or domain name to scan
- `-p, --port`: Port number to scan (1-65535)

### Optional Arguments:
- `-P, --protocol`: Protocol to scan -> `tcp`, `udp`, or `both` (default: both)
- `-v, --verbose`: Enable verbose log output
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

The scanner can also be imported as a library into Python code

```python
from src.port_scanner import scan_port
# ....
result = scan_port(target, port, "both", 10, logger)
print(f"Scan {target}:{port} -> {result}")
```

## Requirements

This project uses only standard Python libraries (Python 3.10+):
- `socket` - Network communication and port scanning
- `ipaddress` - IP address validation and domain resolution
- `argparse` - Parsing arguments in CLI
- `datetime` - Used to determin runtime
- `logging` - For structured logs
- `sys` - Handling exit

## Development / TODO

- Scanning a port range / multiple ports
- Concurent scanning of multiple ports
- Improve UDP scanning heuristics and ICMP handling
- Testing using PyTest
- Predefined scan profiles
