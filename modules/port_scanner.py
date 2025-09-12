import socket

TIMEOUT = 10 # seconds

def scan_port(target:str ,port:int) -> str:
    """
    Scan a single port of a given IPv4 target

    Args:
        target (str): The IPv4 address of the target machine
        port (int): the port number to scan

    Returns:
        str: The result of the port scan
    """
    is_tcp = is_tcp_open(target, port)
    is_udp = is_udp_open(target, port)
    if is_tcp and is_udp :
        service = socket.getservbyport(port, 'tcp')
        service += f"/{socket.getservbyport(port, 'udp')}"
        return f"OPEN (TCP/UDP) - Service: {service}"
    elif is_tcp:
        service = socket.getservbyport(port, 'tcp')
        return f"OPEN (TCP) - Service: {service}"
    elif is_udp:
        service = socket.getservbyport(port, 'udp')
        return f"OPEN (UDP) - Service: {service}"
    else:
        return f"Port {port} is closed or filtered"


    
def is_tcp_open(target:str ,port:int) -> bool:
    """
    Scan a single TCP port of a given IPv4 target

    Args:
        target (str): The IPv4 address of the target machine
        port (int): the port number to scan

    Returns:
        bool: True if 'OPEN', False if 'CLOSED' 
    """
    print(f"\nScanning TCP {target}:{port}")
    # result can be : OPEN or CLOSED
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT) # timeout after 5 seconds
            status = s.connect_ex((target, port)) # return status or raise exception
            if(status == 0):
                print(f"Port {port} is open")
                return True
            print(f"Port {port} is closed")
            return False
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
        return False

def is_udp_open(target:str ,port:int) -> bool:
    """
    Scan a single UDP port of a given IPv4 target

    Args:
        target (str): The IPv4 address of the target machine
        port (int): the port number to scan

    Returns:
        bool: True if 'OPEN', False otherwise ('FILTERED' or 'CLOSED')
    """
    print(f"\nScanning UDP {target}:{port}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(TIMEOUT) # timeout after 5 seconds
            s.sendto(b'', (target, port))
            s.recvfrom(1024)
        print(f"Port {port} is open")
        return True # OPEN
    except socket.timeout:
        print(f"Scan timed out, port {port} is filtered")
        return False # FILTERED
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
        return False # CLOSED