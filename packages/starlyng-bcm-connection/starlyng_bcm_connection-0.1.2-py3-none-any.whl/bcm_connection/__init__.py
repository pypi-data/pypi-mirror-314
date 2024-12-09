"""BCM Connection library for executing BCM commands and managing server configurations.

This library provides:
- execute_bcm_command: Function to execute BCM commands on servers
- BCMServer: Class for managing BCM server configurations
"""

from bcm_connection.bcm import execute_bcm_command
from bcm_connection.utils import get_hostname, get_host_id, get_ip_for_bcm
from bcm_connection.models import BCMServer

__version__ = "0.0.1"

__all__ = [
    "execute_bcm_command",
    "BCMServer",
    "get_hostname",
    "get_host_id",
    "get_ip_for_bcm"
]
