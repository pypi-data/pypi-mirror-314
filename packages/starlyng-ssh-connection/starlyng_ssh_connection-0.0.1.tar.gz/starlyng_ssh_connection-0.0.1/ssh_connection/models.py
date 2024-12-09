"""models.py"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Server:
    # pylint: disable=too-many-instance-attributes
    """
    Represents a server with its connection details.

    Attributes:
        hostname (str): The hostname of the server.
        ip (str): The IP address of the SSH network interface.
        public_ip (str): The servers are accessed via public IP addresses.
        ssh_key_path (Optional[str]): The path to the SSH key file, if applicable.
        ssh_port (int): The SSH port number of the server.
        ssh_user (str): The SSH username for the server.
        ssh_vlan_id (int): The VLAN ID for the SSH network interface.
    """
    hostname: str
    ip: str
    public_ip: bool
    ssh_key_path: Optional[str]
    ssh_port: int
    ssh_user: str
    ssh_vlan_id: int

    def __post_init__(self):
        """Validate the data types of the fields after initialization."""
        if not isinstance(self.ssh_port, int):
            raise TypeError("port must be an integer")
        if self.ssh_key_path is not None and not isinstance(self.ssh_key_path, str):
            raise TypeError("ssh_key_path must be a string or None")
