"""SSH Connection library for checking server availability and managing server configurations.

This library provides:
- Server: Class for managing server configurations with SSH connection details
- ping_servers: Function to check multiple servers in parallel using threading
- run_command_on_servers: Function to execute commands on multiple servers
- get_hostname: Function to generate hostnames based on IP and port
- get_host_id: Function to generate host IDs from IP/port information
- get_ip_for_ssh: Function to format IP addresses for SSH connections
"""

from ssh_connection.connections import ping_servers, run_command_on_servers
from ssh_connection.utils import get_hostname, get_host_id, get_ip_for_ssh
from ssh_connection.models import Server

__all__ = [
    'Server',
    'ping_servers',
    'run_command_on_servers', 
    'get_hostname',
    'get_host_id',
    'get_ip_for_ssh'
]
