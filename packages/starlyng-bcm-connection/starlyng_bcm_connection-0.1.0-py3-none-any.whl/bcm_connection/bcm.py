"""BCM utility module for server management and control operations."""

import logging
import subprocess
import threading
from typing import List, Tuple
from bcm_connection.models import BCMServer

def execute_bcm_command(servers: List[BCMServer], command: str) -> List[Tuple[BCMServer, str]]:
    """
    Executes an IPMI command on multiple servers and returns the results.

    Examples:
        >>> execute_bcm_command(servers, "chassis power status")  # Check power status of servers
        >>> execute_bcm_command(servers, "chassis power off")     # Power off all servers
        >>> execute_bcm_command(servers, "chassis power on")      # Power on all servers
        >>> execute_bcm_command(servers, "sel list")              # Get System Event Log (SEL) entries
        >>> execute_bcm_command(servers, "sel clear")             # Clear System Event Log (SEL) entries

    Args:
        servers (List[Server]): List of Server objects
        command (str): IPMI command to execute

    Returns:
        List[Tuple[Server, str]]: List of tuples containing Server objects and command results
    """
    results = []
    _bcm_threaded_process(servers, command, results)
    return results

def _bcm_command(server: BCMServer, command: str) -> List[str]:
    """
    Returns an IPMI command that can be passed to subprocess.run

    Args:
        server (Server): Server object containing connection details
        command (str): IPMI command to execute

    Returns:
        List[str]: Complete IPMI command as a list of strings
    """
    return [
        "ipmitool",
        "-I", "lanplus",
        "-H", server.bcm_ip,
        "-U", server.bcm_user,
        "-P", server.bcm_pass,
        "-p", server.bcm_port,
    ] + command.split()

def _bcm_threaded_process(servers: List[BCMServer], command: str, result: List[Tuple[BCMServer, str]]=None) -> None:
    """
    Executes an IPMI command on multiple servers in parallel using threads.

    Args:
        servers (List[Server]): List of Server objects
        command (str): IPMI command to execute
        result (List[Tuple[Server, str]], optional): List to store command results
    """
    threads = [
        threading.Thread(target=_run_bcm_subprocess, args=(server, command, result))
        for server in servers
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def _run_bcm_subprocess(server: BCMServer, command: str, subprocess_result: List[Tuple[BCMServer, str]]=None) -> subprocess.CompletedProcess:
    """
    Executes an IPMI command on a remote server and logs any errors.

    Args:
        server (Server): Server object containing connection details
        command (str): IPMI command to execute
        subprocess_result (List[Tuple[Server, str]], optional): List to store command results

    Returns:
        subprocess.CompletedProcess: Result of the subprocess run

    Logs:
        Errors if the command execution fails or if there is any error output
    """
    try:
        result = subprocess.run(_bcm_command(server, command), capture_output=True, text=True, check=True)
        if subprocess_result is not None:
            subprocess_result.append((server, result.stdout.strip()))
        if result.stderr:
            logging.error("run_subprocess: Errors from %s:%s %s\n%s", server.bcm_ip, server.bcm_port, command, result.stderr)
    except subprocess.CalledProcessError as e:
        logging.error("Failed to execute on %s:%s: %s", server.bcm_ip, server.bcm_port, e)
        result = subprocess.CompletedProcess(args=command, returncode=e.returncode, stdout='', stderr=str(e))
    return result
