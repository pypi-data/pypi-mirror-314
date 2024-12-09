"""connections.py"""
import logging
from typing import List, Dict, Union
import threading
import subprocess
from ssh_connection.models import Server

def ping_servers(servers: List[Server]) -> List[str]:
    """
    Ping a list of servers to check if they are online via SSH.

    Parameters:
    servers (List[Server]): A list of Server objects.

    Returns:
    List[str]: A list of offline server hostnames.
    """
    offline_hostnames = []
    threads = []

    for server in servers:
        thread = threading.Thread(target=_check_offline_ssh_worker, args=(server, offline_hostnames))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return offline_hostnames

def run_command_on_servers(servers: List[Server], command: Union[str, List[str]], timeout: int = 30) -> Dict[str, Dict[str, str]]:
    """
    Run a command or sequence of commands on multiple servers in parallel using SSH.
    Only runs commands on servers that are online.

    Parameters:
    servers (List[Server]): A list of Server objects.
    command (Union[str, List[str]]): The command(s) to run on each server. Can be a single command string
                                    or a list of commands to run in sequence.
    timeout (int): The maximum time to wait for the command execution (in seconds).

    Returns:
    Dict[str, Dict[str, str]]: A dictionary mapping hostnames to command results containing:
        'output': The command output if successful
        'error': Error message if the command failed
    """
    results = {}
    threads = []
    lock = threading.Lock()

    # First check which servers are offline
    offline_servers = ping_servers(servers)
    online_servers = [server for server in servers if server.hostname not in offline_servers]

    # Add offline servers to results with error message
    for hostname in offline_servers:
        results[hostname] = {
            'output': '',
            'error': 'Server is offline'
        }

    # Only run commands on online servers
    for server in online_servers:
        thread = threading.Thread(
            target=_run_command_worker,
            args=(server, command, results, lock, timeout)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results

def _check_offline_ssh(server: Server, timeout: int = 2) -> bool:
    """
    Check if a server is online by attempting to connect to it via SSH.

    Parameters:
    server (Server): A Server object.
    timeout (int): The maximum time to wait for the SSH connection (in seconds).

    Returns:
    bool: True if the server is online (connection successful), False otherwise.
    """
    ssh_command = [
        "ssh",
        '-o', 'StrictHostKeyChecking=no',
        "-i", server.ssh_key_path,
        "-p", str(server.ssh_port),
        f"{server.ssh_user}@{server.ip}",
        "exit",
    ]
    try:
        # Attempt to connect via SSH using subprocess
        subprocess.run(
            ssh_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        logging.info("SSH connection failed for %s:%s: %s", server.ip, server.ssh_port, str(e))
        return False

def _check_offline_ssh_worker(server: Server, offline_hostnames: List[str]):
    """
    Thread worker function to check SSH connectivity for a server.

    Parameters:
    server (Server): A Server object.
    offline_hostnames (List[str]): A shared list to store offline hostnames.
    """
    if not _check_offline_ssh(server):
        offline_hostnames.append(server.hostname)

def _run_command_worker(server: Server, command: Union[str, List[str]], results: Dict[str, Dict[str, str]], lock: threading.Lock, timeout: int):
    """
    Thread worker function to run a command or sequence of commands on a server via SSH.

    Parameters:
    server (Server): A Server object.
    command (Union[str, List[str]]): The command(s) to run. Can be a single command string or a list of commands.
    results (Dict[str, Dict[str, str]]): A shared dictionary to store command results.
    lock (threading.Lock): Thread lock for safely updating shared results.
    timeout (int): The maximum time to wait for command execution.
    """
    # Convert single command to list for consistent handling
    commands = [command] if isinstance(command, str) else command

    # Join multiple commands with semicolons
    command_str = "; ".join(commands)

    ssh_command = [
        "ssh",
        '-o', 'StrictHostKeyChecking=no',
        "-i", server.ssh_key_path,
        "-p", str(server.ssh_port),
        f"{server.ssh_user}@{server.ip}",
        command_str
    ]

    try:
        process = subprocess.run(
            ssh_command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        with lock:
            results[server.hostname] = {
                'output': process.stdout,
                'error': ''
            }
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        with lock:
            results[server.hostname] = {
                'output': '',
                'error': str(e)
            }
        logging.error("Command execution failed on %s:%s: %s", server.ip, server.ssh_port, str(e))
