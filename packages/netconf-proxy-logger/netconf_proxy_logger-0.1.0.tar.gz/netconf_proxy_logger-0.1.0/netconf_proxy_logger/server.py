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

import socket
import threading
import paramiko
import select
import datetime
import logging
from pathlib import Path
import os
import json

class SSHProxy:
    def __init__(self,port_name='DUT', listen_addr='127.0.0.1', listen_port=10022, 
                 remote_addr='127.0.0.1', remote_port=22,logdir=''):
        self.listen_addr = listen_addr
        self.listen_port = listen_port
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        self.port_name = port_name
        # Setup host key
        self.host_key_path = Path('ssh_proxy_key')
        self.server_key = self.get_host_key()
        
        # Initialize logging
        self.log_file = 'ssh_events.log'
        logdir = Path(logdir)
        self.response_file = logdir.joinpath(port_name + '_server_responses.txt')
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )

    def log_server_response(self, username, data, is_netconf=False):
        """Log server response to separate text file"""
        try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.response_file, 'a', encoding='utf-8') as f:
                if isinstance(data, bytes):
                    decoded_data = data.decode('utf-8', errors='replace').strip()
                else:
                    decoded_data = str(data).strip()
                
                if decoded_data:
                        f.write(f"{decoded_data}\n")
                        f.flush()
        except Exception as e:
            logging.error(f"Error logging server response: {str(e)}")

    def get_host_key(self):
        """Get or generate a persistent host key"""
        try:
            if self.host_key_path.exists():
                return paramiko.RSAKey(filename=str(self.host_key_path))
            else:
                key = paramiko.RSAKey.generate(2048)
                key.write_private_key_file(str(self.host_key_path))
                print(f"Generated new host key. Fingerprint: {key.get_fingerprint().hex()}")
                return key
        except Exception as e:
            logging.error(f"Error handling host key: {str(e)}")
            return paramiko.RSAKey.generate(2048)

    def log_event(self, event_type, client_addr, username=None, data=None, is_netconf=False):
        """Log SSH events with structured data"""
        try:
            timestamp = datetime.datetime.now().isoformat()
            event = {
                "timestamp": timestamp,
                "event_type": event_type,
                "client_ip": client_addr[0],
                "client_port": client_addr[1],
                "username": username,
                "protocol": "netconf" if is_netconf else "ssh"
            }

            if data:
                try:
                    if isinstance(data, bytes):
                        decoded_data = data.decode('utf-8', errors='replace').strip()
                    else:
                        decoded_data = str(data).strip()
                    
                    if decoded_data:
                        event["data"] = decoded_data
                except Exception as e:
                    event["data"] = "[Binary data]"
                    event["decode_error"] = str(e)

            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event) + '\n')
                f.flush()

        except Exception as e:
            logging.error(f"Error logging event: {str(e)}")

    def handle_netconf_messages(self, client_channel, remote_channel, client_addr, username):
        """Handle NETCONF message forwarding with proper framing"""
        def read_netconf_msg(channel):
            buffer = ""
            while True:
                try:
                    data = channel.recv(4096).decode('utf-8')
                    if not data:
                        return None
                    buffer += data
                    if ']]>]]>' in buffer:
                        msg, _, remaining = buffer.partition(']]>]]>')
                        return msg + ']]>]]>'
                except Exception as e:
                    logging.error(f"Error reading NETCONF message: {str(e)}")
                    return None

        while True:
            r, w, x = select.select([client_channel, remote_channel], [], [], 0.1)
            
            if client_channel in r:
                msg = read_netconf_msg(client_channel)
                if not msg:
                    break
                remote_channel.send(msg.encode('utf-8'))
                self.log_event("netconf_client_message", client_addr, username, msg, True)
                self.log_server_response(username, msg, True)
            
            if remote_channel in r:
                msg = read_netconf_msg(remote_channel)
                if not msg:
                    break
                client_channel.send(msg.encode('utf-8'))
                self.log_server_response(username, msg, True)

    def handle_client_transport(self, client_sock):
        """Handle the client's SSH transport"""
        client_transport = None
        remote_transport = None
        client_addr = client_sock.getpeername()
        
        try:
            self.log_event("connection_attempt", client_addr)
            
            client_transport = paramiko.Transport(client_sock)
            client_transport.set_gss_host(socket.getfqdn(""))
            client_transport.add_server_key(self.server_key)
            
            server_handler = ProxySSHServer()
            client_transport.start_server(server=server_handler)
            
            client_channel = client_transport.accept(60)
            if client_channel is None:
                self.log_event("connection_failed", client_addr, 
                             data="No channel established")
                return

            self.log_event("authentication_successful", client_addr, 
                          username=server_handler.username)

            remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_sock.connect((self.remote_addr, self.remote_port))
            
            remote_transport = paramiko.Transport(remote_sock)
            remote_transport.start_client()
            
            username = server_handler.username
            password = server_handler.password
            
            remote_transport.auth_password(username, password)
            remote_channel = remote_transport.open_session()
            
            # Check if this is a NETCONF session
            if server_handler.is_netconf:
                remote_channel.invoke_subsystem('netconf')
                self.log_event("netconf_session_started", client_addr, username)
                self.handle_netconf_messages(client_channel, remote_channel, client_addr, username)
            else:
                term = os.environ.get('TERM', 'xterm')
                remote_channel.get_pty(term=term, width=80, height=24)
                remote_channel.invoke_shell()
                self.log_event("ssh_session_started", client_addr, username)
                self.forward_data(client_channel, remote_channel, client_addr, username)
            
        except Exception as e:
            self.log_event("error", client_addr, 
                          data=f"Transport error: {str(e)}")
        finally:
            self.log_event("session_ended", client_addr, 
                          username=server_handler.username if hasattr(server_handler, 'username') else None)
            if client_transport:
                client_transport.close()
            if remote_transport:
                remote_transport.close()

    def forward_data(self, client_channel, remote_channel, client_addr, username):
        """Forward data between client and remote server with event logging"""
        try:
            while True:
                r, w, x = select.select([client_channel, remote_channel], [], [], 0.01)
                
                if client_channel in r:
                    try:
                        data = client_channel.recv(1024)
                        if len(data) == 0:
                            break
                        remote_channel.send(data)
                    except socket.timeout:
                        pass
                    except Exception as e:
                        self.log_event("error", client_addr, username,
                                     f"Client receive error: {str(e)}")
                        break
                
                if remote_channel in r:
                    try:
                        data = remote_channel.recv(1024)
                        if len(data) == 0:
                            break
                        client_channel.send(data)
                        self.log_server_response(username, data)
                    except socket.timeout:
                        pass
                    except Exception as e:
                        self.log_event("error", client_addr, username,
                                     f"Server receive error: {str(e)}")
                        break
                
                if client_channel.closed or remote_channel.closed:
                    break
                
        except Exception as e:
            self.log_event("error", client_addr, username,
                          f"Forward error: {str(e)}")
        
        finally:
            client_channel.close()
            remote_channel.close()

    def start_server(self):
        """Start the SSH proxy server"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.listen_addr, self.listen_port))
            sock.listen(5)
            
            logging.info(f"SSH Proxy listening on {self.listen_addr}:{self.listen_port}")
            print(f"Host key fingerprint: {self.server_key.get_fingerprint().hex()}")
            
            while True:
                client_sock, addr = sock.accept()
                client_thread = threading.Thread(
                    target=self.handle_client_transport,
                    args=(client_sock,)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
        
        finally:
            sock.close()

class ProxySSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.username = None
        self.password = None
        self.is_netconf = False

    def check_auth_password(self, username, password):
        self.username = username
        self.password = password
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED

    def check_channel_subsystem_request(self, channel, name):
        if name == 'netconf':
            self.is_netconf = True
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        return True

    def check_channel_window_change_request(self, channel, width, height, pixelwidth,
                                          pixelheight):
        return True

# if __name__ == "__main__":
    
#     proxy = SSHProxy(
#         listen_addr='127.0.0.1',
#         listen_port=10031,
#         remote_addr='127.0.0.1', 
#         remote_port=32848
#     )
#     proxy.start_server()
