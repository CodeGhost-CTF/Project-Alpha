"""
Advanced Network Packet Sniffer with Protocol Analysis
- TCP/UDP/ICMP dissection
- HTTP header extraction
- GeoIP lookup
- Real-time statistics
"""

import socket
import struct
import dpkt
import geoip2.database
from collections import defaultdict
import time

class NetworkWatcher:
    def __init__(self):
        self.geo_reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        self.stats = {
            'protocols': defaultdict(int),
            'countries': defaultdict(int),
            'ports': defaultdict(int)
        }
    
    def _parse_ip_header(self, raw_data):
        """Extract IP header information"""
        version_ihl = raw_data[0]
        version = version_ihl >> 4
        ihl = (version_ihl & 0xF) * 4
        ttl, proto, src, dest = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        return {
            'version': version,
            'src': socket.inet_ntoa(src),
            'dest': socket.inet_ntoa(dest),
            'protocol': proto
        }

    def _get_country(self, ip):
        """GeoIP lookup using MaxMind database"""
        try:
            response = self.geo_reader.city(ip)
            return response.country.iso_code
        except:
            return 'Unknown'

    def start_sniffing(self, interface='eth0'):
        """Main capture loop"""
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        
        try:
            while True:
                raw_data, addr = conn.recvfrom(65535)
                ip_header = self._parse_ip_header(raw_data[14:34])
                
                # Update statistics
                self.stats['protocols'][ip_header['protocol']] += 1
                country = self._get_country(ip_header['src'])
                self.stats['countries'][country] += 1
                
                # Deep packet inspection
                if ip_header['protocol'] == 6:  # TCP
                    self._process_tcp(raw_data[ihl:])
                
                # ... other protocol handlers ...

        except KeyboardInterrupt:
            self.generate_report()

    def _process_tcp(self, segment):
        """TCP payload analysis"""
        # ... HTTP header extraction logic ...

# Example usage:
# watcher = NetworkWatcher()
# watcher.start_sniffing()