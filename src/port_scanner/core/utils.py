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
