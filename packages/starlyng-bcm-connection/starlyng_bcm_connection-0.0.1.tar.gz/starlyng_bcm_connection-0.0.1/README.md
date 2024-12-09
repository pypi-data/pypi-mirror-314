# Starlyng BCM Connection

A Python library for executing Baseboard Management Controller (BMC) commands on servers using IPMI.

## Features

- Execute BMC commands on remote servers using IPMI via `execute_bcm_command`
- Parallel execution of commands across multiple servers using threading
- Comprehensive error logging and handling
- Support for common IPMI operations:
  - Power management (status, on, off, cycle, reset)
  - System Event Log (SEL) operations
  - Chassis control
- Flexible server configuration through `BCMServer` class
- Secure connection handling with IPMI over LAN (LANPLUS)
- Command output capture and structured response handling

## Prerequisites

Before you begin, ensure you have:
* Python 3.9 or higher installed
* ipmitool installed on your system:
  * Ubuntu: `sudo apt-get install ipmitool`
  * macOS: `brew install ipmitool`
* If outside local network, configure port forwarding on your router:
  * Forward BCM port 623 to each server's unique port (62300-62399)
  * Example: Forward port 62300 to 192.168.50.1:623, port 62301 to 192.168.50.2:623
  * Port range must be between 62300-62399

## Installation

```bash
pip install starlyng-bcm-connection
```

## Usage

### Basic Example

```python
from starlyng_bcm_connection import BCMServer, execute_bcm_command

# Create a BCM server instance
server = BCMServer(
    bcm_ip="192.168.1.1",
    bcm_user="admin"
    bcm_pass="password"
    bcm_port=623
)

# Execute a command
# Pass server in a list since execute_bcm_command expects List[BCMServer]
result = execute_bcm_command([server], "power status")
print(result)
```

## Available BMC Commands

Common IPMI commands you can execute:
- `power status` - Get power status
- `power on` - Power on the server
- `power off` - Power off the server
- `power cycle` - Power cycle the server
- `power reset` - Reset the server

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## Contact

If you have any questions, please contact:

- GitHub: [@justinsherwood](https://github.com/justinsherwood)