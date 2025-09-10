import socket
import ipaddress
import datetime
from modules.port_scanner import scan_ports, scan_port_range

"""
-- Port Scanner Tool --
A simple network port scanner that can scan single ports or port ranges
on target IP addresses or domain names.
"""

# -- Functions --
def is_ip(address: str) -> bool:
    try:
        ipaddress.ip_address(address)
        return True
    except Exception:
        return False

def resolve_domain(domain: str) -> str:
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        raise RuntimeError("Couldn't resolve domain name")

# -- Main --

print("=" * 50)
print("    Welcome to Port Scanner Tool")
print("=" * 50)
print("This tool allows you to scan a single port on a target IPv4 address or domain name")
print("Common ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 21 (FTP), 25 (SMTP)")

start_time = datetime.now()

# Check if the target ip/domain is valid

valid_target = False
while (not valid_target):
    try:
        target = input("Enter target (IPv4 address or domain name): ").strip()

        if not is_ip(target):
            resolved_ip = resolve_domain(target)
            print(f"✓ Resolved domain {target} -> {resolved_ip}")
            target = resolved_ip
            valid_target = True
        else:
            print(f"✓ Valid IP address: {target}")
            valid_target = True
    except Exception as e:
        print(f"Invalid target! {e}")

# Check if the port is valid

valid_port = False
while (not valid_port):
    try:
        port = int(input("Enter the port to be scanned:\n"))
        if(port < 1 or port > 65535):
            raise Exception(f"Port {port} is outside valid range.\n"
                "Please enter a port between 1 and 65535.")
        valid_port = True
        print("Port is valid")
    except Exception as e:
        print(f"Invalid port! {e}")

# Start the scan

scan_ports(target, port)

print(f"Scan completed!")
print(f"Status: ")
print(f"Scan duration: {datetime.now() - start_time}")   