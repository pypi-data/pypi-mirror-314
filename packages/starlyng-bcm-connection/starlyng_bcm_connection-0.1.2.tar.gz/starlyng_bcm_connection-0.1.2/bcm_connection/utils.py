"""conversion.py"""

def get_hostname(base_hostname: str, ip: str, port: int, public_ip: bool) -> str:
    """
    Gets the hostname based on local or public IP addresses.

    Args:
        ip (str): The IP address of the server.
        port (int): The port number of the server.

    Raises:
        ValueError: If the IP base address is not between 10 and 255 for local IPs

    Returns:
        str: The hostname of the server.
    """
    host_id = get_host_id(ip, port, public_ip)
    return f"{base_hostname}{host_id}"

def get_host_id(ip: str, port: int, public_ip: bool) -> str:
    """
    Gets the host ID based on local or public IP addresses.

    Args:
        ip (str): The IP address of the server.
        port (int): The port number of the server.

    Raises:
        ValueError: If the IP base address is not between 10 and 255 for local IPs
        ValueError: If the IP address is blank.

    Returns:
        str: The host ID as a two-digit string.
    """
    if not ip:
        raise ValueError("IP address cannot be blank")

    if not public_ip:
        ip_base_address = int(ip.split(".")[-1])
        if not 10 <= ip_base_address <= 255:
            raise ValueError(f"IP base address must be between 10 and 255: ip_base_address = {ip_base_address}")
        return f"{ip_base_address - 10:02d}"

    # For public IPs, extract last 2 digits of port number (e.g. 12345 -> 45)
    # and format as 2-digit string with leading zeros
    return f"{port % 100:02d}"

def get_ip_for_bcm(ip: str, vlan_id: int, public_ip: bool) -> str:
    """
    Gets the BCM IP address based on local or public IP addresses.

    Args:
        ip (str): The IP address of the server.
        vlan_id (int): The vlan ID of the bcm server.
        public_ip (bool): Whether the server is accessed via public IP.

    Raises:
        ValueError: If the IP address is blank.

    Returns:
        str: The BCM IP address, with VLAN ID injected for local IPs.
    """
    if not ip:
        raise ValueError("IP address cannot be blank")

    if not public_ip:
        # Split IP into octets and replace the third octet with vlan_id
        ip_parts = ip.split('.')
        ip_parts[2] = str(vlan_id)
        return '.'.join(ip_parts)

    return ip
