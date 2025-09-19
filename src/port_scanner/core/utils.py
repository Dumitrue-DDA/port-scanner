"""
Utility functions for the port scanner.
"""
import socket
import ipaddress
import logging
from ..config.settings import MIN_PORT, MAX_PORT, LOG_FORMAT, LOG_DATE_FORMAT

def is_ip(address: str) -> bool:
    """
    Check if a given string is a valid IP address.
    
    Args:
        address (str): The address to validate
        
    Returns:
        bool: True if valid IP address, False otherwise
    """
    try:
        ipaddress.ip_address(address)
        return True
    except Exception:
        return False


def resolve_domain(domain: str) -> str:
    """
    Resolve a domain name to its IP address.
    
    Args:
        domain (str): The domain name to resolve
        
    Returns:
        str: The resolved IP address
        
    Raises:
        RuntimeError: If domain cannot be resolved
    """
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        raise RuntimeError("Couldn't resolve domain name")


def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        verbose (bool): Enable debug logging if True
        
    Returns:
        logging.Logger: Configured logger instance
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, 
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT
    )
    return logging.getLogger()


def validate_port(port: int) -> bool:
    """
    Validate if a port number is within valid range.
    
    Args:
        port (int): Port number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return MIN_PORT <= port <= MAX_PORT

# interpeting ICMP codes

# contains all messages to ensure proper handling
# we'll only get 3, 11 or 12 codes
ICMP_MESSAGE = {
    3: {
        0: "Destination network unreachable",
        1: "Destination host unreachable",
        2: "Destination protocol unreachable",
        3: "Destination port unreachable",
        4: "Fragmentation required",
        5: "Source route failed",
        6: "Destination network unkown",
        7: "Destination host unknown",
        8: "Source host isolated",
        9: "Network administratively prohibited",
        10: "Host administratively prohibited",
        11: "Network unreachable for given type of service",
        12: "Host unreachable for given type of service",
        13: "Coommunication administratively prohibited",
        14: "Host precedence violation",
        15: "Precedence cutoff in effect",
    },
    11: {
        0: "Time to live expired in transit",
        1: "Fragment reassembly time exceeded"
    },
    12: {
        0: "Pointer indicates error",
        1: "Missing a required option",
        2: "Bad length"
    }
}

def get_icmp_message(type: int, code:int) -> str:
    """
    Returns appropriate message for the given ICMP type and code
    """
    type_dictionary = ICMP_MESSAGE.get(type)

    if (not type_dictionary):
        return f"unknown ICMP type {type}, {code}"
    
    return type_dictionary.get(code, f"Unknown code {code} for type {type}")