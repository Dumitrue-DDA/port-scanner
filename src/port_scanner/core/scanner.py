import socket
import logging
from .utils import get_icmp_message
from .udp_probes import UDPProbes
from scapy.sendrecv import sr1
from scapy.layers.inet import IP, UDP, ICMP

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

    if protocol == 'tcp' or protocol == 'both':
        logger.debug(f"Scanning TCP port")

        tcp_status = get_tcp_status(target, port, timeout, logger)
        tcp_service = "Unknown"

        if (tcp_status == "Open"):
            try:
                tcp_service = socket.getservbyport(port, 'tcp')
            except:
                logger.debug(f"Unable to get service name for {port}/tcp")

        result += f"{port}/tcp is {tcp_status} - Service: {tcp_service}\n"

    if protocol == 'udp' or protocol == 'both':
        logger.debug(f"Scanning UDP port")
        udp_status = get_udp_status(target,port,timeout,logger)
        result += f"{port}/udp is {udp_status}"

    return result
    
def get_tcp_status(target:str ,port:int, timeout:int, logger:logging.Logger) -> str:
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
                return "Open"
            
            return "Closed"
    except Exception as e:
        logger.error(f"Error scanning port {port}: {e}")
        return "Closed"
    
def get_udp_status(target:str ,port:int, timeout:int,\
                    logger:logging.Logger) -> str:
    """
    Gets status of the UDP port by interpreting response to a generic packet.\n
    First check if a response is received\n
    Then checks if it has a ICMP layer and interprets its type and code\n
    Finally checks if the response has a UDP layer, and returns open if so

    Args:
        target (str): Target IP address
        port (int): Port that is scanned
        timeout (int): Maximum time spent waiting for a response
        logger (logging.Logger): Logger instance 
    """
    payload = UDPProbes.get_probe(port)

    if (payload is not b''):
        packet = IP(dst=target)/UDP(dport=port)/payload
        logger.debug(f"Sending service specific payload")
    else:
        packet = IP(dst=target)/UDP(dport=port)
        logger.debug(f"Sending generic payload")

    # send packet and get response
    response = sr1(packet, timeout=timeout, verbose=0)

    # analyze response
    if (response is None):
        logger.debug(f"No response, port {port} is open|filtered")
        return "Open/Filtered" 
    
    if (response.haslayer(ICMP)):
        icmp_layer = response[ICMP]
        # interpret ICMP type
        if (icmp_layer.type == 3): # destination unreacheable
            logger.debug(f"ICMP type {icmp_layer.type}, code {icmp_layer.code} \
                        -> {get_icmp_message(icmp_layer.type, icmp_layer.code)}")
            return "Closed"
        else:
            logger.debug(f"ICMP type {icmp_layer.type}, code {icmp_layer.code} \
                        -> {get_icmp_message(icmp_layer.type, icmp_layer.code)}")
            return "Filtered"
        
    elif (response.haslayer(UDP)):
        return "Open" 
    
    # handling unexpected response
    return "Unknown"