class UDPProbes:
    """Probe payloads for common UDP services"""

    @staticmethod
    def get_dns_query():
        return b''
    
    @staticmethod
    def get_probe(port: int) -> bytes:
        probes = {
            53: UDPProbes.get_dns_query
        }

        if (port in probes):
            try:
                return probes[port]()
            except:
                return b''

        return b''