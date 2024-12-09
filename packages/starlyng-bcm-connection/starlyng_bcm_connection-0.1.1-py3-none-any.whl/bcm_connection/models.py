"""Data models and structures for BCM operations."""

from dataclasses import dataclass

@dataclass
class BCMServer:
    # pylint: disable=too-many-instance-attributes
    """
    Represents a server with its connection details.

    Attributes:
        bcm_ip (str): The IP address of the BCM network interface.
        bcm_pass (str): The password for BCM access.
        bcm_port (int): The port number for BCM access.
        bcm_user (str): The username for BCM access.
    """
    bcm_ip: str
    bcm_user: str
    bcm_pass: str
    bcm_port: int
    hostname: str

    def __post_init__(self):
        """Validate the data types of the fields after initialization."""
        if not isinstance(self.bcm_port, int):
            raise TypeError("bcm_port must be an integer")
