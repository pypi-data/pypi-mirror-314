'''
Author : Satyajit Ghosh
Date : 25-NOV-2024
Requirements:
Python 3.11.5 or above
paramiko==3.5.0

It is a NETCONF proxy server designed to provide comprehensive network communication interception and logging capabilities for NETCONF. 
This script offers network professionals, security researchers, and system administrators a powerful tool for monitoring, analyzing, 
and debugging network device interactions.
'''
from . import server
import time
import threading
from pathlib import Path


def tail_f(file_path):
    try:
        with open(file_path, 'r') as file:
            file.seek(0, 2)
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                print(line, end='')
    except KeyboardInterrupt:
        print("\nExiting...")


def start_proxy_server(proxy):
    try:
        proxy.start_server()
    except Exception as e:
        print(f"Error in proxy server: {e}")


def validate_ip(ip):
    """Validates if the input string is a valid IPv4 address."""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not (0 <= int(part) <= 255):
            return False
    return True


def validate_port(port):
    """Validates if the input is a valid port number."""
    return port.isdigit() and (0 < int(port) <= 65535)

def main():
    # Input validation
    while True:
        port_name = input("Enter the port name (e.g., DUTA-SSH, DUTB-NETCONF): ").strip()
        if port_name:
            break
        print("Port name cannot be empty. Please try again.")

    while True:
        remote_addr = input("Enter the DUT IP address (e.g., 127.0.0.1): ").strip()
        if validate_ip(remote_addr):
            break
        print("Invalid IP address. Please enter a valid IPv4 address.")

    while True:
        remote_port = input("Enter the DUT port number: ").strip()
        if validate_port(remote_port):
            remote_port = int(remote_port)
            break
        print("Invalid port number. Please enter a number between 1 and 65535.")

    while True:
        listen_port = input("Enter the port number to start the proxy server: ").strip()
        if validate_port(listen_port):
            listen_port = int(listen_port)
            break
        print("Invalid port number. Please enter a number between 1 and 65535.")

    while True:
        logdir = input("Enter the path to save log file: ").strip()
        logdir_path = Path(logdir)
        if logdir_path.exists() and logdir_path.is_dir():
            break
        print("Invalid directory path. Please enter a valid directory path.")

    # Initialize and start the proxy server
    proxy = server.SSHProxy(
        listen_addr='0.0.0.0',
        listen_port=listen_port,
        remote_addr=remote_addr,
        remote_port=remote_port,
        port_name=port_name,
        logdir=logdir
    )

    proxy_thread = threading.Thread(target=start_proxy_server, args=(proxy,))
    proxy_thread.daemon = True
    proxy_thread.start()

    # Prepare the log file and monitor it
    log_file_path = logdir_path.joinpath(port_name + '_server_responses.txt')
    with open(log_file_path, "w") as file:
        file.write("")
    print(f"Log saved into: {log_file_path}")

    # Monitor log file
    tail_f(log_file_path)
