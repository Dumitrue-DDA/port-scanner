import sys
import argparse

from datetime import datetime
from .core.scanner import scan_port
from .core.utils import is_ip, resolve_domain, setup_logging, validate_port
from .config.settings import DEFAULT_TIMEOUT, DEFAULT_PROTOCOL, MIN_PORT, MAX_PORT

"""
-- Port Scanner Tool --
A simple network port scanner that can scan single ports or port ranges
on target IP addresses or domain names.
"""


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="port-scanner",
        description="Port Scanner Tool\n" \
        "Used to check unwanted open ports.",
        epilog="Example: port-scanner -t 0.0.0.0 -p 22 -P both -T 30 --verbose"
    )
    parser.add_argument(
        "-t", "--target", 
        required=True, type=str, 
        help="Set the target IPv4 address or domain name"
    )
    parser.add_argument(
        "-p", "--port", type=int, 
        help=f"Set the port number to scan ({MIN_PORT}-{MAX_PORT})"
    )
    parser.add_argument(
        "-P", "--protocol", choices=['tcp', 'udp', 'both'], 
        default=DEFAULT_PROTOCOL,
        help=f"Set the protocol to scan (default: {DEFAULT_PROTOCOL})"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", 
        help="Enable verbose output"
    )
    """ 
    # NOT IMPLEMENTED YET
    parser.add_argument(
        "-r", "--range", nargs=2, type=int, 
        metavar=('START', 'END'),
        help="Range of ports to scan (1-65535)"
    )    
    """
    parser.add_argument(
        "-T", "--timeout", type=int, 
        default=DEFAULT_TIMEOUT,
        help=f"Set timeout (in seconds) for each port scan (default: {DEFAULT_TIMEOUT})"
    )

    return parser


# -- Main --

def main():
    parser = parse_arguments()
    args = parser.parse_args()

    logger = setup_logging(args.verbose)
    
    start_time = datetime.now()

    # Check if the target ip/domain is valid
    target = args.target
    try:
        if not is_ip(target):
            resolved_ip = resolve_domain(target)
            logger.debug(f"✓ Resolved domain {target} -> {resolved_ip}")
            target = resolved_ip
        else:
            logger.debug(f"✓ Valid IP address: {target}")
    except Exception as e:
        logger.error(f"Invalid target! {e}")
        sys.exit(1)

    # Check if the port is valid
    port = args.port
    try:
        if not validate_port(port):
            raise Exception(f"Port {port} is outside valid range.\n"
                f"Please enter a port between {MIN_PORT} and {MAX_PORT}.")
        logger.debug("Port is valid")
    except Exception as e:
        logger.error(f"Invalid port! {e}")
        sys.exit(1)

    # Start the scan
    if not target:
        logger.error("No target set")
        sys.exit(1)

    if not port:
        logger.error("No port set")
        sys.exit(1)

    protocol = args.protocol
    timeout = args.timeout

    try:
        status = scan_port(target, port, protocol, timeout, logger)
    except Exception as e:
        logger.error(f"Exception caught during port scan!\n")
        status = f" FAILED! {e}"
        sys.exit(1)

    logger.info(f"\nScan completed!")
    logger.info(f"Status: {status}")
    logger.debug(f"Scan duration: {str(datetime.now() - start_time).split('.')[0]} (HH:MM:SS)")
    sys.exit(0)


if __name__ == "__main__":
    main()