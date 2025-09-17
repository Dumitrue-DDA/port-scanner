import socket
import logging

def scan_port(target:str ,port:int, protocol:str, timeout:int, logger:logging.Logger) -> str:
    """
    Scan a single port of a given IPv4 target

    Args:
        target (str): The IPv4 address of the target machine
        port (int): the port number to scan

    Returns:
        str: The result of the port scan
    """
    result = ""

    tcp_open = None
    udp_open = None

    if protocol == 'tcp' or protocol == 'both':
        logger.debug(f"Scanning TCP port")
        tcp_open = is_tcp_open(target, port, timeout, logger)
        if tcp_open == True:
            try:
                tcp_service = socket.getservbyport(port, 'tcp')
            except:
                tcp_service = "unknown"
            result += f"{port}/tcp is open - Service: {tcp_service}\n"
        else:
            result += f"{port}/tcp is closed\n"
    if protocol == 'udp' or protocol == 'both':
        logger.debug(f"Scanning UDP port")
        udp_open = is_udp_open(target, port, timeout, logger)
        if udp_open == True:
            try:
                udp_service = socket.getservbyport(port, 'udp')
            except:
                udp_service = "unknown"
            result += f"{port}/udp is open - Service: {udp_service}\n"
        else:
            result += f"{port}/udp is closed\n"

    return result
    
def is_tcp_open(target:str ,port:int, timeout:int, logger:logging.Logger) -> bool:
    """
    Scan a single TCP port of a given IPv4 target

    Args:
        target (str): The IPv4 address of the target machine
        port (int): the port number to scan

    Returns:
        bool: True if 'OPEN', False if 'CLOSED' 
    """
    # result can be : OPEN or CLOSED
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout) 
            status = s.connect_ex((target, port)) # return status or raise exception
            if(status == 0):
                logger.debug(f"Port {port} is open")
                return True
            logger.debug(f"Port {port} is closed")
            return False
    except Exception as e:
        logger.error(f"Error scanning port {port}: {e}")
        return False

def is_udp_open(target:str ,port:int, timeout:int, logger:logging.Logger) -> bool:
    """
    Scan a single UDP port of a given IPv4 target

    Args:
        target (str): The IPv4 address of the target machine
        port (int): the port number to scan

    Returns:
        bool: True if 'OPEN', False otherwise ('FILTERED' or 'CLOSED')
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout) # timeout after 5 seconds
            s.sendto(b'', (target, port))
            s.recvfrom(1024)
        logger.debug(f"Port {port} is open")
        return True # OPEN
    except socket.timeout:
        logger.debug(f"Scan timed out, port {port} is filtered")
        return False # FILTERED
    except Exception as e:
        logger.error(f"Error scanning port {port}: {e}")
        return False # CLOSED