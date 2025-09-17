"""
Default configuration settings for the port scanner.
"""

# Default timeout for port scans (in seconds)
DEFAULT_TIMEOUT = 10

# Default protocol to scan
DEFAULT_PROTOCOL = 'both'

# Maximum number of concurrent scans (for future range scanning)
MAX_CONCURRENT_SCANS = 100

# Port range limits
MIN_PORT = 1
MAX_PORT = 65535

# Common ports to scan if no port specified (for future implementation)
COMMON_PORTS = [
    21,    # FTP
    22,    # SSH
    23,    # Telnet
    25,    # SMTP
    53,    # DNS
    80,    # HTTP
    110,   # POP3
    143,   # IMAP
    443,   # HTTPS
    993,   # IMAPS
    995,   # POP3S
    1433,  # MSSQL
    3306,  # MySQL
    3389,  # RDP
    5432,  # PostgreSQL
    5900,  # VNC
    8080,  # HTTP-alt
    8443,  # HTTPS-alt
]

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%H:%M:%S'
