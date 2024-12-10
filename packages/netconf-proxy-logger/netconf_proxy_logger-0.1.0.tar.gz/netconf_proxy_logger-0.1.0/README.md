# NETCONF Proxy Logger

## Overview

NETCONF Proxy Logger is a comprehensive logging tool for NETCONF communications, designed to intercept and log all interactions between NETCONF clients and servers. This tool provides detailed insights into NETCONF protocol exchanges, helping network administrators and developers understand and debug network device communications.

## Features

- Full logging of NETCONF client-server communications
- Detailed XML message capture
- Easy integration with existing NETCONF workflows

## Installation

Install the package using pip:

```bash
pip install netconf-proxy-logger
```

## Usage

### Basic Usage

```python
from netconf_proxy_logger import SSHProxy

# Configure and start the proxy
proxy = SSHProxy(
    listen_addr='127.0.0.1',
    listen_port=13500,
    remote_addr='127.0.0.1', 
    remote_port=33151
)
proxy.start_server()
```
![Preview](demo.png)


### Command Line Usage

```bash
netconflog
```

## Requirements

- Python 3.7+
- paramiko>=3.1.0,<4.0.0

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - contact@satyajit.co.in

Project Link: [https://github.com/SATYAJIT1910/netconf-proxy-logger](https://github.com/SATYAJIT1910/netconf-proxy-logger)